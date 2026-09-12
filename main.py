from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
from typing import Optional, Dict, Any, List
from src.preprocessing.dataset_loader import DatasetPreprocessor
from src.intents.classifier import ProposedIntentClassifier
from src.retrieval.retriever import HistoricalSupportRetriever
from src.generation.generator import ReplyGenerator
from src.evaluation.evaluator import Evaluator

ROOT = Path(__file__).resolve().parent

app = FastAPI(
    title="Hiver Uber Support Agent",
    description="AI Customer Support Agent with Intent Classification, Historical Retrieval, Grounded Reply Generation & Escalation Policy",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")

# Initialize pipeline components
preprocessor = DatasetPreprocessor()
conversations = preprocessor.load_or_generate_uber_dataset()
retriever = HistoricalSupportRetriever(conversations)
generator = ReplyGenerator()

texts = [c["customer_message"] for c in conversations]
labels = [c["intent"] for c in conversations]
classifier = ProposedIntentClassifier()
classifier.fit(texts, labels)

class SupportRequest(BaseModel):
    message: str

class SupportResponse(BaseModel):
    customer_message: str
    predicted_intent: str
    intent_confidence: float
    retrieved_evidence: List[Dict[str, Any]]
    reply: str
    escalate: bool
    escalation_reason: str

@app.post("/v1/support", response_model=SupportResponse)
def process_support_query(req: SupportRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Customer message cannot be empty.")

    # 1. Intent Classification
    intent, confidence = classifier.predict_single(req.message)

    # 2. Historical Support Retrieval
    retrieved = retriever.retrieve(req.message, top_k=2)

    # 3. Generation & Escalation Decision
    gen_result = generator.generate_response(req.message, intent, confidence, retrieved)

    return {
        "customer_message": req.message,
        "predicted_intent": intent,
        "intent_confidence": confidence,
        "retrieved_evidence": retrieved,
        "reply": gen_result["reply"],
        "escalate": gen_result["escalate"],
        "escalation_reason": gen_result["escalation_reason"]
    }

@app.post("/v1/evaluate")
def run_evaluation():
    try:
        evaluator = Evaluator()
        results = evaluator.evaluate_system()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_class=HTMLResponse)
def read_root():
    return FileResponse(ROOT / "templates" / "index.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
