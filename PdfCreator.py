import multiprocessing

import fitz

from io import BytesIO
from PIL import Image

font_path = "font/NotoSansJP-VariableFont_wght.ttf"

def compress_image(inq:multiprocessing.Queue, outq:multiprocessing.Queue) -> None:
    image = inq.get()
    pagenum = inq.get()
    img = Image.open(BytesIO(image))
    if img.mode == "RGBA":
        img = img.convert("RGB")

    compressed_stream = BytesIO()
    img.save(compressed_stream, format="PNG", optimize=True)
    compressed_img_bytes = compressed_stream.getvalue()
    
    outq.put((compressed_img_bytes, pagenum))

class PdfCreator:
    def __init__(self):
        self.doc = fitz.open()
    
    def add_page(self, image:bytes, text_data:list, width:int, height:int) -> None:
        tmpdoc = fitz.open()
        page = tmpdoc.new_page(width=width, height=height)
        page.insert_image(page.rect, stream=image)

        for txt in text_data:
            point = fitz.Point(txt["x"], txt["y"] + txt["size"])
            page.insert_text(point, txt["text"], fontsize=txt["size"], fontname="my-jp-font", fontfile=font_path, render_mode=3)
        
        new_page = self.doc.new_page(width=842, height=842 * height / width)
        new_page.show_pdf_page(new_page.rect, tmpdoc, 0)

        tmpdoc.close()
    
    def save(self, path:str):
        self.doc.save(path,garbage=4, deflate=True, clean=True)
        self.doc.close()