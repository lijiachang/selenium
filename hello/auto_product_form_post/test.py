
published_titles = {'key':2}  # 统计已发布的title和出现的次数

published_titles.setdefault('key', 0)
print(published_titles)
published_titles['key'] += 1
print(published_titles)
