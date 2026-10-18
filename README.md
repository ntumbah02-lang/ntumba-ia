# ntumba IA - Chat MVP

J'ai ajouté une implémentation MVP qui transforme ntumba IA en un assistant de type ChatGPT : backend FastAPI + frontend web simple, stockage SQLite pour l'historique, adaptateur OpenAI prêt à l'emploi.

Commandes pour exécuter en local :

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# ajoutez votre clé OPENAI_API_KEY dans .env
uvicorn server.main:app --reload --host 0.0.0.0 --port 8000
# puis ouvrez http://localhost:8000
```

API principale :
- POST /api/chat  -> {"message": "bonjour", "session_id": "optional"} -> {"reply": "...", "session_id": "..."}

Notes :
- L'interface web est en français.
- Aucune clé API n'a été committée. Mettez OPENAI_API_KEY dans .env avant d'appeler l'API.
- Pour ajouter Anthropic/Claude plus tard, j'ai prévu un adaptateur; demandez et je l'active.

Licence: MIT
