import pandas as pd
import tqdm as tqdm
import json

input_path = './부서별 군사한영번역 20240808.xlsx'
output_path = './army_dialog_translation.json'

## 영문 번역 데이터 불러오기
raw_df = pd.read_excel(input_path, sheet_name = '종합')

## 한 -> 영 / 영 -> 한 instruction 테이블
convert_eng_inst = [col for col in raw_df.columns.to_list() if "영어" in col]
convert_kor_inst = [col for col in raw_df.columns.to_list() if ("한국어" in col )|("한글" in col)][1:]

## for문으로 dialog_templete 만들기
fin_list = []
## 한-> 영
for col in convert_eng_inst:
    json_list = []
    for idx, row in raw_df.iterrows():
        dialog = [
            # {"role":"system", "content":"system prompt"},
            {"role":"user","content":row[col]},
            {"role":"assistant","content":row["영문"]}
        ]
        json_list.append(dialog)
    fin_list = fin_list + json_list
## 영 -> 한   
for col in convert_kor_inst:
    json_list = []
    for idx, row in raw_df.iterrows():
        dialog = [
            # {"role":"system", "content":"system prompt"},
            {"role":"user","content":row[col]},
            {"role":"assistant","content":row["한글"]}
        ]
        json_list.append(dialog)
    fin_list = fin_list + json_list
    
## json 저장
with open(output_path, 'w', encoding='utf-8') as file:
    json.dump(json_list, file, ensure_ascii=False)