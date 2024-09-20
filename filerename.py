import os
import pandas as pd
import glob

def rename_files(df, folder_path):
    for index, row in df.iterrows():
        old_filename = row['filename']
        new_docname = row['docname']
        
        # 폴더 내의 pdf 및 hwp 파일을 검색
        possible_files = glob.glob(os.path.join(folder_path, old_filename + '.pdf')) + \
                         glob.glob(os.path.join(folder_path, old_filename + '.hwp'))
        
        if possible_files:
            old_filepath = possible_files[0]  # 해당 이름의 파일이 존재하면 첫 번째 파일 경로 사용
            file_extension = os.path.splitext(old_filepath)[1]
            new_filename = new_docname + file_extension
            new_filepath = os.path.join(folder_path, new_filename)
            
            os.rename(old_filepath, new_filepath)
            print(f'Renamed: {old_filename + file_extension} -> {new_filename}')
        else:
            print(f'File not found: {old_filename}')

## 파일 이름과 문서 이름 매칭된 데이터 프레임 불러오기
# df = pd.read_csv('./file_docname.csv', encoding = 'euc-kr')
# folder_path = './pdffile_test'

rename_files(df, folder_path)