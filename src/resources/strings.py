# Add standardized error messages
ERR_NOT_FOUND = "Resource not found: {resource}"
ERR_BAD_REQUEST = "Invalid request: {details}"
ERR_UNAUTHORIZED = "Authentication required"
ERR_FORBIDDEN = "Access forbidden"

# Add logging messages
LOG_APP_STARTUP = "Application starting up"
LOG_REQUEST_RECEIVED = "Request received: {method} {path}"
LOG_ERROR_OCCURRED = "Error occurred: {error_type} - {message}"

# Error messages
ERR_PARCEL_CREATE = "Error registering parcel: {error}"
ERR_PARCEL_TYPES = "Error retrieving parcel types: {error}"
ERR_PARCEL_LIST = "Error retrieving parcels list: {error}"
ERR_PARCEL_NOT_FOUND = "Parcel with ID={parcel_id} not found"
ERR_PARCEL_RETRIEVING = "Error retrieving parcel with ID={parcel_id}: {error}"
ERR_INVALID_TASK = "Invalid task name. Use 'currency', 'shipping', or 'all'"
ERR_CURRENCY_FETCH = "Failed to fetch currency data: {status_code}"
ERR_CURRENCY_PARSE = "Failed to parse currency data: {error}"
ERR_SHIPPING_CALC = "Error handling shipping cost: {error}"
ERR_STARTUP_FAILED = "Startup failed: {error}"
ERR_VALIDATION = "Validation error occurred."
ERR_RETRY_ATTEMPT = "Error in {func_name}. Attempt {retries}/{max_retries}. Error: {error}"
ERR_MAX_RETRIES = "Max retries reached for {func_name}."

# Log messages
LOG_PARCEL_CREATED = "Parcel registered successfully with ID={id}"
LOG_PARCEL_LISTED = "Retrieved {count} parcels for user {user_id}"
LOG_DEBUG_EVENT_START = "Running debug event: {event}"
LOG_DEBUG_EVENT_COMPLETE = "Debug event '{event}' completed successfully"
LOG_DEBUG_FETCH_CURRENCY = "Running currency fetch task"
LOG_DEBUG_SHIPPING_COST = "Running shipping cost calculation task"
LOG_CURRENCY_UPDATE = "Currency data updated"
LOG_SHIPPING_UPDATE = "Updated {count} parcels with calculated shipping costs"
LOG_NO_UNREGISTERED_PARCELS = "No unregistered parcels found"
LOG_RETRY = "Retrying in {delay} seconds..."

# Warning messages
WARN_REDIS_NOT_FOUND = "Currency data not found in Redis"
WARN_INVALID_CURRENCY_DATA = "Invalid currency data"
