import chromadb
from chromadb.utils import embedding_functions


class VectorDB:
    def __init__(self, persist_directory, model_name, collection_name):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=model_name
        )
        self.collection = self.client.get_collection(
            name=collection_name,
            embedding_function=self.embedding_func,
        )

    def insert_document(self, conversation_id, text):
        """
        Inserts a new document with metadata into the ChromaDB collection.

        Args:

            conversation_id: Unique identifier for the conversation.

        Returns:
            None
            :param text:
            :param conversation_id:
        """
        self.collection.add(
            documents=[text],
            ids=[conversation_id],
            metadatas=[{"hnsw:space": "cosine"}],
        )

    def find_similar_conversions(self, text, n_results=100):
        """
        Finds similar vectors in the ChromaDB collection using a query vector.

        Args:
            n_results: Number of similar vectors to retrieve (default is 5).

        Returns:
            List of dictionaries containing similar vectors and their distances.
            :param n_results:
            :param text:
        """
        query_results = self.collection.query(
            query_texts=[text],
            include=["documents", "distances"],
            n_results=n_results
        )
        result_subset = {
            "ids": query_results.get("ids")[0][1:],
            "distances": query_results.get("distances")[0][1:]
        }

        return result_subset

    def get_text_by_conversation_id(self, conversation_id):
        """
        Retrieves the vector associated with a conversation_id from the ChromaDB collection.

        Args:
            conversation_id: The conversation_id for which to retrieve the vector.

        Returns:
            The vector associated with the conversation_id or -1 if not found.
        """
        try:
            result = self.collection.get(ids=conversation_id)
            return result["documents"][0]
        except (IndexError, KeyError):
            # Conversation_id not found in the collection or conversation_vector key not present
            return None

    def clear_conversation(self, id):
        ids_to_delete = [id]
        self.collection.delete(ids=ids_to_delete)
