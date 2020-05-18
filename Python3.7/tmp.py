keyword = "'123"
keyword = keyword[1:-1] if keyword.startswith("'") and keyword.endswith("'") else keyword

print(keyword)