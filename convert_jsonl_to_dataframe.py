import pandas as pd
import json
import os

def process_jsonl_file(file_path):
    # 빈 리스트 초기화
    data = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # 각 줄을 JSON으로 파싱하여 리스트에 추가
            data.append(json.loads(line.strip()))
    
    df = pd.DataFrame(data)
    df_filtered = df[~df['ori_text'].str.contains('부칙|작성관', na=False)]
    df_sorted_filtered = df_filtered.sort_values(by='ori_text')
    return df_sorted_filtered

def process_folder(folder_path, output_excel_path):
    writer = pd.ExcelWriter(output_excel_path, engine='openpyxl')

    for filename in os.listdir(folder_path):
        if filename.endswith('.jsonl'):
            file_path = os.path.join(folder_path, filename)
            df = process_jsonl_file(file_path)
            sheet_name = os.path.splitext(filename)[0]
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    writer.save()
    
# 사용 예시
folder_path = './make_batch_qa_list/'  # 폴더 경로를 여기에 설정하세요
output_excel_path = './output.xlsx'  # 출력될 Excel 파일 경로
process_folder(folder_path, output_excel_path)