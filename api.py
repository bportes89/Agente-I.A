from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .agent import IAAgent

app = FastAPI(title="Agente IA API")
agent = IAAgent()

class Prompt(BaseModel):
    texto: str
    max_length: int = 100

class Resposta(BaseModel):
    resposta: str

@app.post("/perguntar", response_model=Resposta)
async def fazer_pergunta(prompt: Prompt):
    """Endpoint para fazer perguntas ao agente"""
    try:
        resposta = agent.gerar_resposta(prompt.texto, prompt.max_length)
        return Resposta(resposta=resposta)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"mensagem": "Bem-vindo à API do Agente IA"}