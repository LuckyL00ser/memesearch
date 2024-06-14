#!/bin/sh
#!/bin/sh
docker exec -it memesearch_chromadb_1 python -c "
import chromadb
client = chromadb.HttpClient(host='localhost', port=8000)
collection = client.get_collection('memes')
print(collection.count())
"
