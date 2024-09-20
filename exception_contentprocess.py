#!/bin/env python
#-*- coding: utf-8 -*-
import re
import os
import re
import pdfplumber
import olefile
import zlib
import struct

class ContentsProcess:
    def __init__(self):
        pass

    def convert_key_to_num(contents, number_key, title_type):
        ## 특정 문자가 왔을 때 이걸 차례로 넘버링하기
        # number_key = '¢'

        chapter_number = 1
        result = []
        for line in contents:
            if line.startswith(number_key):
                if title_type != '조':
                    line = f'제{chapter_number}{title_type} {line[2:-1]}\n'
                else:
                    line = f'제{chapter_number}{title_type}({line[2:-1]})\n'
                chapter_number += 1
            result.append(line)
        
        return result
    
    def convert_num_to_jo(contents, title_type):
        ## 1. -> 제1조() 로 변환해주기
        refined_contents = []
        pattern = re.compile(r'^(\s*)(\d+)\.(\s+)(.+)\n')
        
        for line in contents:
            match = pattern.match(line)
            if match:
                etc = match.group(1)
                number = match.group(2)
                content = match.group(4)
                if title_type != '조':
                    refined_line = f"{etc}제{number}{title_type} {content}\n"
                    refined_contents.append(refined_line)
                else:
                    refined_line = f"{etc}제{number}{title_type}({content})\n"
                    refined_contents.append(refined_line)
            else:
                refined_contents.append(line)
        
        return refined_contents
    
    

    def convert_rom_to_num(contents, title_type):
        ## 로마숫자를 제1조()로 바꾸기
        def roman_to_int(roman):
            ## 로마숫자 아라비아 숫자로 변환
            roman_numerals = {
                'Ⅰ': 1, 'Ⅱ': 2, 'Ⅲ': 3, 'Ⅳ': 4, 'Ⅴ': 5, 'Ⅵ': 6, 'Ⅶ': 7, 'Ⅷ': 8, 'Ⅸ': 9, 'Ⅹ': 10,
                'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10
            }
            return roman_numerals.get(roman, 0)
        pattern = re.compile(r'^(Ⅰ|Ⅱ|Ⅲ|Ⅳ|Ⅴ|Ⅵ|Ⅶ|Ⅷ|Ⅸ|Ⅹ|I{1,3}|IV|V|VI{0,3}|IX|X)[\.\s]')
        
        def replace_line(line, title_type):
            match = pattern.match(line)
            if match:
                num = roman_to_int(match.group(1))
                title = line[match.end():].strip()
                if title_type != '조':
                    return f'제{num}{title_type} {title}\n'
                else:
                    return f'제{num}{title_type}({title})\n'
            return line
        
        return [replace_line(line,title_type) for line in contents]
    
    def convert_kor_to_num(contents, title_type):
        # 한글 목차 항목을 찾기 위한 정규 표현식
        pattern = re.compile(r'^\s*([가-하])\.\s*(.+)\n')
        
        # 현재 조항 번호
        article_number = 1
        
        # 변환된 텍스트를 저장할 리스트
        converted_lines = []
        
        for line in contents:
            # 한글 목차 항목을 찾기 위한 정규 표현식 매칭 및 변환
            if title_type != '조':
                new_line = pattern.sub(lambda m: f'제{article_number}{title_type} {m.group(2)}\n', line)
            else:
                new_line = pattern.sub(lambda m: f'제{article_number}{title_type}({m.group(2)})\n', line)
            if new_line != line:  # 변환이 일어난 경우에만 조항 번호 증가
                article_number += 1
            converted_lines.append(new_line)
        
        return converted_lines
    
class DocToText:
    def __init__(self, filename, folder_path, output_path):
        self.filename = filename
        self.folder_path = folder_path
        self.output_path = output_path
    
    # hwp --> text 변환
    def get_hwp_text(self):
        f = olefile.OleFileIO(self.folder_path + self.filename + '.hwp')
        dirs = f.listdir()

        # HWP 파일 검증
        if ["FileHeader"] not in dirs or \
        ["\x05HwpSummaryInformation"] not in dirs:
            raise Exception("Not Valid HWP.")

        # 문서 포맷 압축 여부 확인
        header = f.openstream("FileHeader")
        header_data = header.read()
        is_compressed = (header_data[36] & 1) == 1

        # Body Sections 불러오기
        nums = []
        for d in dirs:
            if d[0] == "BodyText":
                nums.append(int(d[1][len("Section"):]))
        sections = ["BodyText/Section"+str(x) for x in sorted(nums)]

        # 전체 text 추출
        text = ""
        for section in sections:
            bodytext = f.openstream(section)
            data = bodytext.read()
            if is_compressed:
                unpacked_data = zlib.decompress(data, -15)
            else:
                unpacked_data = data
        
            # 각 Section 내 text 추출    
            section_text = ""
            i = 0
            size = len(unpacked_data)
            while i < size:
                header = struct.unpack_from("<I", unpacked_data, i)[0]
                rec_type = header & 0x3ff
                rec_len = (header >> 20) & 0xfff

                if rec_type in [67]:
                    rec_data = unpacked_data[i+4:i+4+rec_len]
                    section_text += rec_data.decode('utf-16')
                    section_text += "\n"

                i += 4 + rec_len

            text += section_text
            text += "\n"

        # 텍스트 파일로 저장
        with open(self.output_path + self.file_name + '.txt', 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)

        # 텍스트를 \n 기준으로 리스트화
        text_list = [line + '\n' for line in text.split('\n') if line]
        
        return text_list
    
    # pdf --> text 변환
    def get_pdf_text(self, drop_page):
        ## 제거할 페이지 남기고 txt 추출
        with pdfplumber.open(self.folder_path + self.file_name + '.pdf') as pdf:
            text = ''
            for page_number in range(len(pdf.pages)):
                if page_number not in drop_page:
                    ## 페이지 텍스트 추출
                    text += pdf.pages[page_number].extract_text()

                    # 텍스트 파일로 저장
                with open(self.output_path + self.file_name + '.txt', 'w', encoding='utf-8') as txt_file:
                    txt_file.write(text)
        
        # 텍스트를 \n 기준으로 리스트화
        text_list = [line + '\n' for line in text.split('\n') if line]

        return text_list


## 아래 함수를 사용해서 데이터를 정제하세요. 
file_name = '탄약 수송 결박지침서'
folder_path = './data/jisi/' 
output_path = './'

DocToText = DocToText(file_name, folder_path, output_path)

# 한글파일 일 때
text_list = DocToText.get_hwp_text()

# pdf 파일일 때
    ## 제거해야할 페이지 설정
    ## 해당 부분은 PDF일때만 적용됨
    ## 여백 페이지 같은거 확인한 후 지울 페이지 수 입력하면 됨
drop_page = list(range(1,8)) + [23]
# 1~8페이지같이 연속된 숫자 : list(range(start_num, end_num))
# 단일 페이지 : [1, 2, 3]
drop_page = [p-1 for p in drop_page]
text_list = DocToText.get_pdf_text(drop_page)

## 아래 함수들 중 활성화
# ### 특정 문자가 조나 장이 되도록 변환 (가운데 특수기호, 세번째 장 원하는걸로 변경)
# ContentsProcess.convert_key_to_num(text_list,'¢','장')
# ### 1. 2. -> 제1조(), 제2조()로 변환 (장, 절도 가능, 두번째 값 변경)
# ContentsProcess.convert_num_to_jo(text_list, '조')
# ### 로마자 아라비아로 변경후 장, 절 조로 변환(숫자 10까지밖에 안됨. 그 이상 있으면 말씀하세요)
# ContentsProcess.convert_rom_to_num(text_list, '조')
# ### 가, 나, 다 -> 제1조(),제2조()로 변환 (장, 절도 가능, 두번째 값 변경)
# ContentsProcess.convert_kor_to_num(text_list, '조')
