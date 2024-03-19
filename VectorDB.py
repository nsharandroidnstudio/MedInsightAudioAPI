import chromadb
from chromadb.utils import embedding_functions

CHROMA_DATA_PATH = "chroma_data/"
COLLECTION_NAME = "conversation_collection"
MODEL_NAME = "all-MiniLM-L6-v2"
chromadb_client = chromadb.PersistentClient(path=CHROMA_DATA_PATH)
embedding_functions_client = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name= MODEL_NAME
        )
class VectorDB:
    def __init__(self):
        self.client = chromadb_client
        self.embedding_func = embedding_functions_client
        self.get_or_create_collection(COLLECTION_NAME)

    def get_or_create_collection(self, collection_name):       
        try:            
            self.collection = self.client.get_collection(name=collection_name)
        except Exception as e:            
            self.collection = self.client.create_collection(
                name=collection_name, embedding_function=self.embedding_func
            )

    def insert_document(self, conversation_id, text):        
        self.collection.add(
            documents=[text],
            ids=[conversation_id],
            metadatas=[{"hnsw:space": "cosine"}],
        )

    def find_similar_conversions(self, text, n_results=3):        
        query_results = self.collection.query(
            query_texts=[text],
            include=["documents", "distances"],
            n_results=n_results
        )
        result_subset = {
            "Similar tests": query_results.get("documents")[0][1:],
            "Most similar conversations ids": query_results.get("ids")[0][1:],
            "Conversations distances": query_results.get("distances")[0][1:]
        }

        return result_subset

    def get_text_by_conversation_id(self, conversation_id):       
        try:
            result = self.collection.get(ids=conversation_id)
            return result["documents"][0]
        except (IndexError, KeyError):           
            return None

    def clear_conversation(self):
        ids_to_delete = []
        self.collection.delete(ids=ids_to_delete)