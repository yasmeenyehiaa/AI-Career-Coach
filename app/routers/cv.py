"""POST /api/cv/review"""
from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.config import get_settings
from app.schemas.cv import CVResponse, CVRequest
from app.services.cv_review import review_cv
from app.services.llm import LLMError
from app.services.pdf_parser import CVInputError, parse_pdf

router = APIRouter(prefix="/api/cv", tags=["cv"])



@router.post("/review", response_model=CVResponse)
def review(
    role: str = Form(...),                       
    cv_text: str | None = Form(None),             
    file: UploadFile | None = File(None),          
    job_description: str | None = Form(None),    
):
    settings = get_settings()

    # 1. Validate the role
    if not role.strip():
        raise HTTPException(status_code=400, detail="Please provide the target role.")

    # 2. Validate the cv: exactly file or pasted text
    has_text = bool(cv_text and cv_text.strip())
    has_file = file is not None and bool(file.filename)
    if has_text == has_file:  # both or neither
        raise HTTPException(status_code=400, detail="Provide either a PDF file or pasted text, not both or none.")

    try:
        # 3. Get the CV as plain text
        if has_file:
            if not file.filename.lower().endswith(".pdf"):
                raise HTTPException(status_code=400, detail="Only PDF files are supported.")
            max_bytes = settings.max_file_mb * 1024 * 1024
            data = file.file.read(max_bytes + 1)  # read one extra byte to detect "too big"
            if len(data) > max_bytes:
                raise HTTPException(status_code=413, detail=f"File too large (max {settings.max_file_mb} MB).")
            text = parse_pdf(data)
        else:
            text = cv_text.strip()

        if len(text) > settings.max_cv_chars:
            raise HTTPException(status_code=413, detail="CV text is too long.")

        request = CVRequest(
            role=role.strip(),
            job_description=job_description,
            cv_text= text
        )

        # 4. Ask the model for the review
        return review_cv(request)

    except CVInputError as e:      # bad user input -> 400
        raise HTTPException(status_code=400, detail=str(e))
    except LLMError as e:          # OpenAI problem -> 502
        raise HTTPException(status_code=502, detail=str(e))
