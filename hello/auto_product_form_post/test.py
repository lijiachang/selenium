common_form = """timesend: 2021-10-12 21:10:03
access_key: 6165892ba9d32
info[title]: 利津县115平的房子装修大概多少钱
info[seo_title]: 利津县115平的房子装修大概多少钱
info[keywords]: 利津县,115,平,房子,装修,大概,多少钱
info[description]: 前50字符
submit1: ok
info[id]: 51
is_auto_save: 1
info[status]: 
http_referer: http://{0}/index.php?m=site&c=content&a=product_index
status: 1
cat_id[]: 4
copy_id: 
tag_content: ,3369,3370,3371,3372,3373,3374,3375
info[filename]: 
info[listorder]: 
iscopy: 0
content: <p>一平方600到1000!也就是7万到12万左右!</p>"""


def get_headers(header_raw):
    """
    通过原生请求头获取请求头字典
    :param header_raw: {str} 浏览器请求头
    :return: {dict} headers
    """
    tmp_list = []
    for line in header_raw.split("\n"):
        line_s = line.strip().split(": ", 1)
        tmp_list.append(line_s if len(line_s) == 2 else line_s + [''])
    print(tmp_list)
    return dict(tuple(tmp_list))


print(get_headers(common_form))
