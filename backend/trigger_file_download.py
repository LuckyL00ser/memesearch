import chromadb

if __name__ == "__main__":
    #this will trigger download of LLM models during Dockerfile build to store them in the image
    client = chromadb.Client()
    collection = client.get_or_create_collection('memes')
    collection.add(ids=['test'],documents=["meme"], metadatas=[{"x": 0}])
    collection.query(query_texts=["meme"])