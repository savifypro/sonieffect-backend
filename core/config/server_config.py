# server_config.py
# This is the main configuration file for the SoniEffect backend server.
# It handles environment detection, server URLs, ports, FastAPI initialization, and CORS setup.
# All lines are fully commented for clarity and maintainability.
# The configuration supports both local development and production deployment.

# Import standard Python modules
import os  # This module allows access to environment variables and system-level operations
import socket  # This module is used to retrieve the local machine's IP address dynamically

# Import FastAPI framework components
from fastapi import FastAPI  # FastAPI is a modern, fast, and asynchronous web framework for building APIs
from fastapi.middleware.cors import CORSMiddleware  # Middleware to allow cross-origin requests from frontend apps

# Import Uvicorn ASGI server
import uvicorn  # Uvicorn is a lightning-fast ASGI server to run FastAPI applications

# Local development configuration
# These settings are only used when running the backend on a developer's local machine
# This allows testing the backend before deploying it to production

LOCAL_PROTOCOL = "http"  # Protocol for local development. HTTP is sufficient for testing
LOCAL_IP = socket.gethostbyname(socket.gethostname())  
# Dynamically retrieves the local machine's IP address so developers do not need to hardcode it
LOCAL_PORT = 5000  # Port number to run the server locally. Can be any free port on your machine

# Production server configuration
# These settings are used when deploying the backend to a live server
# The production server should be accessible over HTTPS with a public domain name

PRODUCTION_PROTOCOL = "https"  # Production should always use HTTPS to ensure encrypted communication
PRODUCTION_SUBDOMAIN = "sonieffect"  # Subdomain for the API, e.g., sonieffect.onrender.com
PRODUCTION_DOMAIN = "onrender"  # Main domain for the production server
PRODUCTION_EXTENSION = "com"  # Top-level domain for the production server

# Construct a URL for local development
FINAL_IP = f"{LOCAL_PROTOCOL}://{LOCAL_IP}:{LOCAL_PORT}"  
# This represents the full URL for the local server
# Example output: http://192.168.1.10:5000
# Can be used for logging or referencing the local server in scripts

# Determine which environment the server is running in
# Reads the SERVER_ENV environment variable from the operating system
# If not set, defaults to "production" to prevent accidental local exposure
ENVIRONMENT = os.getenv("SERVER_ENV", "production").lower().strip()  
# Converts the value to lowercase and removes leading/trailing whitespace
# This ensures that values like " Local " or "PRODUCTION" are normalized

# Conditional server configuration based on environment
# Sets the host, port, and full server URL depending on whether we are running locally or in production

if ENVIRONMENT == "local":
    # Configuration for local development environment
    SERVER_HOST = LOCAL_IP  # The server will bind to the local machine's IP address
    SERVER_PORT = LOCAL_PORT  # The server will run on the local port defined above
    SERVER_URL = f"{LOCAL_PROTOCOL}://{LOCAL_IP}:{LOCAL_PORT}"  
    # Full URL for local testing
    # Can be printed to console or used in local frontend apps
else:
    # Configuration for production environment
    SERVER_HOST = "0.0.0.0"  
    # 0.0.0.0 allows the server to listen on all network interfaces
    SERVER_PORT = 5000  # Default production port. Can be changed if the hosting provider requires it
    SERVER_URL = f"{PRODUCTION_PROTOCOL}://{PRODUCTION_SUBDOMAIN}.{PRODUCTION_DOMAIN}.{PRODUCTION_EXTENSION}"  
    # Full URL for production API
    # Example: https://sonieffect.onrender.com

# Function to create and configure the FastAPI application
# This includes setting metadata for API documentation and adding middleware
def create_app():
    # Initialize the FastAPI application with title, description, and version
    app = FastAPI(
        title="SoniEffect Server",  # Name displayed in the automatically generated API docs
        description="FastAPI backend for SoniEffect mobile app",  # Description for API documentation
        version="1.0.0"  # Backend version
    )

    # Add Cross-Origin Resource Sharing (CORS) middleware
    # This allows frontend applications to communicate with this backend securely
    # It is especially important for mobile apps or web dashboards that run on different origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  
        # Allow requests from any origin. For production, this can be restricted to trusted domains
        allow_credentials=True,  
        # Allows sending cookies and authentication credentials in requests
        allow_methods=["*"],  
        # Allows all HTTP methods such as GET, POST, PUT, DELETE, PATCH
        allow_headers=["*"],  
        # Allows all HTTP headers in requests
    )

    return app  # Return the configured FastAPI application instance

# This block runs only when executing this script directly
# It creates the FastAPI app and starts the Uvicorn server
if __name__ == "__main__":
    # Print the current environment and server configuration for debugging
    print(f"[CONFIG] Environment: {ENVIRONMENT}")  
    # Prints whether the server is running in local or production mode
    print(f"[CONFIG] SERVER_URL: {SERVER_URL}")  
    # Prints the full server URL for logs or frontend reference
    print(f"[CONFIG] FINAL_IP: {FINAL_IP}")  
    # Prints local development URL
    print(f"[CONFIG] HOST: {SERVER_HOST}, PORT: {SERVER_PORT}")  
    # Prints host and port that the server is bound to

    # Create the FastAPI app instance
    app = create_app()  

    # Start the FastAPI application using Uvicorn ASGI server
    # Host and port are determined by the environment configuration
    uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT)  
