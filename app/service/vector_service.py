import json
import uuid
from app.repository.vector_repo import VectorRepository

class VectorService:
    def __init__(self, vector_repo: VectorRepository):
        self.vector_repo = vector_repo

    def save_documents(self, file_path: str = "rules.json"):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        documents = []
        metadatas = []
        ids = []

        for item in data:
            documents.append(item["content"])
            metadatas.append(item["metadata"])
            ids.append(str(uuid.uuid4())) # 고유 ID 생성

        #DB에 저장
        self.vector_repo.add_documents(documents, metadatas, ids)
        return {"status": "success", "count": len(documents)}

    def search(self, query: str):
        return self.vector_repo.query(query)