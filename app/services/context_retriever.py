"""
Builds and queries a vectorstore from customer support articles using LangChain and OpenAI embeddings.

This module loads support content, splits it into semantically meaningful chunks, generates embeddings,
and stores them in a persistent Chroma vectorstore. It supports similarity-based retrieval to enhance
LLM responses with relevant context.
"""

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json
with open('data/kb/support_articles.json', 'r') as f:
    kb_articles = json.load(f)
documents = [f"Title: {a['title']}\nContent: {a['content']}" for a in kb_articles]
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = text_splitter.split_texts(documents)
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_texts(chunks, embeddings, persist_directory='./chroma_db')

def retrieve_context(query, k=3):
    """retrieve_context - TODO: Add description."""
    results = vectorstore.similarity_search(query, k=k)
    return '\n\n'.join([doc.page_content for doc in results])