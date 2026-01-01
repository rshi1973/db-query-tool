# Database Query Tool - Frontend

React-based web frontend for the Database Query Tool, built with Refine 5, Ant Design, and Monaco Editor.

## Tech Stack

- **React 18+**: UI library
- **TypeScript 5+**: Type-safe JavaScript
- **Refine 5**: React admin framework
- **Ant Design 5**: UI component library
- **Monaco Editor**: SQL code editor (VS Code editor engine)
- **Tailwind CSS 4**: Utility-first CSS framework
- **Vite**: Fast build tool and dev server
- **Axios**: HTTP client
- **React Router**: Client-side routing

## Prerequisites

- Node.js 18+ (LTS recommended)
- npm or yarn package manager

## Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
# or
yarn install
```

### 2. Configure Environment

Create `.env.local` file (optional, defaults provided):

```bash
cp .env.local.example .env.local
```

Environment variables:

- `VITE_API_BASE_URL`: Backend API URL (default: `http://localhost:8000`)

### 3. Start Development Server

```bash
npm run dev
# or
yarn dev
```

The application will be available at `http://localhost:5173`

## Development

### Available Scripts

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linter
npm run lint

# Run tests
npm test
```

### Project Structure

```
frontend/
├── src/
│   ├── components/       # Reusable React components
│   │   ├── SqlEditor.tsx
│   │   ├── ResultTable.tsx
│   │   ├── MetadataTree.tsx
│   │   └── NaturalLanguageInput.tsx
│   ├── pages/           # Page components
│   │   ├── databases/
│   │   │   ├── list.tsx
│   │   │   ├── create.tsx
│   │   │   └── show.tsx
│   │   ├── queries/
│   │   │   └── execute.tsx
│   │   └── Home.tsx
│   ├── services/        # API client and data providers
│   │   ├── api.ts       # Axios instance
│   │   └── dataProvider.ts  # Refine data provider
│   ├── types/           # TypeScript type definitions
│   │   ├── database.ts
│   │   ├── metadata.ts
│   │   └── query.ts
│   ├── styles/          # Global styles
│   │   ├── index.css
│   │   └── design-tokens.css
│   ├── App.tsx          # Main application component
│   └── main.tsx         # Application entry point
├── public/              # Static assets
├── package.json
├── tsconfig.json        # TypeScript configuration
├── vite.config.ts       # Vite configuration
└── tailwind.config.js   # Tailwind CSS configuration
```

## Features

### Database Connection Management

- Add/edit/delete database connections
- Support for PostgreSQL and MySQL
- Connection status indicators
- Connection testing

### Metadata Browsing

- Tree view of database schemas, tables, and columns
- Column information (data type, nullable, primary key)
- Metadata refresh functionality
- Cached metadata display

### SQL Query Execution

- Monaco-based SQL editor with syntax highlighting
- Execute queries and view results in table format
- Query history panel
- Error handling and display
- Loading states

### Natural Language to SQL

- Tab-based interface (Manual SQL / Natural Language)
- Multi-language support (English and Chinese)
- Generate SQL from natural language prompts
- Edit generated SQL before execution
- Keyboard shortcuts (Cmd/Ctrl + Enter)

### Export Functionality

- Export query results to CSV
- Export query results to JSON
- Large dataset warnings (>10,000 rows)
- Client-side export (no server roundtrip)

## Styling

The application uses Tailwind CSS 4 with custom design tokens based on the MotherDuck design system:

- **Colors**: Sunbeam Yellow (#FFDE00), black borders (#000000)
- **Typography**: Uppercase labels, 0.04em letter spacing
- **Layout**: Three-column layout, card-based UI

## TypeScript

The project uses strict TypeScript configuration. All API responses are typed:

```typescript
// Example type definition
interface QueryResult {
  columns: QueryColumn[];
  rows: Record<string, any>[];
  rowCount: number;
  executionTimeMs: number;
  sql: string;
}
```

## API Integration

The frontend communicates with the backend via REST API:

- Base URL: Configured via `VITE_API_BASE_URL`
- All API responses use camelCase (handled automatically)
- Error handling with user-friendly messages
- Loading states for async operations

## Building for Production

```bash
npm run build
```

The production build will be in the `dist/` directory, ready to be served by any static file server.

### Preview Production Build

```bash
npm run preview
```

### Deploy

The `dist/` folder contains the static files. Deploy to any static hosting service:

- **Vercel**: Connect GitHub repo, set build command: `npm run build`
- **Netlify**: Connect GitHub repo, set publish directory: `dist`
- **Nginx**: Copy `dist/` contents to web root

## Testing

```bash
# Run tests in watch mode
npm test

# Run tests once
npm test -- --run
```

## Troubleshooting

### Build Errors

If you encounter build errors:

1. Clear node_modules and reinstall:
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```

2. Check Node.js version (requires 18+):
   ```bash
   node --version
   ```

### API Connection Issues

1. Verify backend server is running on `http://localhost:8000`
2. Check `VITE_API_BASE_URL` in `.env.local`
3. Verify CORS is enabled on backend (should allow all origins in dev)

### Monaco Editor Issues

If Monaco Editor fails to load:

1. Clear browser cache
2. Check browser console for errors
3. Verify `@monaco-editor/react` is installed

## Development Tips

### Hot Module Replacement (HMR)

Vite provides fast HMR. Changes to components will update instantly without page reload.

### Type Checking

Run TypeScript type checking:

```bash
npx tsc --noEmit
```

### Code Formatting

The project uses ESLint. Auto-fix issues:

```bash
npm run lint
```

## License

See root README for license information.

