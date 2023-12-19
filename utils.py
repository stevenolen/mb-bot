from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings


class Datastore:
    def __init__(self,
                 persist_directory="data/chroma",
                 cache_directory="data/embeddings",
                 embedding_model="all-MiniLM-L6-v2"):
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model, cache_folder=cache_directory)
        self.db = Chroma(embedding_function=self.embeddings, persist_directory=persist_directory)

    def search(self, text, k=10):
        return self.db.similarity_search(text, include_metadata=False, k=k)
