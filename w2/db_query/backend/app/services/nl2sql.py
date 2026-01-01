"""Natural Language to SQL conversion service using Google Gemini."""

import google.generativeai as genai
from app.config import settings
from app.models.database import DatabaseType
import logging
import asyncio

logger = logging.getLogger(__name__)


class NaturalLanguageToSQLService:
    """Service for converting natural language queries to SQL using Google Gemini."""

    def __init__(self):
        """Initialize Gemini client."""
        genai.configure(api_key=settings.gemini_api_key)
        # Use gemini-2.5-flash as default (fast and cost-effective for SQL generation)
        # Model names should NOT include 'models/' prefix when using GenerativeModel
        self.model_name = "gemini-2.5-flash"
        self.model = genai.GenerativeModel(self.model_name)
        logger.info(f"Initialized Gemini model: {self.model_name}")

    def _build_prompt(
        self, user_prompt: str, metadata: dict, db_type: DatabaseType = DatabaseType.POSTGRESQL
    ) -> str:
        """Build the prompt for Gemini with database metadata context.

        Args:
            user_prompt: Natural language query from user
            metadata: Database schema metadata dictionary
            db_type: Database type (PostgreSQL or MySQL)

        Returns:
            Complete prompt string for Gemini
        """
        # Build schema context
        schema_context = []
        for table in metadata.get("tables", []):
            columns_info = []
            for col in table.get("columns", []):
                col_desc = f"  - {col['name']} ({col['dataType']})"
                if col.get("primaryKey"):
                    col_desc += " PRIMARY KEY"
                if not col.get("nullable", True):
                    col_desc += " NOT NULL"
                if col.get("unique"):
                    col_desc += " UNIQUE"
                columns_info.append(col_desc)

            row_count = table.get("rowCount", "unknown")
            table_info = f"Table: {table['schemaName']}.{table['name']} ({row_count} rows)\n"
            table_info += "\n".join(columns_info)
            schema_context.append(table_info)

        for view in metadata.get("views", []):
            columns_info = [f"  - {col['name']} ({col['dataType']})" for col in view.get("columns", [])]
            view_info = f"View: {view['schemaName']}.{view['name']}\n"
            view_info += "\n".join(columns_info)
            schema_context.append(view_info)

        schema_text = "\n\n".join(schema_context)

        # Build database-specific rules
        if db_type == DatabaseType.MYSQL:
            db_name = "MySQL"
            syntax_rules = """3. Use backticks for identifiers (e.g., `table_name`, `column_name`)
4. Return valid MySQL syntax
5. Use MySQL LIMIT syntax (LIMIT n)
6. Be aware of MySQL-specific features like AUTO_INCREMENT"""
        else:
            db_name = "PostgreSQL"
            syntax_rules = """3. Use proper schema qualification (schema.table)
4. Return valid PostgreSQL syntax
5. Use double quotes for identifiers if needed"""

        system_prompt = f"""You are an expert SQL query generator for {db_name} databases.

Database Schema:
{schema_text}

Rules:
1. Generate ONLY SELECT queries (no INSERT/UPDATE/DELETE/DROP)
2. Always include LIMIT clause (max 1000 rows)
{syntax_rules}
7. Handle both English and Chinese natural language
8. Be concise - return just the SQL query

Output format:
Return ONLY the SQL query, nothing else. No explanations, no markdown code blocks, just the SQL query."""

        full_prompt = f"{system_prompt}\n\nUser query: {user_prompt}\n\nSQL Query:"
        return full_prompt

    async def generate_sql(
        self, user_prompt: str, metadata: dict, db_type: DatabaseType = DatabaseType.POSTGRESQL
    ) -> dict[str, str]:
        """Convert natural language to SQL query.

        Args:
            user_prompt: Natural language query
            metadata: Database schema metadata dictionary
            db_type: Database type (PostgreSQL or MySQL)

        Returns:
            Dict with 'sql' and 'explanation' keys

        Raises:
            Exception: If Gemini API call fails
        """
        prompt = self._build_prompt(user_prompt, metadata, db_type)

        # Try different model names if default fails
        # Remove 'models/' prefix from default name to get base name
        base_name = self.model_name.replace('models/', '')
        
        # Build list of model names to try (avoid duplicates)
        model_names_to_try = []
        seen = set()
        
        # Add current model name first
        if self.model_name not in seen:
            model_names_to_try.append(self.model_name)
            seen.add(self.model_name)
        
        # Add base name variation (without 'models/' prefix)
        if base_name not in seen:
            model_names_to_try.append(base_name)
            seen.add(base_name)
        
        # Add with 'models/' prefix if different
        prefixed = f"models/{base_name}"
        if prefixed != self.model_name and prefixed not in seen:
            model_names_to_try.append(prefixed)
            seen.add(prefixed)
        
        # Add other common model names (updated to use available models)
        for candidate in [
            "gemini-2.5-flash",  # Fast and cost-effective
            "gemini-2.5-pro",    # More capable
            "gemini-2.0-flash",  # Alternative flash model
            "gemini-1.5-pro",    # Legacy model (may not be available)
            "gemini-1.5-flash",  # Legacy model (may not be available)
        ]:
            if candidate not in seen:
                model_names_to_try.append(candidate)
                seen.add(candidate)

        last_error = None
        for model_name in model_names_to_try:
            try:
                # Create model instance for this attempt
                try:
                    model = genai.GenerativeModel(model_name)
                except Exception as e:
                    logger.debug(f"Failed to create model {model_name}: {e}")
                    continue

                # Call Gemini API in a thread pool to avoid blocking
                def _generate(model_instance=model):
                    response = model_instance.generate_content(
                        prompt,
                        generation_config=genai.types.GenerationConfig(
                            temperature=0.1,  # Low temperature for consistent SQL generation
                            max_output_tokens=500,
                        ),
                    )
                    return response.text

                # Run in executor to make it async
                try:
                    loop = asyncio.get_running_loop()
                except RuntimeError:
                    loop = asyncio.get_event_loop()
                generated_sql = await loop.run_in_executor(None, _generate)
                # Success! Update the model name for future use
                if model_name != self.model_name:
                    logger.info(f"Successfully used model: {model_name}, updating default")
                    self.model_name = model_name
                    self.model = model
                break
            except Exception as e:
                error_msg = str(e)
                last_error = e
                logger.debug(f"Failed with model {model_name}: {error_msg}")
                # If it's a 404, try next model. Otherwise, it might be a different error
                if "404" not in error_msg and "not found" not in error_msg.lower():
                    # Not a model name issue, re-raise
                    raise
                continue
        else:
            # All models failed
            raise Exception(
                f"Failed to generate SQL with any available model. "
                f"Tried: {model_names_to_try}. Last error: {str(last_error)}"
            )

        # Clean up the response (remove markdown code blocks if present)
        generated_sql = generated_sql.strip()
        if generated_sql.startswith("```sql"):
            generated_sql = generated_sql.replace("```sql", "").replace("```", "").strip()
        elif generated_sql.startswith("```"):
            generated_sql = generated_sql.replace("```", "").strip()

        # Remove any leading/trailing whitespace or newlines
        generated_sql = generated_sql.strip()

        # Generate explanation
        explanation = f"Generated SQL from: {user_prompt}"

        logger.info(f"Generated SQL for prompt: {user_prompt[:50]}...")

        return {"sql": generated_sql, "explanation": explanation}


# Global instance
nl2sql_service = NaturalLanguageToSQLService()
