import chromadb
from typing import List, Dict, Any

class VectorRepository:
    def __init__(self, client: chromadb.ClientAPI):
        self.client = client
        # 'company_rules'라는 이름의 저장소를 만듭니다 (없으면 생성, 있으면 가져오기)
        self.collection = self.client.get_or_create_collection(name="company_rules")

    def add_documents(self, documents: List[str], metadatas: List[Dict[str, Any]], ids: List[str]):
        # 데이터 저장 함수
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def query(self, query_text: str, n_results: int = 3) -> List[str]:
        # 데이터 검색 함수
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        # 검색 결과 중 텍스트만 뽑아서 반환
        return results["documents"][0] if results["documents"] else []