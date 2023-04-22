from fastapi import FastAPI, File, UploadFile
from manga_ocr import MangaOcr
import PIL.Image

app = FastAPI()

@app.post("/get_text")
async def get_text(image: UploadFile = File(...)):
    mocr = MangaOcr()
    img = PIL.Image.open(image.file)
    text = mocr(img)
    return {"text": text}
