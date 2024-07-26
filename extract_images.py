import io
import fitz
import os
import PIL.Image
import requests


def downloadPDF(url: str, filename: str):
    with open(filename, mode="wb") as pdf:
        pdf.write(requests.get(url).content)


def extract_images(pdf: fitz.Document, page: int, imgDir: str):
    imageList = pdf[page].get_images()
    os.makedirs(imgDir, exist_ok=True)
    if imageList:
        for idx, img in enumerate(imageList, start=1):
            data = pdf.extract_image(img[0])
            with PIL.Image.open(io.BytesIO(data.get("image"))) as image:
                image.save(f'{imgDir}/{page}-{idx}.{data.get("ext")}', mode="wb")


def main(url: str = pdf_url):
    filename = url.split("/")[-1]
    foldername = filename.replace(".pdf", "")
    imgDir = os.path.join("papers", foldername, "images")

    downloadPDF(url=url, filename=filename)
    pdf = fitz.open(filename)

    for page in range(pdf.page_count):
        extract_images(pdf, page, imgDir)


if __name__ == "__main__":
    pdf_url = "https://arxiv.org/pdf/1706.03762"
    main()
