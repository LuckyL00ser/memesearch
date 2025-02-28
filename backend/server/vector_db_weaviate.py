from datetime import datetime
import logging
from typing import List, Optional
from uuid import UUID
from zoneinfo import ZoneInfo
import weaviate
import weaviate.classes as wvc
from weaviate.classes.query import Filter
from weaviate.util import generate_uuid5
from globals import WEAVIATE_HOST, WEAVIATE_PORT
from pydantic import BaseModel, Field
import time


class MemeDTO(BaseModel):
    img_path: str
    description: str
    keywords: List[str]
    file_created_at: datetime
    # exif_tags: Dict
    analyzed: bool = False
    meme_analyzed_at: Optional[datetime] = None

    @property
    def uuid(self):
        return generate_uuid5(self.img_path)
    
    def model_dump(self, *args, **kwargs):
        #override pydantic model_dump to include timezone and avoid Weaviate errors
        local_tz = ZoneInfo(time.tzname[0]) 
        data = super().model_dump(*args, **kwargs)
        if self.file_created_at:
            data['file_created_at'] = self.file_created_at.astimezone(local_tz)
        if self.meme_analyzed_at:
            data['meme_analyzed_at'] = self.meme_analyzed_at.astimezone(local_tz)
        return data


class VectorDBWeaviate:
    def __init__(
        self,
        weaviate_host: Optional[str] = WEAVIATE_HOST,
        weaviate_port: Optional[int] = WEAVIATE_PORT,
        collection_name: str = "memes",
    ):
        self.client = weaviate.connect_to_local(host=weaviate_host, port=weaviate_port)
        self.collection_name = collection_name
        self._create_schema()

    def _create_schema(self):
        properties = [
            wvc.config.Property(
                name="img_path",
                data_type=wvc.config.DataType.TEXT,
                skip_vectorization=True,
            ),
            wvc.config.Property(name="description", data_type=wvc.config.DataType.TEXT),
            wvc.config.Property(
                name="keywords", data_type=wvc.config.DataType.TEXT_ARRAY
            ),
            wvc.config.Property(
                name="file_created_at",
                data_type=wvc.config.DataType.DATE,
                skip_vectorization=True,
            ),
            wvc.config.Property(
                name="meme_analyzed_at",
                data_type=wvc.config.DataType.DATE,
                skip_vectorization=True,
            ),
            # wvc.config.Property(
            #     name="exif_tags",
            #     data_type=wvc.config.DataType.OBJECT,
            #     skip_vectorization=True
            # )
        ]

        if not self.client.collections.exists(self.collection_name):
            logging.info(f"Creating new collection - {self.collection_name}.")
            self.client.collections.create(
                name=self.collection_name,
                vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_transformers(),
                properties=properties,
                inverted_index_config=wvc.config.Configure.inverted_index(
                    index_null_state=True
                ),
            )
    
    @staticmethod
    def _queried_meme_to_dto(meme) -> MemeDTO:
        return MemeDTO(
            **{
                **meme.properties,
                'analyzed': meme.properties['meme_analyzed_at'] is not None
            }    
        )

    def get_collection(self):
        return self.client.collections.get(self.collection_name)

    def add_meme(self, meme_dto: MemeDTO) -> UUID:
        collection = self.get_collection()
        properties = meme_dto.model_dump()

        uuid = collection.data.insert(
            properties=properties, uuid=meme_dto.uuid
        )
        return uuid

    def add_memes(self, memes: List[MemeDTO]):
        for meme in memes:
            self.add_meme(meme)

    def query(self, query_text: str, n_results: int = 10) -> List[MemeDTO]:
        collection = self.get_collection()
        result = collection.query.hybrid(
            query=query_text,
            query_properties=["description", "keywords"],
            filters=Filter.by_property("meme_analyzed_at").is_none(False),
            alpha=0.5,
            limit=n_results,
        ).objects

        return list(map(VectorDBWeaviate._queried_meme_to_dto, result))

    def get_all_memes(self) -> List[MemeDTO]:
        memes = self.get_collection().query.fetch_objects(include_vector=True, limit=1000).objects
        return list(map(VectorDBWeaviate._queried_meme_to_dto, memes))

    def get_total_memes_count(self) -> int:
        return len(self.get_collection())

    def get_meme_by_id(self, id: str) -> Optional[MemeDTO]:
        meme = self.get_collection().query.fetch_object_by_id(uuid=id)
        if meme:
            return VectorDBWeaviate._queried_meme_to_dto(meme)
        return None

    def delete_meme_by_id(self, id: str) -> bool:
        return self.get_collection().data.delete_by_id(uuid=id)

    def update_meme(self, img_path: str, description: str, keywords: List[str]):
        collection = self.get_collection()
        uuid = generate_uuid5(img_path)
        collection.data.update(
            uuid=uuid, properties={"description": description, "keywords": keywords, "meme_analyzed_at": datetime.now()}
        )

    def get_unanalyzed_memes(self) -> List[MemeDTO]:
        collection = self.get_collection()
        result = collection.query.fetch_objects(
            filters=Filter.by_property("meme_analyzed_at").is_none(True), limit=1000
        )
        return list(map(VectorDBWeaviate._queried_meme_to_dto, result.objects))


if __name__ == "__main__":
    db = VectorDBWeaviate()
    # db.client.collections.delete(db.collection_name)

    # print(f"Memes in db: {db.get_total_memes_count()}")
    # print(f"Unanalyzed memes in db: {len(db.get_unanalyzed_memes())}")
    # db.add_meme(MemeDTO(img_path="test.jpg", description="test", keywords=["test"], file_created_at=datetime.now()))
    memes = db.get_all_memes()
    pass
