import hashlib
import os
from copy import copy
from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, Dict, Tuple

import chromadb


class CacheList(Enum):
    recruiter = "recruiter"


@dataclass
class RecruiterResponse:
    question: str
    answer: str

    @property
    def id(self):
        txt = f"Q: {self.question}\nA: {self.answer}"
        return hashlib.md5(txt.encode()).hexdigest()

    @property
    def metadata(self):
        return {"answer": self.answer}


class ResponseCache:
    @classmethod
    def new(cls, path: str = "./cache/resumate.db"):
        cls = copy(cls)
        if os.path.exists(path):
            cls.load()
            return cls

        cls.client = chromadb.PersistentClient(path=path)

        # create collections for different steps
        for cache_name in CacheList:
            cls.client.create_collection(
                name=cache_name.value, metadata={"hnsw:space": "cosine"}
            )

        return cls

    @classmethod
    def load(cls, path: str = "./cache/resumate.db"):
        cls.client = chromadb.PersistentClient(path=path)

    @classmethod
    def set_cache(cls, cache: CacheList):
        cls.collection = cls.client.get_collection(cache.value)

    @classmethod
    def cache_question(cls, r: RecruiterResponse):
        cls.collection.add(documents=[r.question], metadatas=[r.metadata], ids=[r.id])

    @staticmethod
    def parse_nearest(results) -> Tuple[str, float]:
        if results.get("distances") and results["distances"][0]:
            return results["metadatas"][0][0], results["distances"][0][0]

    @classmethod
    def threshold_query(cls, query: str, threshold: float = 0.25) -> Optional[str]:
        results = cls.collection.query(query_texts=[query], n_results=1)
        nearest_meta, nearest_dist = ResponseCache.parse_nearest(results)
        if nearest_dist < threshold:
            return nearest_meta.get("answer")
        else:
            return None
