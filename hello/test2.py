

import re
import chardet


with open('cafe.txt', 'w', encoding='utf-8') as f:
    print(f)
    f.write('café')

with open('cafe.txt', 'rb') as f:
    b = f.read()
    print(chardet.detect(b)) # 中文