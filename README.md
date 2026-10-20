# AI-Career-Coach
An AI-powered Career Coach that helps users prepare for job interviews, improve their CVs, and advance their careers through a conversational interface.

## Deploying to Vercel

Deploy the frontend and backend as separate Vercel projects from this repository.

### Backend

1. Import the repository as a Vercel project and set **Root Directory** to `.` (the repository root).
2. Let Vercel detect the FastAPI app in `app/main.py`; do not set a static output directory or frontend build command.
3. Add these environment variables:
   - `OPENAI_API_KEY`: your OpenAI API key.
   - `FRONTEND_ORIGIN`: the frontend's production Vercel origin, such as `https://your-frontend.vercel.app` (no trailing slash).
4. Deploy and check `https://your-backend.vercel.app/api/health`; it should return `{"status":"ok"}`.

### Frontend

1. Import the same repository as another Vercel project and set **Root Directory** to `frontend`.
2. Select **Vite** as the framework. Use build command `npm run build` and output directory `dist`.
3. Add `VITE_API_BASE_URL` with the backend's origin, such as `https://your-backend.vercel.app` (no trailing slash).
4. Deploy. The CV reviewer is available at the frontend project's root URL.

Vite environment variables are embedded at build time, so redeploy the frontend after changing `VITE_API_BASE_URL`. If using a different frontend preview URL, add that exact origin to the backend's `FRONTEND_ORIGIN` and redeploy the backend.
