import os

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
MEME_DIRECTORY=os.getenv("MEME_DIRECTORY")
ALLOWED_IMAGE_EXTENSIONS=[".jpg", ".jpeg", ".png", ".bmp"]
DB_PATH=os.getenv("DB_PATH")
CHROMADB_HOST=os.getenv("CHROMADB_HOST")
CHROMADB_PORT=os.getenv("CHROMADB_PORT")
ANALYZE_EVERY_N_MINUTES=int(os.getenv("ANALYZE_EVERY_N_MINUTES",10))

def get_os_meme_path(img_path: str) -> str:
    return f"{MEME_DIRECTORY}/{img_path}"