from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from src.core.engine import AnalisadorADMWeb
import tempfile, os, cv2, base64, numpy as np

router = APIRouter()

@router.post("/video")
async def analisar_video(
    video: UploadFile = File(...),
    movimento: str = Form(...),
    lado: str = Form(...),
    paciente_id: int = Form(...)
):
    # Salva o vídeo temporariamente
    suffix = os.path.splitext(video.filename)[1] or ".mp4"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await video.read())
        tmp_path = tmp.name

    try:
        analisador = AnalisadorADMWeb(
            id_paciente=str(paciente_id),
            tipo_movimento=movimento,
            lado_do_corpo=lado,
            usar_gpu=False
        )

        cap = cv2.VideoCapture(tmp_path)
        if not cap.isOpened():
            raise HTTPException(status_code=400, detail="Não foi possível abrir o vídeo")

        fps = cap.get(cv2.CAP_PROP_FPS) or 30
        frames_processados = []

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame_anotado = analisador.processar_frame(frame)
            if frame_anotado is not None:
                _, buf = cv2.imencode(".jpg", frame_anotado, [cv2.IMWRITE_JPEG_QUALITY, 60])
                frames_processados.append(base64.b64encode(buf).decode())

        cap.release()

        resultado = analisador.finalizar_analise(fps=fps)
        resultado["frames_b64"] = frames_processados[-10:] if len(frames_processados) > 10 else frames_processados

        return resultado

    finally:
        os.unlink(tmp_path)
