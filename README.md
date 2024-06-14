# MemeSearch - meme semantic search engine

**Have you ever experienced an urge to immediately react to your friend's message with a great meme you saw but couldn't find it in
the depths of your gallery? MemeSearch has a solution!**


MemeSearch service allows you to semantically index a directory of your choice 
to provide a convinient way of looking for favourite memes.

The general overview of how it works:

1. A script scans recursively a directory of your choice and finds all allowed media types (.jpg, .png, .bmp right now). Job is periodic (every 10 mins by default) so even if you add something new to your catalog it'll queued and processed soon.
2. All new discovered files are stored in the database and scheduled for analysis.
3. One by one pictures are send to ChatGPT-4o to be analyzed i.e. described and keywords extracted.
4. Returned semantic description of a meme (a document) is transformed to embedding vector and stored in the database along with file metadata.
5. An application serves the files and allows for quick search of your memes by comparing the embedding vector of your query to memes' vectors stored in the database.
6. You can enjoy your memes server quickly!

### Tech stack
Backend + analyzer:
- python,
- fastapi

Database:
- ChromaDB for effcient embeddings vector storage

Frontend:
- Typescript + React + Tailwind + TanStack Query.

## How to run
For production build just set the following evnironmental variables: `MEME_DIRECTORY` pointing to your directory of choice, `OPENAI_API_KEY` an api key to OpenAI platform (you need access to ChatGPT-4o).

Run with `docker-compose up -d`

## Development
For the frontend development do:
```
docker-compose up -d
cd frontend
npm install
npm run start
```
Visit http://localhost:3000 , it should work fine with other services running from the docker.

---
### TODO:
1. Improve prompt
2. Show 
3. Logs from analyzer
4. filters
