# app_name.py
#
# This module centralizes the application name for SoniEffect.
# By defining the app name in a single location:
# - All references throughout the codebase remain consistent
# - Updating the app name requires changing only this file
# - It simplifies logging, error messages, notifications, and UI references
#
# This avoids hardcoding the app name in multiple places,
# which reduces the risk of typos, inconsistencies, or maintenance issues.
#
# The value of APP_NAME should be treated as immutable at runtime
# unless there is a very specific reason to change it dynamically.

# APP_NAME is the canonical name of the application used in:
# - Logging messages
# - System notifications
# - UI displays
# - Error reports
# - Any other location where the app name must appear consistently
APP_NAME: str = "SoniEffect"

# End fo app_name.py
