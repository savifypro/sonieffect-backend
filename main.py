import uvicorn

from core.branding.app_name import APP_NAME
from core.config.server_config import FINAL_IP, SERVER_PORT, SERVER_URL, create_app
from route_registory import register_all_routes

app = create_app()
register_all_routes(app)


if __name__ == "__main__":
    print(f"[!] INFO: Starting {APP_NAME} Server on {FINAL_IP}")
    print(f"[!] INFO: Access the API at {SERVER_URL}")
    uvicorn.run("main:app",
        host="0.0.0.0",
        port=SERVER_PORT,
        reload=True
    )
