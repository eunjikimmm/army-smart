#!/bin/env python
#-*- coding: utf-8 -*-

# from PyPDF2 import PdfReader
# import src.ConvertPdftoTxt as cpt
# from tqdm import tqdm
import os
import re
import json

def preprocessing(output_folder, txt_file_name):
    
    ## txt 추출
    txt_list = []
    with open(os.path.join(output_folder, txt_file_name),'r') as f:
        line = f.readlines()
        txt_list += line
    f.close()

    ## 이 문서는 목차가 없음. 그리고 조 단위가 없으므로 1. ~ 인걸로 찾아야 함
    ## 조항 내용 / 별표와 별지 따로 리스트 생성
    if len([i for i, txt in enumerate(txt_list) if re.search('\s*1\.', txt)]) >= 2:
        jeoul_idx = [i for i, txt in enumerate(txt_list) if re.search('\s*1\.', txt)]
        start_raw = jeoul_idx[0]

    ## 별표 및 별지 별도 추출
    ## 별표 및 별지가 없을 경우, 해당 텍스트 자체가 모두 raw_txt
    if len([i for i, txt in enumerate(txt_list) if re.search('(별표\s*및\s*별지)|(별표\s*목차)|(별지\s*목차)|(별표\s*및)|(별표\s*\/\s*서식)', txt)]) >= 2:
        start_pyo = [i for i, txt in enumerate(txt_list) if re.search('(별표\s*및\s*별지)|(별표\s*목차)|(별지\s*목차)|(별표\s*및)|(별표\s*\/\s*서식)', txt)]
        start_pyo = max(start_pyo)
        pyo_contents = [i for i, txt in enumerate(txt_list) if re.search('\〔별지|\[별지|\【별지|\〔별표|\[별표|\【별표|\〔별표\s*제?1호?\〕|\[별표\s*제?1호?\]|\【별표\s*제?1호?\】', txt)]

        raw_txt = txt_list[start_raw:start_pyo]
        pyo_txt = txt_list[max(pyo_contents):]

    elif len([i for i, txt in enumerate(txt_list) if re.search('(별표\s*및\s*별지)|(별표\s*목차)|(별지\s*목차)|(별표\s*및)|(별표\s*\/\s*서식)', txt)]) < 1:
        start_kook = [i for i, txt in enumerate(txt_list) if re.search('(육\s*군\s*참\s*모\s*총\s*장)|(국\s*방\s*부\s*장\s*관)', txt)]
        start_kook = max(start_kook)
        pyo_contents = [i for i, txt in enumerate(txt_list) if re.search('\〔별지|\[별지|\【별지|\〔별표|\[별표|\【별표|\〔별표\s*제?1호?\〕|\[별표\s*제?1호?\]|\【별표\s*제?1호?\】', txt)]

        raw_txt = txt_list[start_raw:start_kook]
        pyo_txt = txt_list[max(pyo_contents):]
    else:
        raw_txt = txt_list[start_raw:]
        pyo_txt = []
        
    ## 번호에 따라 분할하기
    ## 그리고 그 번호를 조로 변환하기
    raw_txt = [txt for txt in raw_txt if txt!='\n']

    raw = []
    for txt in tqdm(raw_txt):
        if re.match('((\s*)\d+\.(.+)\s*(.+)\s*\n)|(부\s*칙)|(작\s*성\s*관)', txt):
            split_text = re.split(r'(\d+\.\s*[가-힣])', txt)  ## 편/장/절 중간에 조항이 있으면 쪼개기
            if len(split_text) >= 2:
                split_idx = [i for i, s in enumerate(split_text) if re.search(r'(\d+\.)',s)]
                for idx in sorted(split_idx, reverse=True):
                    split_text[idx+1] = split_text[idx] + split_text[idx+1]
                    del split_text[idx]
                split_text = [s for s in split_text if s]
                split_text = [re.sub(r'(\d+)\.\s*(.+)',r'제\1조(\2)', s) for s in split_text]
                raw.extend(split_text)
            else:
                raw.append(txt)
        else:
            split_text = re.split(r'(\d+\.\s*[가-힣])', txt)  ## 문장 중간에 조항이 있으면 쪼개기
            if len(split_text) >= 2:
                split_idx = [i for i, s in enumerate(split_text) if re.search(r'(\d+\.\s*[가-힣])',s)]
                for idx in sorted(split_idx, reverse=True):
                    split_text[idx+1] = split_text[idx] + split_text[idx+1]
                    del split_text[idx]
                split_text = [s for s in split_text if s]
                # raw 가 0일 경우
                if len(raw)==0:
                    raw.extend(split_text)
                else:
                    raw[-1] = "".join([raw[-1],split_text[0]])
                    split_text = [re.sub(r'(\d+)\.\s*(.+)',r'제\1조(\2)', s) for s in split_text]
                    raw.extend(split_text[1:])
            elif len(raw)==0:
                raw.append(txt)
            else:
                raw[-1] = "".join([raw[-1],txt])

    # 불필요한 값들 삭제
    for i in range(len(raw)):
        raw[i] = re.sub(r'제\s*(\d+)\s*(편|장|절|관)',r'제 \1\2 ',raw[i])        # 공백 (숫자) 절 공백 제외 (예. 제 3 편)
        raw[i] = re.sub(r'제(\d+)조의 (\d+)',r'제\1조의\2',raw[i])            # n조의 2와 같은 항목 통일성 유지
        raw[i] = re.sub(r'부(\s)*칙(\s)*',r'부칙',raw[i])                     # 부칙 사이 공백 제거
        raw[i] = re.sub(r'제(\d+)조\[(.*)\]',r'제\1조(\2)',raw[i])            # n조의 2와 같은 항목 통일성 유지
        raw[i] = re.sub('\s+',' ',raw[i])                                    # 공백이 여러개일 경우 한개만 둠
        raw[i] = re.sub('(\s)*\n',' ',raw[i])                                # \n은 띄어쓰기로 변환
        raw[i] = re.sub('(\s)*\)',')',raw[i])                                # \n은 띄어쓰기로 변환
        raw[i] = re.sub('·',' ',raw[i])                                      # ·와 같은 특수문자는 나중에 규칙을 혼란스럽게 만들 수 있어 제외
        raw[i] = re.sub('&#\d*;',' ',raw[i])                                 # 특수문자 제외
        raw[i] = re.sub(' \(삭제\) ','(삭제)',raw[i])                         # 삭제조항 공백 제거
        raw[i] = re.sub('-\s+(\d+)\s+-','',raw[i])                           # page numbering 삭제
        raw[i] = re.sub('^\d+-\d+$','',raw[i])                               # 페이지 넘버링만 있는 리스트 삭제
        raw[i] = re.sub(r'\s*작\s*성\s*관', r'작성관', raw[i])                # 작성관으로 변경
        raw[i] = re.sub(r'국\s*방\s*부\s*장\s*관', r'', raw[i])               # 이제 필요 없으니 삭제
        raw[i] = re.sub(r'조\((.+?)\((.+?)\)(.+?)\)',r'조(\1<\2>\3)',raw[i])  # 조 안에 중첩괄호 <>으로 바꾸기
        
    raw = [txt for txt in raw if txt] ## 빈 문자열 제거
    
    # 조를 뽑아내는 pattern
    pattern = r'제[0-9]{1,3}조(의\s*\d+\s*)?\s*\((.+?)\)|(부칙)|(작성관)'
    name_com = re.compile(pattern)

    # candidate pool jsonl 생성
    candidate_pool = []
    for i, txt in enumerate(raw):
        try:
            split_std = name_com.search(txt).span()[1]  # 이름과 제목 끊을 라인
            txt_dic = {
                'subject':txt[:split_std],
                'text':txt[split_std:],
                'reference': txt_file_name.replace('.txt','')
                }
            candidate_pool.append(txt_dic)
        except AttributeError:
            print(str(i)+'행의 "'+ txt + '" 문장을 확인해주세요.')
            pass
    
    if not os.path.isdir('./candidate_pool'):
        os.mkdir('./candidate_pool')
    with open('./candidate_pool/'+ txt_file_name.replace('.txt','.jsonl'),encoding='utf-8', mode="w") as file:
        for i in candidate_pool:
            file.write(json.dumps(i, ensure_ascii=False) + "\n")

# def gwan_loop(gwan_idx, raw, i): # 관이 있을때 loop
#     if len(gwan_idx) > 0:
#         for gwan_i, gwan in enumerate(gwan_idx):
#             if i > gwan and (gwan_i == len(gwan_idx) - 1 or i < gwan_idx[gwan_i + 1]):
#                 raw[i] = raw[gwan] + raw[i]
#                 break
#     return raw
    
# def jeoul_loop(jeoul_idx, gwan_idx, raw, i): # 절이 있을때 loop
#     if len(jeoul_idx) > 0:
#         for jeoul_i, jeoul in enumerate(jeoul_idx):
#             if i > jeoul and (jeoul_i == len(jeoul_idx) - 1 or i < jeoul_idx[jeoul_i + 1]):
#                 if jeoul+1 in gwan_idx:
#                     gwan_loop(gwan_idx, raw, i)
#                     raw[i] = raw[jeoul] + raw[i]
#                     break
#                 else: #관이 없는 경우
#                     raw[i] = raw[jeoul] + raw[i]
#                     break
#     else:
#         raw = gwan_loop(gwan_idx, raw, i)
#     return raw

# def jang_loop(jang_idx, jeoul_idx, gwan_idx, raw, i):
#     if len(jang_idx) > 0:
#         for jang_i, jang in enumerate(jang_idx):
#             # 현재 인덱스가 jang보다 크고, 다음 jang 인덱스가 현재 인덱스보다 크지 않은 경우
#             if i > jang and (jang_i == len(jang_idx) - 1 or i < jang_idx[jang_i + 1]):
#                 if jang+1 in jeoul_idx:
#                     jeoul_loop(jeoul_idx, gwan_idx, raw, i)
#                     raw[i] = raw[jang] + raw[i]
#                     break
#                 elif jang+1 in gwan_idx:
#                     gwan_loop(gwan_idx, raw, i)
#                     raw[i] = raw[jang] + raw[i]
#                     break
#                 else: # 절이 없는 경우
#                     raw[i] = raw[jang] + raw[i]
#                     break
#     else: 
#         raw = jeoul_loop(jeoul_idx, gwan_idx, raw, i)
#     return raw

# def pyeon_loop(pyeon_idx, jang_idx, jeoul_idx, gwan_idx, raw, i): # 편이 있을 때 loop
#     if len(pyeon_idx) > 0:
#         for pyeon_i, pyeon in enumerate(pyeon_idx):
#             if i > pyeon and (pyeon_i == len(pyeon_idx) - 1 or i < pyeon_idx[pyeon_i + 1]):
#                 if pyeon+1 in jang_idx:
#                     jang_loop(jang_idx, jeoul_idx, gwan_idx, raw, i)
#                     raw[i] = raw[pyeon] + raw[i]
#                     break
#                 elif pyeon+1 in jeoul_idx:
#                     jeoul_loop(jeoul_idx, gwan_idx, raw, i)
#                     raw[i] = raw[pyeon] + raw[i]
#                     break
#                 else:
#                     raw[i] = raw[pyeon] + raw[i]
#     else: 
#         raw = jang_loop(jang_idx, jeoul_idx, gwan_idx, raw, i)
#     return raw