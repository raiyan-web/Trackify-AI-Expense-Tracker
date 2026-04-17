# Trackify-AI-Expense-Tracker

AI-powered receipt and expense tracker.

## Stack

- Frontend: React + TailwindCSS
- Backend: FastAPI + PostgreSQL
- AI: Claude / Anthropics image + text extraction
- Auth: JWT
- Storage: local uploads (can be extended to AWS S3)

## Getting started

1. Copy `.env.example` to `.env` and set your values.
2. Start PostgreSQL locally or with Docker.
3. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the backend:
   ```bash
   uvicorn backend.main:app --reload
   ```
5. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## API endpoints

- `POST /auth/signup`
- `POST /auth/login`
- `POST /receipts/upload`
- `GET /receipts/`
- `GET /expenses/`
- `GET /reports/monthly?month=1&year=2025`

## Notes

- Set `ANTHROPIC_API_KEY` in `.env` to enable Claude extraction.
- Use `DATABASE_URL` to point to PostgreSQL.
- `docker-compose.yml` includes a local Postgres service.
