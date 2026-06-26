from Driver import *
from PdfCreator import *

import multiprocessing

import tkinter as tk
from tkinter import ttk, filedialog

def capture():
    driver.focus()
    pdfdata = []
    outq_img = multiprocessing.Queue()
    outq_txt = multiprocessing.Queue()
    num = 0
    while True:
        data = driver.getRaw()
        pdfdata.append([None, None, data[2],data[3]])
        q_img = multiprocessing.Queue()
        q_img.put(data[0])
        q_img.put(num)
        p_img = multiprocessing.Process(target=compress_image, args=(q_img, outq_img))
        p_img.start()
        q_txt = multiprocessing.Queue()
        q_txt.put(data[1])
        q_txt.put(num)
        p_txt = multiprocessing.Process(target=parsePageTexts, args=(q_txt, outq_txt))
        p_txt.start()
        num += 1
        if not driver.nextPage(): break

    for _ in range(num):
        d_img = outq_img.get()
        pdfdata[d_img[1]][0] = d_img[0]
        d_txt = outq_txt.get()
        pdfdata[d_txt[1]][1] = d_txt[0]
    pdf = PdfCreator()
    for d in pdfdata:
        pdf.add_page(*d)
    path = filedialog.asksaveasfilename(defaultextension=".pdf")
    try:
        if not path.lower().endswith(".pdf"):
            path += ".pdf"
    except:
        return
    pdf.save(path)

def gopanda():
    driver.goto("https://panda.ecs.kyoto-u.ac.jp/portal")

def gokulms():
    driver.goto("https://lms.gakusei.kyoto-u.ac.jp/portal")

if __name__ == "__main__":
    window = tk.Tk()
    window.title("BookRollDL")
    window.attributes("-topmost", True)

    window.resizable(False, False)
    sty = ttk.Style(window)
    sty.configure("main.TButton", font=",20")

    pandabtn = ttk.Button(text="PandA", command=gopanda)
    kulmsbtn = ttk.Button(text="KULMS", command=gokulms)
    startbtn = ttk.Button(style="main.TButton", text="取り込み開始", command=capture)
    pandabtn.grid(row=0, column=0, padx=10, pady=10)
    kulmsbtn.grid(row=0, column=1, padx=10, pady=10)
    startbtn.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    driver = Driver()

    window.mainloop()

    driver.quit()