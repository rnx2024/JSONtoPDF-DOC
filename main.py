from fastapi import FastAPI
from routes.render import router

app = FastAPI(title="JSON+Image → PDF/DOCX Converter (modular, no app package)")
app.include_router(router)
