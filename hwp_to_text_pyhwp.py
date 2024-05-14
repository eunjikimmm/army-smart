import os
# import win32com.client as win32

import_path = './test_folder/' ## hwp 파일 저장된 경로 (폴더)
convert_path = './txt_folder' ## text 파일 저장되어야 하는 경로 (폴더)
exefile = 'hwp5txt'

## 한글파일 txt로 변환해서 저장

res = []
for root, dirs, files in os.walk(import_path):
    # rootpath = os.path.join(os.path.abspath(import_path), root)
    import_rootpath = os.path.abspath(import_path)
    convert_rootpath = os.path.abspath(convert_path)

    for file in files:
        import_file_path = os.path.join(import_rootpath, file)
        convert_file_path = os.path.join(convert_rootpath, file[:-4]+".txt")
        output = '--output ' + '"' + convert_file_path + '"'
        result = '"' + import_file_path + '"'
        print(exefile + ' ' + output + ' ' + result)
        os.system(exefile + ' ' + output + ' ' + result)