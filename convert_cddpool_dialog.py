#!/bin/env python
#-*- coding: utf-8 -*-

import jsonlines
import json
import os

all_files = os.listdir('./retrieval_data/candidate_pool_url/') ## candidate pool 경로
jsonl_file = [os.path.splitext(file)[0] for file in all_files if file.endswith('.jsonl')] ## jsonl인 확장자만 불러와서 파일 명만 추출

# candiate_pool로 규정 데이터를 학습하는 방법
def convert_cddpool_dialog(file_name):
    ## candidate_pool로 원본 데이터 불러오기 
    ## ori_text는 제목과 내용이 붙어있어서 분할하기 어려울 것 같음
    candidate_pool_path = f'./retrieval_data/candidate_pool_url/{file_name}.jsonl' ## candidate pool 있는 경로로 변환
    dialog_output_path = f'./sft_dialog_data/text_dialog/{file_name}.json'         ## dialog 경로로 변환

    candidate_pool = []
    with jsonlines.open(candidate_pool_path, 'r') as file:
        for pool in file:
            candidate_pool.append(pool)  # JSON 파일을 파싱
            
    sft_dialog = []
    for row in candidate_pool:
        sft_dialog.append([
            {"role": "system", "content" : "당신은 육군 스마트부대 상담사입니다. 다음 내용을 읽고 친절하게 답변할 수 있도록 합니다."}, ## 시스템 메세지 넣기
            {"role":"user", "content":f"{row['reference']}의 {row['url']}에 대해 그대로 읽어줘"}, 
            {"role":"assistant", "content":f"{row['reference']}의 {row['url']}에 대해 읽어드리겠습니다.\n {row['text']}"}
        ])

    with open(dialog_output_path, 'w', encoding='utf-8') as file:
        json.dump(sft_dialog, file, ensure_ascii=False)


# 모든 문서 적용시키기       
for file_name in jsonl_file:
    convert_cddpool_dialog(file_name)