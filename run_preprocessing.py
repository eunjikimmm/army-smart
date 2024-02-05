#!/bin/env python
#-*- coding: utf-8 -*-

from src import TxtPreprocessing

# pdf_folder_path = '/home/minds/army_smart/data/pdf/' # 서버 내 pdf 위치
# output_folder = '/home/minds/army_smart/data/txt/'   # 서버 내 txt 폴더 위치
# txt_file_name = '「국방 양성평등 지원에 관한 훈령」 일부개정안 전문.txt' # 파일 명
def run():
    # output_folder = '/home/minds/army_smart/data/txt/'
    output_folder = '/home/minds/army_smart/data/txt/'
    txt_file_name = input('파일 이름을 입력하세요 (예. 국방부 전문.txt): ')
    
    
    TxtPreprocessing.preprocessing(output_folder, txt_file_name)
    # except Exception as e:
    #     print(e)
        
# 함수 호출
if __name__ == "__main__":
    run()