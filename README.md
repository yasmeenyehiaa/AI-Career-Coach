# AI Career Coach

AI Career Coach is a full-stack app for improving CVs and practicing interviews with AI guidance. It combines a FastAPI backend with a Vue 3 frontend so users can review a CV, run mock interviews, and sharpen interview answers using structured feedback.

**Live app:** [AI career coach](https://yourcareercoach.vercel.app/)

## Features

- **CV reviewer:** paste CV text or upload a PDF, choose a target role, and optionally include a job description. The backend scores the CV and returns actionable feedback across key areas.
- **CV history and PDF export:** the frontend keeps the last five review results in-browser, lets users compare reviews for the same role, and downloads the latest feedback as a PDF.
- **Interview practice:** run a full role-specific mock interview, then receive a summary of strengths and gaps.
- **Answer coach:** generate a random behavioral question, optionally filtered by role and theme, and analyze a draft answer using the STAR method with guided improvement prompts.

## Project structure

```text
.
├── app/                            # FastAPI backend
│   ├── routers/                    # CV, interview, and coach API routes
│   │   ├── cv.py
│   │   ├── interview.py
│   │   └── coach.py
│   ├── schemas/                   # Request/response models
│   │   ├── cv.py
│   │   ├── interview.py
│   │   └── coach.py
│   ├── services/                  # LLM, CV scoring, interview logic, and PDF parsing
│   │   ├── cv_review.py
│   │   ├── interview.py
│   │   ├── coach.py
│   │   ├── llm.py
│   │   ├── pdf_parser.py
│   │   └── prompts.py
│   ├── config.py                  # Environment settings and .env loading
│   ├── main.py                    # FastAPI entry point and CORS config
│   └── __init__.py
├── frontend/                      # Vue 3 + Vite frontend
│   ├── public/
│   │   └── image.png               # Hero illustration
│   └── src/
│       ├── components/             # CV and interview UI components
│       ├── api.js                  # Backend API helper functions
│       ├── pdf.js                 # PDF export logic
│       ├── scores.js              # Score band formatting helpers
│       ├── App.vue                # Main page layout and navigation
│       └── main.js
├── requirements.txt               # Python dependencies
├── .gitignore
├── .env                           # Local environment variables (not committed)
└── README.md
```

## Tech stack

- Frontend: Vue 3 and Vite
- Backend: Python and FastAPI
- AI layer: OpenAI chat/completions with structured responses

## API endpoints

- `GET /api/health` — backend health check
- `POST /api/cv/review` — review pasted CV text or an uploaded PDF against a target role
- `POST /api/interview/start` — start a mock interview and receive the first question
- `POST /api/interview/answer` — submit the latest answer and receive the next question or completion status
- `POST /api/interview/feedback` — evaluate the full interview conversation
- `POST /api/coach/question` — generate a role- or theme-specific behavioral question
- `POST /api/coach/analyze` — assess a draft answer using the STAR framework
- `GET /api/coach/categories` — list the available question categories


## Run locally

You will need Python 3.10+, Node.js with npm, and an OpenAI API key.

1. Create and activate a virtual environment from the project root:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   On Windows, activate it with `.venv\Scripts\activate`.

2. Install the backend dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the repository root:

   ```env
   OPENAI_API_KEY=your_openai_api_key
   ```

   `OPENAI_API_KEY` is required. `OPENAI_MODEL` is `gpt-6-luna` by default. The backend also supports `MAX_CV_CHARS` (default `15000`) and `MAX_FILE_MB` (default `4`).

4. Start the FastAPI backend:

   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at `http://localhost:8000` and health checks are exposed at `http://localhost:8000/api/health`.

5. In a second terminal, install and launch the frontend:

   ```bash
   cd frontend
   npm install
   npm run dev
   ```

   Vite will print the local development URL. During local development, `/api` requests are proxied to the backend at `http://localhost:8000`.

## Deploy to Vercel

Deploy the backend and frontend as two separate projects from this repository.

### Backend project

1. Import the repository with the repository root (`.`) as the **Root Directory**.
2. Configure `OPENAI_API_KEY` and, if needed, `OPENAI_MODEL`.
3. Set `FRONTEND_ORIGIN` to the deployed frontend URL without a trailing slash, for example `https://your-frontend.vercel.app`.
4. Deploy and confirm `https://your-backend.vercel.app/api/health` returns `{"status":"ok"}`.

### Frontend project

1. Import the same repository again and set **Root Directory** to `frontend`.
2. Use the Vite framework preset with the build command `npm run build` and output directory `dist`.
3. Set `VITE_API_BASE_URL` to the backend origin without a trailing slash, for example `https://your-backend.vercel.app`.
4. Redeploy after the environment variable is set so the frontend picks up the backend URL.

If the frontend is deployed on a preview URL or custom domain, update `FRONTEND_ORIGIN` on the backend to that exact origin and redeploy the backend.