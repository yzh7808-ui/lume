# Lume

Lume is an MVP for a personal thought organizer and AI reflection agent.

It helps users:
- capture daily notes, reflections, and brainstorms
- extract themes, mood, and keywords from entries
- store semantic memory in Qdrant
- search for related ideas across time
- generate weekly summaries and reflection prompts

## Stack
- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Qdrant
- SentenceTransformers

## Project goals
- low-friction journaling
- semantic recall of old ideas
- theme clustering over time
- better weekly reflection and insight generation

## Quick start

1. Copy environment variables:
   ```bash
   cp .env.example .env
   ```

2. Start infrastructure:
   ```bash
   docker-compose up -d
   ```

3. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

4. Run the app:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. Visit the API docs:
   - http://localhost:8000/docs

## Example request

```bash
curl -X POST "http://localhost:8000/api/v1/notes" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "u_001",
    "title": "About growth",
    "content": "I realized that real growth is not doing more, but reducing what is meaningless.",
    "source": "text",
    "category": "reflection",
    "mood": "calm",
    "importance": 0.9,
    "tags": ["growth", "work", "life"]
  }'
```

## Notes
This is an MVP skeleton intended for experimentation, learning, and product prototyping.
The architecture is designed to be extended with:
- weekly reflection summaries
- theme clustering
- personal knowledge graph ideas
- richer AI prompts and embeddings
- frontend interface and mobile app

## License
MIT
