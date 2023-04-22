from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from manga_ocr import MangaOcr
from PIL import Image
from io import BytesIO

app = FastAPI()

@app.get("/")
async def home():
    return HTMLResponse("""
        <html>
            <body>
                <form method="post" enctype="multipart/form-data">
                    <input type="file" name="image" accept="image/*">
                    <button type="submit">Extract text</button>
                </form>
            </body>
        </html>
    """)

@app.post("/")
async def get_text(image: UploadFile = File(...)):
    mocr = MangaOcr()
    img = Image.open(BytesIO(await image.read()))
    text = mocr(img)
    return HTMLResponse(f"""
        <html>
            <body>
                <p>Extracted text:</p>
                <pre>{text}</pre>
            </body>
        </html>
    """)

