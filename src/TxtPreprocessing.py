#!/bin/env python
# -*- coding: utf-8 -*-

# from PyPDF2 import PdfReader
# import src.ConvertPdftoTxt as cpt
# from tqdm import tqdm
import os, sys
import re
import json


def preprocessing(text, file_path):
    # 기존 txt파일 input부분을 원pdf 읽는 걸로 바꿈
    print(file_path)
    file_name = os.path.basename(file_path)
    print(file_name)
    txt_file_name = file_name
    # 텍스트를 \n 기준으로 리스트화
    txt_list = [line + '\n' for line in text.split('\n') if line]

    # ## 로마자가 있는 경우, 장으로 바꾸고, 아날로그 숫자만 있는 경우 조로 바꾸기
    # def roman_to_int(s):
    #     roman_numerals = {'Ⅰ': 1, 'Ⅱ': 2, 'Ⅲ': 3, 'Ⅳ': 4, 'Ⅴ': 5, 'Ⅵ': 6, 'Ⅶ': 7, 'Ⅷ': 8, 'Ⅸ': 9, 'Ⅹ': 10}
    #     return roman_numerals.get(s, 0)
    #
    # if len([txt for txt in txt_list if re.match(r'제\s*\d+\s*조(\(|\[)', txt)]) < 1:
    #     transformed_list = []
    #
    #     for txt in txt_list:
    #         # 정규식 패턴으로 - 숫자 - 찾아서 먼저 삭제
    #         txt = re.sub(r'(\-\s+(\d{1,2})\s+\-\s*)', r'', txt)
    #
    #         # 정규식 패턴으로 로마 숫자를 포함하는 행 찾기
    #         roman_pattern = r'\s*(Ⅰ|Ⅱ|Ⅲ|Ⅳ|Ⅴ|Ⅵ|Ⅶ|Ⅷ|Ⅸ|Ⅹ)\.\s*.*\n'
    #         match = re.match(roman_pattern, txt)
    #         if match:
    #             roman_numeral = match.group(1)
    #             arabic_numeral = roman_to_int(roman_numeral)
    #             # 로마 숫자를 "제 {숫자} 장" 형태로 교체
    #             # 아라빅 숫자를 "제 {숫자} 조" 형태로 교체
    #             txt = re.sub(r'\s*(Ⅰ|Ⅱ|Ⅲ|Ⅳ|Ⅴ|Ⅵ|Ⅶ|Ⅷ|Ⅸ|Ⅹ)\.', fr'제{arabic_numeral}장', txt)
    #             # txt = re.sub(r'\-\s*\d+\s*\-\s*(Ⅰ|Ⅱ|Ⅲ|Ⅳ|Ⅴ|Ⅵ|Ⅶ|Ⅷ|Ⅸ|Ⅹ)\.', fr'제{arabic_numeral}장', txt)
    #             txt = re.sub(r'(\s*)(\d+)\.\s*(.+)\n', r' 제\2조(\3)\n', txt)
    #             # txt = re.sub(r'(-\s*\d+\s*-)\s*(\d+)\.?\s*(\w+)\n', r' 제\2조(\3)\n', txt)
    #             transformed_list.append(txt)
    #         else:
    #             txt = re.sub(r'(\s*)(\d+)\.(.+)\n', r'\1제\2조(\3)\n', txt)
    #             txt = re.sub(r'.+(\-\s*\d+\s*\-)\s*(\d+)\.?(.+)\n', r' 제\2조(\3)\n', txt)
    #             transformed_list.append(txt)
    #
    #     txt_list = transformed_list
        # print(txt_list)

    ## 목차를 지우고 내용만 추출
    ## 조항 내용 / 별표와 별지 따로 리스트 생성
    import pdb; pdb.set_trace()
    if len([i for i, txt in enumerate(txt_list) if re.search('제\s*1\s*편', txt)]) >= 2:
        jeoul_idx = [i for i, txt in enumerate(txt_list) if re.search('제\s*1\s*편', txt)]
        start_raw = jeoul_idx[1]
    elif len([i for i, txt in enumerate(txt_list) if re.search('(제\s*1\s*장)', txt)]) >= 2:
        jeoul_idx = [i for i, txt in enumerate(txt_list) if re.search('(제\s*1\s*장)', txt)]
        start_raw = jeoul_idx[1]
    elif len([i for i, txt in enumerate(txt_list) if re.search('(제\s*1\s*장)', txt)]) == 1:
        jeoul_idx = [i for i, txt in enumerate(txt_list) if re.search('(제\s*1\s*장)', txt)]
        start_raw = jeoul_idx[0]
    else:
        jeoul_idx = [i for i, txt in enumerate(txt_list) if re.search('(제\s*1\s*조)', txt)]
        if len(jeoul_idx) > 1:
            start_raw = jeoul_idx[1]
        else:
            start_raw = jeoul_idx[0]

    ## 별표 및 별지 별도 추출
    ## 별표 및 별지가 없을 경우, 해당 텍스트 자체가 모두 raw_txt
    if len([i for i, txt in enumerate(txt_list) if re.search('(국\s+방\s+부\s+장\s+관)|(육\s+군\s+참\s+모\s+총\s+장)|(제\s+9\s+보\s+병\s+사\s+단(\s+장)?)|(내\s+용\s+끝)', txt)]) >= 1:
        start_kook = [i for i, txt in enumerate(txt_list) if re.search('(국\s+방\s+부\s+장\s+관)|(육\s+군\s+참\s+모\s+총\s+장)|(제\s+9\s+보\s+병\s+사\s+단(\s+장)?)|(내\s+용\s+끝)', txt)]
        start_kook = min(start_kook)
        # pyo_contents = [i for i, txt in enumerate(txt_list) if re.search('\〔별표|\[별표|\【별표|\〔별표\s*제?1호?\〕|\[별표\s*제?1호?\]|\【별표\s*제?1호?\】', txt)]

        raw_txt = txt_list[start_raw:start_kook]
        # pyo_txt = txt_list[max(pyo_contents):]


    elif len([i for i, txt in enumerate(txt_list) if re.search('(국\s+방\s+부\s+장\s+관)|(육\s+군\s+참\s+모\s+총\s+장)|(제\s+9\s+보\s+병\s+사\s+단(\s+장)?)|(내\s+용\s+끝)', txt)]) == 0:
        start_pyo = [i for i, txt in enumerate(txt_list) if re.search('(별\s*표\s*및\s*별\s*지)|(별\s*표\s*목\s*차)|(별\s*지\s*목\s*차)|(별표\s*및)|(별표\s*\/\s*서식)|(별\s*지\s*서\s*식\s*목\s*록)', txt)]
        if len(start_pyo) >= 2:
            start_pyo = start_pyo[1]
        elif len(start_pyo) == 1:
            start_pyo = start_pyo[0]
        else:
            start_pyo = None
        # pyo_contents = [i for i, txt in enumerate(txt_list) if re.search('\〔별표|\[별표|\【별표|\〔별표\s*제?1호?\〕|\[별표\s*제?1호?\]|\【별표\s*제?1호?\】', txt)]

        raw_txt = txt_list[start_raw:start_pyo]
        # pyo_txt = txt_list[max(pyo_contents):]
    #
    # else:
    #     start_buchik = [i for i, txt in enumerate(txt_list) if re.search('(\s*부\s*칙)', txt)]
    #     start_buchik = min(start_buchik)
    #     # pyo_contents = [i for i, txt in enumerate(txt_list) if re.search('\〔별표|\[별표|\【별표|\〔별표\s*제?1호?\〕|\[별표\s*제?1호?\]|\【별표\s*제?1호?\】', txt)]
    #
    #     raw_txt = txt_list[start_raw:start_buchik]
    #     # pyo_txt = []

    # 입력 데이터 전처리 (불필요한 빈 줄 제거 및 <삭제>, <삭 제>를 (삭제)로 변환)
    def preprocess_text(raw_txt):
        processed_txt = []
        for txt in raw_txt:
            if txt != '/n':
                txt = txt.replace('<삭제>', '(삭제)')
                txt = re.sub(r'<삭\s*제>', '(삭제)', txt)
                processed_txt.append(txt)
        return processed_txt

    def split_clause(text):
        pattern = r'(제\s*(\d+)\s*조\s*(의?\s*\d+)?(\s*\(|\s*\[))'
        split_text = re.split(pattern, text)
        split_text = [s for s in split_text if s]  # 빈 문자열 제거
        return split_text

    raw_txt = preprocess_text(raw_txt)
    raw = []
    processed_clauses = set()

    for txt in raw_txt:
        if re.match(r'(\s*)(제\s*[0-9]+\s*편|제\s*[0-9]+\s*장|제\s*[0-9]+\s*절|제\s*[0-9]+\s*관|제\s*[0-9]+\s*조(의?\s*\d+\s*)?\s*(\(|\<|\[)([^)]+|[^>]+|[^]]+)(\)|\>|\])|제\s*[0-9]+\s*조(의?\s*\d+\s*)?(\s*\(삭\s*제\))|\s*부\s*칙|(작\s*성\s*(관|자)|\s*작\s*성\s*책\s*임\s*(관|자)|\s*작\s*성\s*담\s*당\s*(관|자)))',txt):
            split_text = split_clause(txt)
            if len(split_text) >= 6:
                for idx in range(0, len(split_text), 6):
                    clause_num = split_text[idx + 1]  # 조항 번호
                    if clause_num not in processed_clauses:
                        processed_clauses.add(clause_num)
                        if idx == 0:
                            raw.append("".join(split_text[idx:idx + 6]))
                        else:
                            raw[-1] += split_text[idx]
                            raw.append("".join(split_text[idx + 1:idx + 6]))
                    else:
                        raw[-1] += "".join(split_text[idx:idx + 6])
            else:
                raw.append(txt)
        else:
            split_text = split_clause(txt)
            if len(split_text) >= 6:
                for idx in range(0, len(split_text), 6):
                    clause_num = split_text[idx + 1]  # 조항 번호
                    if clause_num not in processed_clauses:
                        processed_clauses.add(clause_num)
                        if idx == 0:
                            raw.append("".join(split_text[idx:idx + 6]))
                        else:
                            raw[-1] += split_text[idx]
                            raw.append("".join(split_text[idx + 1:idx + 6]))
                    else:
                        raw[-1] += "".join(split_text[idx:idx + 6])
            elif len(raw) == 0:
                raw.append(txt)
            else:
                raw[-1] += txt

    # 각 섹션의 마지막 번호를 추적하기 위한 변수
    last_pyeon = 0
    last_jang = 0
    last_jeoul = 0
    last_gwan = 0

    pyeon_idx = []
    jang_idx = []
    jeoul_idx = []
    gwan_idx = []
    buchik_idx = []
    editor_idx = []

    for i, txt in enumerate(raw):
        if re.match(r'.*(제\s*[0-9]+\s*편)', txt):
            current_pyeon = int(re.search(r'제\s*([0-9]+)\s*편', txt).group(1))
            if current_pyeon == last_pyeon + 1:
                raw[i] = re.sub(r'.*(제)(\s*[0-9]+\s*)(편)', r'제\2편', txt)
                pyeon_idx.append(i)
                last_pyeon = current_pyeon
                # 새로운 편이 시작되면 장,절,관의 카운터 초기화
                last_jang = 0
                last_jeoul = 0
                last_gwan = 0
        elif re.match(r'.*(제\s*[0-9]+\s*장)', txt):
            current_jang = int(re.search(r'제\s*([0-9]+)\s*장', txt).group(1))
            if current_jang == last_jang + 1:
                raw[i] = re.sub(r'.*(제)(\s*[0-9]+\s*)(장)', r'제\2장', txt)
                jang_idx.append(i)
                last_jang = current_jang
                # 새로운 장이 시작되면 절,관의 카운터 초기화
                last_jeoul = 0
                last_gwan = 0
        elif re.match(r'.*(제\s*[0-9]+\s*절)', txt):
            current_jeoul = int(re.search(r'제\s*([0-9]+)\s*절', txt).group(1))
            if current_jeoul == last_jeoul + 1:
                raw[i] = re.sub(r'.*(제)(\s*[0-9]+\s*)(절)', r'제\2절', txt)
                jeoul_idx.append(i)
                last_jeoul = current_jeoul
                # 새로운 절이 시작되면 관의 카운터 초기화
                last_gwan = 0
        elif re.match(r'.*(제\s*[0-9]+\s*관)', txt):
            current_gwan = int(re.search(r'제\s*([0-9]+)\s*관', txt).group(1))
            if current_gwan == last_gwan + 1:
                raw[i] = re.sub(r'.*(제)(\s*[0-9]+\s*)(관)', r'제\2관', txt)
                gwan_idx.append(i)
                last_gwan = current_gwan
        elif re.match(r'\s*\t*부\t*\s*칙\s*', txt):
            buchik_idx.append(i)
        elif re.match(r'\s*작\s*성\s*(관|자)|\s*작\s*성\s*책\s*임\s*(관|자)|\s*작\s*성\s*담\s*당\s*(관|자)',
                      txt):  # ' 작성관'인 파일도 있어 패턴 \s* 추가
            editor_idx.append(i)

    ## 편, 장, 절을 조 앞에 붙이기
    for i in range(len(raw)):
        flag = False
        if i not in gwan_idx + jang_idx + jeoul_idx + pyeon_idx + buchik_idx:
            try:
                if i < buchik_idx[0]: ## 부칙은 끝쪽에 있으니 그 전에
                    raw = pyeon_loop(pyeon_idx, jang_idx, jeoul_idx, gwan_idx, raw, i)
                    if re.search('(제\s*(\d+)\s*조\s*\(|제\s*(\d+)\s*조\s*\[|제\s*(\d+)\s*조\s*(의?\s*(\d+))?\s*\(|제\s*(\d+)\s*조\s*(의?\s*(\d+))?\s*\[)', raw[i]) is None:
                        raw[i] = ''
                else:    ## 부칙 있는 부분
                    for buchik_i, buchik in enumerate(buchik_idx):
                        if (i > buchik) and (i > buchik_idx[buchik_i + 1]): continue
                        if i > buchik or i == (len(buchik_idx) - 1):
                            raw[i] = raw[buchik] + raw[i]
                        else: break
            except IndexError:
                pass
            try:
                for editor_i, editor in enumerate(editor_idx):
                    if (i > editor) and (i > editor_idx[editor_i + 1]): continue
                    if i > editor:
                        raw[i] = raw[editor] + raw[i]
                    else: break
            except IndexError:
                pass
        else: continue

    ## 편, 장, 절 만 있는 값 삭제
    raw = [txt for i, txt in enumerate(raw) if i not in gwan_idx + jang_idx + jeoul_idx + pyeon_idx]
    raw = [txt for txt in raw if txt]
    raw = [txt for txt in raw if not re.search('(부\s*\t*칙\s*?\n*$)|(부\s*\t*칙\n*?\s*$)|(부\s*\t*칙\n*\s*(\〈|\<|\().*\s*([0-9]{4}\.)?\s*[0-9]{1,2}\.\s*[0-9]{1,2}\.?\s*.*(\)|\>|\〉))\n*\s*$|(부\s*\t*칙\n*\s*(\〈|\<|\().*?\s*([0-9]{4}\.)?\s*[0-9]{1,2}\.\s*[0-9]{1,2}\.?\s*.*?(\)|\>|\〉))\s*\n*$', txt)]

    # 불필요한 값들 삭제
    for i in range(len(raw)):
        raw[i] = re.sub(r'제\s*(\d+)\s*(편|장|절|관)',r'제\1\2 ',raw[i])          # 공백 (숫자) 절 공백 제외 (예. 제 3 편)
        raw[i] = re.sub(r'제\s*(\d+)\s*조\s*(\()\s*', r'제\1조\2', raw[i])          # '제 n 조 ('와 같은 항목 통일성 유지
        raw[i] = re.sub(r'제\s*(\d+)\s*조\s*(\d+)\s*(\(|\<)',r'제\1조의\2\3',raw[i])     # '제n조의 n ('와 같은 항목 통일성 유지
        raw[i] = re.sub(r'제\s*(\d+)\s*조의\s*(\d+)\s*(\(|\<)',r'제\1조의\2\3',raw[i])     # '제n조의 n ('와 같은 항목 통일성 유지
        raw[i] = re.sub(r'제(\d+)조\s*(\d+)\s*(\(|\<)', r'제\1조의\2\3', raw[i])  # '제n조 n을 제n조의 n으로 통일
        raw[i] = re.sub(r'제(\d+)조\s*삭\s*제', r'제\1조(삭제)', raw[i])           # '제n조 삭제를 제n조(삭제)로 통일
        raw[i] = re.sub(r'제\s*(\d+)\s*조\s*<삭\s*제>', r'제\1조<삭제>', raw[i])           # '제n조 삭제를 제n조(삭제)로 통일
        raw[i] = re.sub(r'제(\d+)조\s*(\d+)\s*삭\s*제', r'제\1조의\2(삭제)', raw[i])           # '제n조 삭제를 제n조(삭제)로 통일
        raw[i] = re.sub(r'제(\d+)조의\s*(\d+)\s*삭\s*제', r'제\1조의\2(삭제)', raw[i])           # '제n조 삭제를 제n조(삭제)로 통일
        raw[i] = re.sub(r'\s*부\s*칙\s*',r'부칙', raw[i])                        # 부칙 사이 공백 제거
        raw[i] = re.sub(r'\t*부\t*칙\t*',r'부칙', raw[i])                        # 부칙 사이 공백 제거
        raw[i] = re.sub(r'제(\d+)조\[(.*)\]',r'제\1조(\2)',raw[i])               # n조의 2와 같은 항목 통일성 유지
        raw[i] = re.sub(r'[^\S\n]+',' ',raw[i])                                    # 공백 여러개일 경우 중 '\n'이 있을 때 공백 제거 후 '\n'은 유지
        raw[i] = re.sub('\s+\n','\n',raw[i])                                       # 줄바꿈 앞 공백 제거
        raw[i] = re.sub('\n\s+','\n',raw[i])                                       # 줄바꿈 뒷 공백 제거
        raw[i] = re.sub('^\s+','',raw[i])                                          # text의 첫 시작이 공백일 경우 제거
        raw[i] = re.sub('\s$','',raw[i])                                           # text의 끝이 공백일 경우 제거
        raw[i] = re.sub('\)\n',')',raw[i])                                         # 괄호 뒤 \n 제거
        raw[i] = re.sub('\>\n','> ',raw[i])                                         # 꺽새 뒤 \n 제거
        raw[i] = re.sub('\n제',' 제',raw[i])                                         # '제'단어 앞 \n 제거
        raw[i] = re.sub('\n$','',raw[i])                                         # text의 끝 '\n' 삭제
        raw[i] = re.sub('\n+','\n',raw[i])                                       # 줄바꿈이 여러개일 경우 한개만 둠
        raw[i] = re.sub('\((\s*)','(',raw[i])                                   # '( ' 공백 제거
        raw[i] = re.sub('(\s*)\)',')',raw[i])                                   # ' )' 공백 제거
        # raw[i] = re.sub('\s*\·\s*',' ',raw[i])                                  # ·와 같은 특수문자는 나중에 규칙을 혼란스럽게 만들 수 있어 제외
        raw[i] = re.sub('&#\d*;',' ',raw[i])                                    # 특수문자 제외:q:q
        raw[i] = re.sub(' \(삭제\) ','(삭제)',raw[i])                            # 삭제조항 공백 제거
        raw[i] = re.sub('-\s+(\d+)\s+-','',raw[i])                              # page numbering 삭제
        raw[i] = re.sub('^\d+\s*-\s*\d+$','',raw[i])                            # 페이지 넘버링만 있는 리스트 삭제
        raw[i] = re.sub(r'\s*작\s*성\s*(관|자)\s*:?\s*', r'작성관', raw[i])       # 작성관으로 통일
        raw[i] = re.sub(r'\s*작\s*성\s*담\s*당\s*(관|자)\s*:?\s*', r'작성관', raw[i])       # 작성관으로 통일
        raw[i] = re.sub(r'\s*작\s*성\s*책\s*임\s*(관|자)\s*:?\s*', r'작성관', raw[i])       # 작성관으로 통일
        raw[i] = re.sub(r'국\s+방\s+부\s+장\s+관', r'', raw[i])                  # 이제 필요 없으니 삭제
        raw[i] = re.sub(r'육\s+군\s+참\s+모\s+총\s+장', r'', raw[i])                  # 이제 필요 없으니 삭제
        raw[i] = re.sub(r'(제\s+9\s+보\s+병\s+사\s+단(\s+장)?)', r'', raw[i])                  # 이제 필요 없으니 삭제
        raw[i] = re.sub(r'(내\s+용\s+끝)', r'', raw[i])                  # 이제 필요 없으니 삭제
        raw[i] = re.sub(r'조\((.+?)\((.+?)\)(.+?)\)',r'조(\1<\2>\3)',raw[i])    # 조 안에 중첩괄호 <>으로 바꾸기
        raw[i] = re.sub(r'(\d*)\s*\.\s*(\d+)\s*\.\s*(\d+)\s*\.?', r'\1.\2.\3.', raw[i])  # nnnn.nn.nn. 으로 통일
        raw[i] = re.sub(r'(\s*사단행정예규\s*\d+\s*\-\s*\d+)', r'', raw[i])            # 불필요한 텍스트 제거
        raw[i] = re.sub(r'(\ž|\Ÿ)', r'-', raw[i])  # 불필요한 텍스트 제거
        raw[i] = re.sub(r'(\-\s+(\d{1})\s+\-\s*)', r'', raw[i])              # 페이지 쪽 번호 제거
        #raw[i] = re.sub(r'^(\d){1}\s*-\s*(\d){1}', r'', raw[i])              # 페이지 쪽 번호 제거

    raw = [txt for txt in raw if txt] ## 빈 문자열 제거

    # 조를 뽑아내는 pattern
    pattern = r'제\s*[0-9]+\s*조(의?\s*\d+\s*)?\s*(\(|\<)([^)]+|[^>]+|[^]]+)(\)|\>)|(부칙)|(작성관)'
    name_com = re.compile(pattern)

    # candidate pool jsonl 생성
    candidate_pool = []
    for i, txt in enumerate(raw):
        try:
            split_std = name_com.search(txt).span()[1]  # 이름과 제목 끊을 라인
            txt_dic = {
                'url': txt[:split_std],
                'text': txt[split_std:],
                'reference': txt_file_name.replace('.txt', '')
            }
            candidate_pool.append(txt_dic)
        except AttributeError:
            print(str(i) + '행의 "' + txt + '" 문장을 확인해주세요.')
            pass

    if not os.path.isdir(candipool_path):
        os.mkdir(candipool_path)
    with open(candipool_path + '/' + txt_file_name.replace('.pdf', '.jsonl'), encoding='utf-8', mode="w") as file:
        for i in candidate_pool:
            file.write(json.dumps(i, ensure_ascii=False) + "\n")


def gwan_loop(gwan_idx, raw, i):  # 관이 있을때 loop
    if len(gwan_idx) > 0:
        for gwan_i, gwan in enumerate(gwan_idx):
            if i > gwan and (gwan_i == len(gwan_idx) - 1 or i < gwan_idx[gwan_i + 1]):
                raw[i] = raw[gwan] + raw[i]
                break
    return raw


def jeoul_loop(jeoul_idx, gwan_idx, raw, i):  # 절이 있을때 loop
    if len(jeoul_idx) > 0:
        for jeoul_i, jeoul in enumerate(jeoul_idx):
            if i > jeoul and (jeoul_i == len(jeoul_idx) - 1 or i < jeoul_idx[jeoul_i + 1]):
                if jeoul + 1 in gwan_idx:
                    gwan_loop(gwan_idx, raw, i)
                    raw[i] = raw[jeoul] + raw[i]
                    break
                else:  # 관이 없는 경우
                    raw[i] = raw[jeoul] + raw[i]
                    break
    else:
        raw = gwan_loop(gwan_idx, raw, i)
    return raw


def jang_loop(jang_idx, jeoul_idx, gwan_idx, raw, i):
    if len(jang_idx) > 0:
        for jang_i, jang in enumerate(jang_idx):
            # 현재 인덱스가 jang보다 크고, 다음 jang 인덱스가 현재 인덱스보다 크지 않은 경우
            if i > jang and (jang_i == len(jang_idx) - 1 or i < jang_idx[jang_i + 1]):
                if jang + 1 in jeoul_idx:
                    jeoul_loop(jeoul_idx, gwan_idx, raw, i)
                    raw[i] = raw[jang] + raw[i]
                    break
                elif jang + 1 in gwan_idx:
                    gwan_loop(gwan_idx, raw, i)
                    raw[i] = raw[jang] + raw[i]
                    break
                else:  # 절이 없는 경우
                    raw[i] = raw[jang] + raw[i]
                    break
    else:
        raw = jeoul_loop(jeoul_idx, gwan_idx, raw, i)
    return raw


def pyeon_loop(pyeon_idx, jang_idx, jeoul_idx, gwan_idx, raw, i):  # 편이 있을 때 loop
    if len(pyeon_idx) > 0:
        for pyeon_i, pyeon in enumerate(pyeon_idx):
            if i > pyeon and (pyeon_i == len(pyeon_idx) - 1 or i < pyeon_idx[pyeon_i + 1]):
                if pyeon + 1 in jang_idx:
                    jang_loop(jang_idx, jeoul_idx, gwan_idx, raw, i)
                    raw[i] = raw[pyeon] + raw[i]
                    break
                elif pyeon + 1 in jeoul_idx:
                    jeoul_loop(jeoul_idx, gwan_idx, raw, i)
                    raw[i] = raw[pyeon] + raw[i]
                    break
                else:
                    raw[i] = raw[pyeon] + raw[i]
    else:
        raw = jang_loop(jang_idx, jeoul_idx, gwan_idx, raw, i)
    return raw