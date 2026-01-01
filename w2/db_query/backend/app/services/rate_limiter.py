"""Rate limiting service for API endpoints."""

import time
from collections import defaultdict
from typing import Dict, Tuple
from fastapi import HTTPException, status


class RateLimiter:
    """Simple in-memory rate limiter using sliding window algorithm.
    
    This rate limiter tracks request counts per identifier (e.g., IP address)
    within a time window. Once the limit is reached, subsequent requests
    are blocked until the window resets.
    """

    def __init__(
        self,
        max_requests: int = 10,
        window_seconds: int = 60,
    ):
        """Initialize rate limiter.
        
        Args:
            max_requests: Maximum number of requests allowed per window
            window_seconds: Time window in seconds
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        # Store request timestamps per identifier
        self.requests: Dict[str, list[float]] = defaultdict(list)

    def is_allowed(self, identifier: str) -> Tuple[bool, int]:
        """Check if request is allowed.
        
        Args:
            identifier: Unique identifier (e.g., IP address)
            
        Returns:
            Tuple of (is_allowed, remaining_requests)
        """
        now = time.time()
        window_start = now - self.window_seconds
        
        # Get requests for this identifier
        request_times = self.requests[identifier]
        
        # Remove requests outside the window
        request_times[:] = [t for t in request_times if t > window_start]
        
        # Check if limit exceeded
        if len(request_times) >= self.max_requests:
            # Calculate when next request will be allowed
            oldest_request = min(request_times) if request_times else now
            reset_time = oldest_request + self.window_seconds
            remaining = int(reset_time - now)
            return False, remaining
        
        # Add current request
        request_times.append(now)
        
        # Calculate remaining requests
        remaining = self.max_requests - len(request_times)
        return True, remaining

    def get_remaining(self, identifier: str) -> int:
        """Get remaining requests for identifier.
        
        Args:
            identifier: Unique identifier
            
        Returns:
            Number of remaining requests
        """
        now = time.time()
        window_start = now - self.window_seconds
        
        request_times = self.requests[identifier]
        request_times[:] = [t for t in request_times if t > window_start]
        
        return max(0, self.max_requests - len(request_times))


# Global rate limiter instance for LLM endpoint
# Default: 10 requests per 60 seconds per client
# Note: Settings are accessed lazily to avoid circular import
llm_rate_limiter: RateLimiter | None = None


def get_llm_rate_limiter() -> RateLimiter:
    """Get or create LLM rate limiter instance."""
    global llm_rate_limiter
    if llm_rate_limiter is None:
        from app.config import settings
        llm_rate_limiter = RateLimiter(
            max_requests=settings.llm_rate_limit_max_requests,
            window_seconds=settings.llm_rate_limit_window_seconds,
        )
    return llm_rate_limiter


def check_rate_limit(identifier: str) -> None:
    """Check rate limit and raise exception if exceeded.
    
    Args:
        identifier: Client identifier (e.g., IP address)
        
    Raises:
        HTTPException: If rate limit exceeded
    """
    limiter = get_llm_rate_limiter()
    allowed, retry_after = limiter.is_allowed(identifier)
    
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Please try again in {retry_after} seconds.",
            headers={"Retry-After": str(retry_after)},
        )

