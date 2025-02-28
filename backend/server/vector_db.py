from datetime import datetime
from typing import Dict, List, Optional
import chromadb

from globals import CHROMADB_HOST, CHROMADB_PORT, DB_PATH


class VectorDB:
    def __init__(
        self,
        db_path: Optional[str] = DB_PATH,
        chromadb_host: Optional[str] = CHROMADB_HOST,
        chromadb_port: Optional[int] = CHROMADB_PORT,
        collection_name: str = "memes",
    ):
        try:
            self.chroma_client = chromadb.HttpClient(
                host=chromadb_host, port=chromadb_port
            )
        except Exception:
            self.chroma_client = chromadb.PersistentClient(path=db_path)
        self.collection_name = collection_name
        self.collection = self.chroma_client.get_or_create_collection(
            self.collection_name
        )

    @staticmethod
    def create_metadata(
        keywords: List[str],
        file_created_at: str,
        exif_tags: Dict,
        analyzed: bool = False,
    ):
        return {
            "keywords": str(keywords),
            "file_created_at": file_created_at,
            "meme_analyzed_at": (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S") if analyzed else ""
            ),
            **exif_tags,
        }

    def add_meme(
        self,
        img_path: str,
        description: str,
        keywords: List[str],
        file_created_at: str,
        exif_tags: Dict,
        analyzed: bool = False,
    ):
        self.collection.upsert(
            documents=[description],
            metadatas=[
                VectorDB.create_metadata(keywords, file_created_at, exif_tags, analyzed)
            ],
            ids=[img_path],
        )

    def add_memes(
        self,
        img_paths: List[str],
        descriptions: List[str],
        keywords_list: List[List[str]],
        files_created_at: List[str],
        exif_tags_list: List[Dict],
        analyzed_list: List[bool],
    ):
        self.collection.upsert(
            documents=descriptions,
            metadatas=[
                VectorDB.create_metadata(keywords, file_created_at, exif_tags, analyzed)
                for (keywords, file_created_at, exif_tags, analyzed) in zip(
                    keywords_list, files_created_at, exif_tags_list, analyzed_list
                )
            ],
            ids=img_paths,
        )

    def query(self, query_text: str, n_results: int = 10):
        query_result = self.collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where={"meme_analyzed_at": {"$ne": ""}},
            # where={"metadata_field": "is_equal_to_this"},
            # where_document={"$contains":"search_string"}
            include=["metadatas", "documents"],
        )
        return query_result

    def get_all_memes(self):
        return self.collection.get()

    def get_total_memes_count(self) -> int:
        return self.collection.count()

    def get_meme_by_id(self, id: str) -> List[dict]:
        return self.collection.get(ids=[id], include=["metadatas"])

    def get_unanalyzed_memes(self) -> List[str]:
        return self.collection.get(where={"meme_analyzed_at": ""})["ids"]


if __name__ == "__main__":
    db = VectorDB()
    print(f"Memes in db: {db.get_total_memes_count()}")
    print(f"Unanalyzed memes in db: {len(db.get_unanalyzed_memes())}")

