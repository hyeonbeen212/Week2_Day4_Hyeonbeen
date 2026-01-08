import os
import chromadb
from chromadb import Settings

def get_db_client():
    #환경변수에서 주소를 가져오되 없으면 로컬호스트로 설정
    chroma_host = os.getenv("CHROMA_HOST", "localhost")
    chroma_port = os.getenv("CHROMA_PORT", "8000")
    
    #DB 접속
    client = chromadb.HttpClient(
        host=chroma_host,
        port=int(chroma_port),
        settings=Settings(allow_reset=True, anonymized_telemetry=False)
    )
    return client