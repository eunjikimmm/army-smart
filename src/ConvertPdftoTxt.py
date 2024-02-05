from PyPDF2 import PdfReader
import os

def save_all_pdfs_as_texts(pdf_folder_path, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for pdf_file_name in os.listdir(pdf_folder_path):
        if pdf_file_name.endswith(".pdf"):
            pdf_file_path = os.path.join(pdf_folder_path, pdf_file_name)
            output_text_file_path = os.path.join(output_folder, pdf_file_name.replace('.pdf', '.txt'))

            save_pdf_as_text(pdf_file_path, output_text_file_path)

def save_pdf_as_text(pdf_file_path, output_text_file_path):
    with open(pdf_file_path, 'rb') as pdf_file, open(output_text_file_path, 'w', encoding='utf-8') as text_file:
        reader = PdfReader(pdf_file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]  # 수정된 부분
            text_file.write(page.extract_text())

# 입력 PDF 파일이 있는 폴더 경로와 출력 텍스트 파일이 저장될 폴더를 설정합니다.
# PDF_FOLDER_PATH = r'C:\Users\mindslab\PycharmProjects\XDC\environment_eval\환경2023\사전\pdf'
# OUTPUT_FOLDER = r'C:\Users\mindslab\PycharmProjects\XDC\environment_eval\환경2023\사전\txt'

# # 함수 호출
# save_all_pdfs_as_texts(PDF_FOLDER_PATH, OUTPUT_FOLDER)