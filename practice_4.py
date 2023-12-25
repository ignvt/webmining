import io
import os
from urllib.parse import urljoin, urlparse
from zipfile import ZipFile

import fitz
import requests
from PIL import Image
from bs4 import BeautifulSoup


def download_pdf(url, local_dir):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return None

    pdf_path = os.path.join(local_dir, os.path.basename(url))
    with open(pdf_path, "wb") as pdf_file:
        for chunk in response.iter_content(chunk_size=128):
            pdf_file.write(chunk)
    return pdf_path


def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page_num in range(doc.page_count):
            page = doc[page_num]
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return ""


def extract_images_from_pdf(pdf_path, image_local_dir):
    try:
        doc = fitz.open(pdf_path)
        for page_num in range(doc.page_count):
            page = doc[page_num]
            images = page.get_images(full=True)
            for img_index, img_info in enumerate(images):
                img_index += 1
                base_image = doc.extract_image(img_index)
                image_bytes = base_image["image"]
                image = Image.open(io.BytesIO(image_bytes))
                image_path = os.path.join(image_local_dir, f"image_page{page_num + 1}_img{img_index}.png")
                image.save(image_path, "PNG")
    except Exception as e:
        print(f"Error extracting images from {pdf_path}: {e}")


def process_pdf_and_save_text(pdf_url, pdf_local_dir, txt_local_dir, image_local_dir):
    pdf_path = download_pdf(pdf_url, pdf_local_dir)
    if pdf_path:
        text = extract_text_from_pdf(pdf_path)
        txt_path = os.path.join(txt_local_dir, os.path.basename(pdf_path).replace(".pdf", ".txt"))
        with open(txt_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(text)

        extract_images_from_pdf(pdf_path, image_local_dir)


def get_links_recursive_with_processing(url, depth=1, visited=None, pdf_local_dir=None, txt_local_dir=None,
                                        image_local_dir=None, max_links=1):
    if visited is None:
        visited = set()
    if pdf_local_dir is None:
        pdf_local_dir = "pdf_files"
    if txt_local_dir is None:
        txt_local_dir = "txt_files"
    if image_local_dir is None:
        image_local_dir = "image_files"

    if not os.path.exists(pdf_local_dir):
        os.makedirs(pdf_local_dir)
    if not os.path.exists(txt_local_dir):
        os.makedirs(txt_local_dir)
    if not os.path.exists(image_local_dir):
        os.makedirs(image_local_dir)

    if depth == 0 or url in visited or len(os.listdir(pdf_local_dir)) >= max_links:
        return

    visited.add(url)

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return

    links = [urljoin(url, a.get("href")) for a in BeautifulSoup(response.text, "html.parser").find_all("a", href=True)]

    for link in links:
        if urlparse(link).netloc == urlparse(url).netloc:
            if link.endswith(".pdf"):
                process_pdf_and_save_text(link, pdf_local_dir, txt_local_dir, image_local_dir)

            get_links_recursive_with_processing(link, depth - 1, visited, pdf_local_dir, txt_local_dir, image_local_dir,
                                                max_links)


if __name__ == "__main__":
    start_url = "https://pstu.ru/sveden/education/"
    pdf_folder = "pdf_files"
    txt_folder = "txt_files"
    image_folder = "image_files"

    get_links_recursive_with_processing(start_url, pdf_local_dir=pdf_folder, txt_local_dir=txt_folder,
                                        image_local_dir=image_folder)

    with ZipFile("result_archive.zip", "w") as zip_file:
        for folder in [pdf_folder, txt_folder, image_folder]:
            for root, dirs, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    zip_file.write(file_path, os.path.relpath(file_path, folder))
