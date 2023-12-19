from tinydb import TinyDB, Query
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

db = TinyDB("data/all-texts.json")
mb_texts = db.search((Query().is_reaction == False) & (Query().sender == 'Mike Brode'))
mb_content = [m['content'] for m in mb_texts]
mb_content = [m for m in mb_content if 'nerdlegame' not in m]
mb_content = [m for m in mb_content if 'Worldle' not in m]
mb_content = [m for m in mb_content if 'Wordle' not in m]
mb_content = [m for m in mb_content if 'Heardle' not in m]
mb_content = [m for m in mb_content if 'sedecordle' not in m]
mb_content = [m for m in mb_content if 'Daily #' not in m]
mb_content = [m for m in mb_content if 'Quordle ' not in m]
mb_content = [m for m in mb_content if 'Beadle ' not in m]
mb_content = [m for m in mb_content if m != '']
mb_content = [m for m in mb_content if len(m) < 40]


# generate and store embeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2", cache_folder="/data/embeddings")
chroma_db = Chroma.from_texts(mb_content, embeddings, persist_directory="/data/chroma")
