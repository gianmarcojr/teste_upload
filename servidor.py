from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from datetime import datetime

app = FastAPI()

# Liberar acesso de qualquer origem (para funcionar com o HTML local)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/enviar")
async def receber_dados(
    perito: str = Form(...),
    descricao: str = Form(...),
    arquivo: UploadFile = File(...)
):
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_base = f"{timestamp}_{perito.replace(' ', '_')}"

        caminho_arquivo = os.path.join(UPLOAD_DIR, f"{nome_base}_{arquivo.filename}")

        with open(caminho_arquivo, "wb") as buffer:
            buffer.write(await arquivo.read())

        with open(os.path.join(UPLOAD_DIR, f"{nome_base}_descricao.txt"), "w", encoding="utf-8") as f:
            f.write(descricao)

        return JSONResponse(content={"mensagem": "Dados recebidos com sucesso!"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"erro": str(e)})
