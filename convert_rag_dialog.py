#!/bin/env python
#-*- coding: utf-8 -*-

import pandas as pd
import jsonlines
import json
import os

## 이건 엑셀파일이 여러개일 때 한번에 돌리기 위한 경로. 만약 엑셀파일 하나라면 아래 두줄은 주석처리하세요.
all_files = os.listdir('.') ## qa데이터 정제 엑셀파일 폴더 경로
excel_file = [os.path.splitext(file)[0] for file in all_files if file.endswith('.xlsx')] ## xlsx인 확장자만 불러와서 파일 명만 추출

## 엑셀 파일 단위로 데이터 생성
def convert_rag_dialog(excel_file_name):
    ## 파일이 엑셀에 묶여있으니까 엑셀 파일 먼저
    qa_file_path = '' + excel_file_name + '.xlsx' ## qa 정제 set 데이터 경로
    
    ## 엑셀 파일 내 시트 이름 리스트
    xls = pd.ExcelFile(qa_file_path)
    sheet_name_list = xls.sheet_names
    
    for sheet_nm in sheet_name_list:
        
        ## dialog 데이터 셋 데이터 경로
        qa_output_path = f'./sft_dialog_data/rag_dialog/{sheet_nm}.json'
        ## 파일 불러오기
        qa_table = pd.read_excel(qa_file_path, sheet_name=sheet_nm)
        
        sft_dialog = []
        for index, row in qa_table.iterrows():
            idx = row['ori_text'].find(')') ## ) 기준으로 조항 이름과 내용 나누기
            doc_idx = row['ori_text'][:idx+1].strip() ## 조항 이름
            doc_cont = row['ori_text'][idx+1:].strip() ## 조항 본문
            
            ## user content 가 너무 길어서 따로 빼서 봄. 수정해도 됩니다.
            user_content = f"""주어진 질문에 차근차근 생각하고 질문에 대한 답변을 해주세요.
'제가 알고 있는 정보' 중 유효한 정보만을 선별하여, 내용 왜곡 없이 질문에 답변하세요. 
반드시 '제가 알고 있는 정보'만을 사용하여 답변하여야 합니다. 
질문에 대한 유효한 정보가 없다면 답변할 수 없다고 말해주세요.
#제가 알고 있는 정보1:{doc_cont}
#참조: {sheet_nm}의 {doc_idx}

#질문: {row['question']}

답변형식은 답변: [내용]을 유지하세요."""
            
            sft_dialog.append([
                {"role": "system", "content" : "당신은 육군 스마트부대 상담사입니다. 다음 내용을 읽고 친절하게 답변할 수 있도록 합니다."}, ## 시스템 메세지 넣기
                {"role":"user", "content": user_content}, ## 여기에 따로 넣어도 됨
                {"role":"assistant", "content": row["answer"]}
            ])
            
        with open(qa_output_path, 'w', encoding='utf-8') as file:
            json.dump(sft_dialog, file, ensure_ascii=False)
            
# 모든 문서 적용시키기 (함수 하나씩만 써도 됨)
## 만일 엑셀이 여러개면 아래 두줄 주석처리 안해도 됨. 
for file_name in excel_file:
    convert_rag_dialog(file_name)

## 만일 엑셀 파일이 하나면 아래 함수 주석 풀어 실행시키기
# file_name = '' ## 엑셀 파일 이름(경로 X)
# convert_rag_dialog(file_name)
