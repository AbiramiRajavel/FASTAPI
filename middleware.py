from fastapi.middleware.cors import CORSMiddleware

def add_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],  # or ["*"] for all origins (not recommended for production)
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )