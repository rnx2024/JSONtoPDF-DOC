from fastapi import FastAPI
from routes.render import router

app = FastAPI(title="JSON+Image to PDF/DOCX Converter")
app.include_router(router)
