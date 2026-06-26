import base64
import hashlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time

from bs4 import BeautifulSoup

import multiprocessing

def parsePageTexts(inq:multiprocessing.Queue, outq:multiprocessing.Queue) -> None:
    text = inq.get()
    pagenum = inq.get()
    soup = BeautifulSoup(text, "html.parser")
    spans = soup.find_all("span")
    
    text_data = []
    for span in spans:
        text = span.get_text().strip()
        if not text: continue
        style = span.get("style", "")
        left = float(re.search(r"left:\s*([\d\.]+)px", style).group(1))
        top = float(re.search(r"top:\s*([\d\.]+)px", style).group(1))
        font_size = float(re.search(r"font-size:\s*([\d\.]+)px", style).group(1))
        text_data.append({"text": text, "x": left, "y": top, "size": font_size})
    
    outq.put((text_data, pagenum))

class Driver:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.previous_canvas_hash:str|None = None
        self.previous_text_hash:str|None = None
        self.test_canvas_hash:str|None = None
        self.test_text_hash:str|None = None
    
    def goto(self, url:str) -> None:
        self.driver.get(url)
    
    def focus(self) -> None:
        tabs = self.driver.window_handles
        self.driver.switch_to.window(tabs[-1])
    
    def quit(self) -> None:
        self.driver.quit()
    
    def getRaw(self) -> tuple[bytes, str, int, int]:
        return (self.getPage(), self.getPageTextsRaw(), *self.getSize())
    
    def getPage(self) -> bytes:
        flag = False
        while True:
            canvas = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".material-canvas canvas"))
            )
            text_layer = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "text-layer"))
            )
            canvas_base64 = self.driver.execute_script("return arguments[0].toDataURL('image/png');", canvas)
            canvas_hash = hashlib.sha256(canvas_base64.encode('utf-8')).hexdigest()
            
            current_text_html = text_layer.get_attribute("innerHTML")
            if current_text_html == "":
                time.sleep(0.05)
                continue
            text_hash = hashlib.sha256(current_text_html.encode('utf-8')).hexdigest()
            
            if (not flag) and (self.previous_canvas_hash != canvas_hash) and (self.previous_text_hash != text_hash):
                self.test_canvas_hash = canvas_hash
                self.test_text_hash = text_hash
                flag = True
                time.sleep(0.05)
                continue

            if flag:
                if (self.test_canvas_hash != canvas_hash) or (self.test_text_hash != text_hash):
                    self.test_canvas_hash = canvas_hash
                    self.test_text_hash = text_hash
                    time.sleep(0.05)
                    continue
                self.previous_canvas_hash = canvas_hash
                self.previous_text_hash = text_hash
                
                base64_data = canvas_base64.split(",")[1]
                return base64.b64decode(base64_data)
            
            time.sleep(0.05)
    
    def getPageTextsRaw(self) -> str:
        text_layer = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "text-layer")))
        return text_layer.get_attribute("innerHTML")
    
    def getSize(self) -> tuple[int, int]:
        canvas_element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".material-canvas canvas")))
        orig_w = int(canvas_element.get_attribute("width"))
        orig_h = int(canvas_element.get_attribute("height"))

        return (orig_w, orig_h)
    
    def nextPage(self) -> bool:
        if self.isLastPage():
            return False
        current_page = self.getPageNum()[0]
        next_button = self.driver.find_element(By.CSS_SELECTOR, "button.next-btn")
        next_button.click()
        return True
    
    def isLastPage(self) -> bool:
        pagenum = self.getPageNum()
        return pagenum[0] == pagenum[1]
    
    def getPageNum(self) -> tuple[int, int]:
        page_element = self.driver.find_element(By.CSS_SELECTOR, ".page-chip")
        page_text = page_element.text.strip()
        current_page, total_pages = map(int, page_text.split("/"))
        return (current_page, total_pages)