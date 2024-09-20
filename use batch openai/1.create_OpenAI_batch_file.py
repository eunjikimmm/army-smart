import requests
import json
import time
import pandas as pd
from tqdm import tqdm
import tkinter as tk
from tkinter import filedialog
import os  # os 모듈 추가

# 파일 선택 대화상자 초기화
root = tk.Tk()
root.withdraw()  # Tkinter 창을 보이지 않게 함

# 사용자가 파일을 선택할 수 있도록 함
file_path = filedialog.askopenfilename(title="엑셀 파일 선택", filetypes=[("Excel files", "*.xlsx;*.xls")])

# 선택된 파일이 있는 디렉토리의 경로를 얻음
directory = os.path.dirname(file_path)

# 파일명 추출 (확장자 제외)
file_name = os.path.splitext(os.path.basename(file_path))[0]

# 엑셀에서 질문 읽어오기
df_from_excel = pd.read_excel(file_path)  # 사용자가 선택한 파일로 변경
model = df_from_excel['model']
system = df_from_excel['system']  # 읽어올 열의 이름, 질문이 있는 열의 이름 입력
user = df_from_excel['user']  # 읽어올 열의 이름, 질문이 있는 열의 이름 입력
temperature = 0
top_p = 0.1
presence_penalty = 0
frequency_penalty = 0
max_tokens = 4096

n = len(user)
result = []
# print(system[0], len(system))
# print(user[1], len(user))

for i in tqdm(range(n)):
    task = {
            "custom_id": f"task{i}",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                # This is what you would have in your Chat Completions API call
                "model": model[i],
                "messages": [
                    {
                        "role": "system",
                        "content": system[i]
                    },
                    {
                        "role": "user",
                        "content": user[i]
                    }
                ],
                "temperature": temperature,
                "top_p": top_p,
                "presence_penalty": presence_penalty,
                "frequency_penalty": frequency_penalty,
                "max_tokens": max_tokens,
            }
        }
    # print(task)
    result.append(task)


jsonl_name = f"{file_name}_JSONL_RESULT.jsonl"

with open(jsonl_name, 'w', encoding='utf-8') as file:
    for obj in result:
        file.write(json.dumps(obj, ensure_ascii=False) + '\n')