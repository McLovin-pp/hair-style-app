import io
import requests
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

app = FastAPI()

# Разрешаем запросы с мобильного приложения/сайта
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Используем бесплатную открытую модель Inpainting
HF_API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-inpainting"

@app.post("/generate-hairstyle")
async def generate_hairstyle(
    file: UploadFile = File(...),
    prompt: str = Form(...) # Например: "a man with short fade haircut, realistic, photo"
):
    image_bytes = await file.read()
    init_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    
    # 1. Создаем простую маску верхней части головы (где волосы)
    width, height = init_image.size
    mask = Image.new("L", (width, height), 0)
    # Закрашиваем белым верхнюю треть изображения (область прически)
    from PIL import ImageDraw
    draw = ImageDraw.Draw(mask)
    draw.rectangle([0, 0, width, int(height * 0.45)], fill=255)

    # 2. Подготавливаем буферы
    init_buf = io.BytesIO()
    init_image.save(init_buf, format="PNG")
    mask_buf = io.BytesIO()
    mask.save(mask_buf, format="PNG")

    # 3. Отправляем в бесплатный Hugging Face API
    # Примечание: Для продакшена нужен бесплатный API-токен с сайта huggingface.co
    payload = {
        "inputs": {
            "image": init_buf.getvalue().hex(),
            "mask_image": mask_buf.getvalue().hex(),
            "prompt": prompt
        }
    }
    
    response = requests.post(HF_API_URL, json=payload)
    
    return {"status": "success", "result": response.json()}