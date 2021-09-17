import pandas as pd

df = pd.read_excel('doc.xlsx')  # 这个会直接默认读取到这个Excel的第一个表单

ratingB_counts = df['ratingB'].value_counts()
ratingB_counts_dict = ratingB_counts.to_dict()
print("统计ratingB数据：\n{0}".format(ratingB_counts_dict))


def not_null(s):
    return str(s) != 'nan'


def is_null(s):
    return str(s) == 'nan'


# 去年ratingA有评级，今年ratingB没有评级
withdraw_filter = df.loc[df['ratingA'].apply(not_null)].loc[df['ratingB'].apply(is_null)]
withdraw_filter_counts_dict = withdraw_filter['ratingA'].value_counts().to_dict()
print(withdraw_filter)
print(withdraw_filter_counts_dict)

# 去年ratingA为任意评级（或无），今年ratingB为评级9
ratingB_9_filter = df.loc[df['ratingB'].apply(lambda x: str(x).strip() == '9')]
ratingB_9_filter_counts_dict = ratingB_9_filter['ratingA'].value_counts().to_dict()

print(ratingB_9_filter)
print(ratingB_9_filter_counts_dict)

# 制作索引
BRR = [' '.join((n, x)) for n in ('1', '2', '3', '4', '5') for x in ('A', 'B', 'C')]
BRR = [0] + BRR + [x for x in range(6, 10)]
BRR_str = [str(x) for x in BRR]

# 数据输出
EDA = ['' for _ in range(len(BRR))]

ToTal = [ratingB_counts_dict.get(rating_number, 0) for rating_number in BRR]

CRE_nr = [withdraw_filter_counts_dict.get(rating_number, '') for rating_number in BRR]

CRE_def = [ratingB_9_filter_counts_dict.get(rating_number, '') for rating_number in BRR]

#汇总
data = {'BRR': BRR_str, 'EAD$': EDA, 'ToTal #': ToTal, 'CRE_nr': CRE_nr, 'CRE_def': CRE_def}
output = pd.DataFrame(data)

# 居中格式化，但是没起作用？
d = dict(selector="th",
         props=[('text-align', 'center')])
output.style.set_properties(**{'width': '10em', 'text-align': 'center'}).set_table_styles([d])

# 输出到excel
print(output)
output.to_excel('out.xlsx', index=False)
