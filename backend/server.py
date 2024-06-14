from math import ceil
from typing import Dict, List, Tuple
from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn


from vector_db import VectorDB

# Create a router
router = APIRouter()
db = VectorDB()

class PaginatedMemeResponse(BaseModel):
    results: List[Dict]
    pages: int
    page: int

def paginate_chroma_db_results(results: List, page_size: int, page:int) -> Tuple[List[str],List[Dict],int]:
    """Provides paginated results for from chromadb's `collection.query()/collection.get()`.

    Args:
        results (List): chromadb's results
        page_size (int): page size
        pages (int): page to be returned

    Returns:
        Tuple[List[Dict],List[str]]: Tuple with single page of results (list of Dicts), total pages count.
    """
    results_length = len(results["ids"])
    page_size = max(1, min(100, page_size))
    pages_count = ceil(results_length/float(page_size))
    page = max(0, min(page, pages_count-1))
    page_start = page*page_size
    page_end = min(page_start + page_size + 1, results_length)
    paginated_ids = results["ids"][page_start:page_end]
    paginated_metadatas = results["metadatas"][page_start:page_end]
    #merge two lists
    merged_paginated_results = [
        {"id": doc_id, **metadata}
        for doc_id, metadata in zip(paginated_ids, paginated_metadatas)
    ]
    return merged_paginated_results, pages_count

@router.get("/memes", response_model=PaginatedMemeResponse)
def query_memes(query:str=None, page:int=0, page_size:int = 20):
    results = db.query(query) if query else db.get_all_memes()
    results = {"ids": results["ids"][0], "metadatas": results["metadatas"][0]} if query else results

    merged_paginated_results, pages_count = paginate_chroma_db_results(results,page_size, page)
    return PaginatedMemeResponse(results=merged_paginated_results, pages=pages_count, page=page)


@router.get("/memes/collection-status")
def get_status():
    unanalyzed = len(db.get_unanalyzed_memes())
    total = db.get_total_memes_count()
    return {
        "total_count": total,
        "unanalyzed_count": unanalyzed,
        "analyzed_count": total - unanalyzed,
        "progress": (total - unanalyzed)/total if total != 0 else 0
    }

@router.get("/memes/{meme_id}")
def get_meme(meme_id):
    result = db.get_meme_by_id(meme_id)
    if not len(result["ids"]):
        raise HTTPException(404, "Not Found")
    return {
        "id": result["ids"][0],
        **result["metadatas"][0]
    }


app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)