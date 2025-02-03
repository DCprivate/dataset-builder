# Software/DataHarvester/to-do.md

High Priority Tasks:
-------------------
1. Error Handling
   - Consolidate into single, flexible system
   - Standardize across codebase

2. Database Operations
   - Standardize on either sync or async operations
   - Implement proper configuration caching

3. Validation & Configuration
   - Unify validation framework
   - Create unified config validation system
   - Centralize logging configuration

4. Infrastructure
   - Centralize health checks
   - Create shared utility functions
   - Standardize resource cleanup patterns

5. Logging
   - Centralize logging configuration
   - Create shared utility functions
   - Standardize resource cleanup patterns

6. merge in the subscraper functionality into the data ingestion pipeline.
   - Add support for youtube, reddit, and other sources.

# snippets of code to use elsewhere:

from src.infrastructure.error_handling.middleware.error_middleware import ErrorMiddleware

@ErrorMiddleware.rate_limit
@ErrorMiddleware.catch_errors(context="YouTube API")
def fetch_video_data():
    # Your code here
    pass

@ErrorMiddleware.retry(retries=3, context="YouTube API")
def fetch_subtitles():
    # Your code here
    pass

# Or combine rate limiting and retry:
@ErrorMiddleware.with_retry_and_rate_limit(context="YouTube API")
def fetch_video_data():
    # Your code here
    pass    