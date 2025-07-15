
from llama_index.readers.database import DatabaseReader
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.core import VectorStoreIndex, Settings, StorageContext
from llama_index.embeddings.openai import OpenAIEmbedding
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore

import os
os.environ["OPENAI_API_KEY"] = "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"

reader = DatabaseReader(
    uri="mysql+pymysql://root:sinha1998@localhost:3306/testdb?charset=utf8",
)

query = "SELECT * FROM users"
documents = reader.load_data(query=query)
print(documents)

# initialize client, setting path to save data
db = chromadb.PersistentClient(path="./chroma_db")

# create collection
chroma_collection = db.get_or_create_collection("quickstart")

# assign chroma as the vector_store to the context
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# create your index
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)

# create a query engine and query
query_engine = index.as_query_engine()
response = query_engine.query("what is the email of user_id 2?")
print(response)

# global default
#Settings.embed_model = OpenAIEmbedding()

#pipeline = IngestionPipeline(transformations=[TokenTextSplitter(), ...])

#nodes = pipeline.run(documents=documents)
#index = VectorStoreIndex(nodes)
#index = VectorStoreIndex.from_documents(documents)
#print(index)