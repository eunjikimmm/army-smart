#!/bin/env python
#-*- coding: utf-8 -*-
import pandas as pd
import jsonlines
import json

## 각 데이터 셋 경로 지정
qa_set_path = './예상QA증강_intent.csv'                       ## 전달받은 QA 데이터셋
retriever_train_path = './qa_retriever_train.jsonl'   ## retriever 학습 셋
candidate_pool_path = './candidate_pool_add_qa.jsonl' ## candidate_pool
sft_dialog_path = './dialog_sft.jsonl'                ## 추가학습 데이터셋

## QA 데이터셋 불러오기
qa_set = pd.read_csv('./예상QA증강.csv', encoding = 'euc-kr')

## retriever train set을 만들기 위한 과정
retriever_train = []
for index, row in qa_set.iterrows():
    retriever_train.append({"source": row["질문"], "target": row["이상적인 답변"]})

with jsonlines.open(retriever_train_path, mode = 'w') as writer:
    writer.write_all(retriever_train)

## candidate_pool을 만들기 위한 과정
answer_list = qa_set[['이상적인 답변', '관련근거']].drop_duplicates()
candidate_pool = []
for index, row in answer_list.iterrows():
    candidate_pool.append({"subject": "", "text": row['이상적인 답변'], "reference": row['관련근거']})

with jsonlines.open(candidate_pool_path, mode = 'w') as writer:
    writer.write_all(candidate_pool)


## dialog_templete 만들기
sft_dialog = []
for index, row in qa_set.iterrows():
    sft_dialog.append([
        {"role": "system", "content" : "시스템 메세지를 넣으세요"}, ## 시스템 메세지 넣기
        {"role":"user", "content":row["질문"]}, 
        {"role":"assistant", "content":row["이상적인 답변"] + "\n ※관련 근거:" + row["관련근거"]}
    ])

# with jsonlines.open(sft_dialog_path, mode = 'w') as writer:
#     writer.write_all(sft_dialog)


with open(sft_dialog_path, 'w', encoding='utf-8') as file:
    json.dump(sft_dialog, file, ensure_ascii=False)