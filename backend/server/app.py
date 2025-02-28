from datetime import datetime
from math import ceil
from typing import Dict, List, Optional, Tuple
from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn


from server.vector_db_weaviate import MemeDTO, VectorDBWeaviate

# Create a router
router = APIRouter()
db = VectorDBWeaviate()

class MemeResponse(BaseModel):
    id: str
    img_path: str
    description: str
    keywords: List[str]
    file_created_at: datetime
    meme_analyzed_at: Optional[datetime]

class PaginatedMemeResponse(BaseModel):
    results: List[MemeResponse]
    pages: int
    page: int


def convert_to_meme_response_dto(meme: MemeDTO) -> MemeResponse:
    return MemeResponse(
        id=meme.uuid,
        img_path=meme.img_path,
        description=meme.description,
        keywords=meme.keywords,
        file_created_at=meme.file_created_at,
        meme_analyzed_at=meme.meme_analyzed_at
    )

def paginate_db_results(results: List[MemeDTO], page_size: int, page:int) -> Tuple[List[MemeResponse],int]:
    """Provides paginated results for database response.

    Args:
        results (List[MemeDTO]): results
        page_size (int): page size
        pages (int): page to be returned

    Returns:
        Tuple[List[MemeDTO],int]: Tuple with single page of results (list of MemeResponses), total pages count.
    """
    results_length = len(results)
    page_size = max(1, min(100, page_size))
    pages_count = ceil(results_length/float(page_size))
    page = max(0, min(page, pages_count-1))
    page_start = page*page_size
    page_end = min(page_start + page_size + 1, results_length)
    paginated_results = list(map(convert_to_meme_response_dto, results[page_start:page_end]))

    return paginated_results, pages_count

@router.get("/memes", response_model=PaginatedMemeResponse)
def query_memes(query:str=None, page:int=0, page_size:int = 20):
    results = db.query(query) if query else db.get_all_memes()

    merged_paginated_results, pages_count = paginate_db_results(results,page_size, page)
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
    if not result:
        raise HTTPException(404, "Not Found")
    
    return result


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
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000, reload=True)