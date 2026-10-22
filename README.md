# AI Career Coach

An AI-powered career coaching app to help you improve your CV and prepare for job interviews.

**Live app:** [AI career coach](https://yourcareercoach.vercel.app/)

## Features

- **CV Reviewer:** Paste your CV or upload a PDF, choose a target role, and optionally add a job description. Get scored, actionable feedback across five areas.
- **Track CV improvements:** Save your five most recent reviews in your browser, compare reviews for the same role, and download feedback as a PDF.
- **Mock Interview:** Practice a role-specific interview, optionally tailored to a job description. Choose the interview length, answer questions in a chat, and receive a score and personalized feedback.

## Project structure

```text
.
├── app/                    # FastAPI backend
│   ├── routers/            # CV review and interview API routes
│   ├── schemas/            # Request and response models
│   ├── services/           # AI, CV review, interview, and PDF logic
│   ├── config.py           # Environment-based settings
│   └── main.py             # FastAPI app entry point
├── frontend/               # Vue 3 + Vite frontend
│   └── src/
│       ├── components/     # CV reviewer and mock interview UI
│       ├── api.js          # Backend API client
│       └── App.vue         # Main app and navigation
├── requirements.txt        # Python dependencies
└── README.md
```

## Tech stack

- Frontend: Vue 3 and Vite
- Backend: Python, FastAPI, and the OpenAI API

## Run locally

You'll need Python 3.10 or newer, Node.js with npm, and an OpenAI API key.

1. Install the backend dependencies from the repository root:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

   On Windows, activate the virtual environment with `.venv\Scripts\activate`.

2. Create a `.env` file in the repository root:

   ```env
   OPENAI_API_KEY=your_openai_api_key
   ```

3. Start the backend from the repository root:

   ```bash
   uvicorn app.main:app --reload
   ```

   The API runs at `http://localhost:8000`. Check that it is available at `http://localhost:8000/api/health`.

4. In a separate terminal, install and start the frontend:

   ```bash
   cd frontend
   npm install
   npm run dev
   ```

   Open the local URL printed by Vite. During development, Vite proxies `/api` requests to the backend at `http://localhost:8000`.

## API endpoints

- `GET /api/health` — backend health check
- `POST /api/cv/review` — review pasted CV text or a PDF
- `POST /api/interview/start` — start a mock interview
- `POST /api/interview/answer` — submit an answer and get the next question
- `POST /api/interview/feedback` — get feedback on an interview
