# AI Career Coach

An AI-powered career coaching app to help you improve your CV and prepare for job interviews.

**Live app:** [AI career coach](https://yourcareercoach.vercel.app/)

## Features

- **CV Reviewer:** Paste your CV or upload a PDF, choose a target role, and optionally add a job description. Get scored, actionable feedback across five areas.
- **Track CV improvements:** Save your five most recent reviews in your browser, compare reviews for the same role, and download feedback as a PDF.
- **Interview Practice:** Choose between a full role-specific mock interview with personalized feedback or practicing one question with AI-generated prompts and STAR-based answer coaching.

## Project structure

```text
.
├── app/                    # FastAPI backend
│   ├── routers/            # CV review, interview, and answer coach routes
│   ├── schemas/            # API request and response models
│   ├── services/           # AI, CV review, interview, and PDF logic
│   ├── config.py           # Environment-based settings
│   └── main.py             # FastAPI app entry point
├── frontend/               # Vue 3 + Vite frontend
│   ├── public/
│   │   └── image.png        # Hero illustration
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

   The backend also supports `OPENAI_MODEL` (defaults to `gpt-6-luna`), `MAX_CV_CHARS` (defaults to `15000`), and `MAX_FILE_MB` (defaults to `4`).

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

## Deploy to Vercel

Deploy the backend and frontend as **two separate Vercel projects** from this repository.

### Backend project

1. Import the repository as a Vercel project with the repository root (`.`) as its **Root Directory**.
2. Configure `OPENAI_API_KEY`. Set `FRONTEND_ORIGIN` to the deployed frontend's origin, with no trailing slash (for example, `https://your-frontend.vercel.app`).
3. Deploy the backend and verify `https://your-backend.vercel.app/api/health` returns `{"status":"ok"}`.

### Frontend project

1. Import the same repository as a second Vercel project and set **Root Directory** to `frontend`.
2. Use the Vite framework preset with build command `npm run build` and output directory `dist`.
3. Set `VITE_API_BASE_URL` to the backend's origin, with no trailing slash (for example, `https://your-backend.vercel.app`), then deploy.

Vite embeds `VITE_API_BASE_URL` during the frontend build, so redeploy the frontend after changing it. If using a frontend preview on a different origin, update the backend's `FRONTEND_ORIGIN` to that exact origin and redeploy the backend.

## API endpoints

- `GET /api/health` — backend health check
- `POST /api/cv/review` — review pasted CV text or an uploaded PDF
- `POST /api/interview/start` — start a mock interview
- `POST /api/interview/answer` — submit an answer and get the next question
- `POST /api/interview/feedback` — get feedback on an interview
- `POST /api/coach/question` — generate a role- and theme-specific practice question
- `POST /api/coach/analyze` — evaluate a draft answer using the STAR method
- `GET /api/coach/categories` — list available question themes
