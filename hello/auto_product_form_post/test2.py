import requests


def get_cookies(url):
    """"""

    resp = requests.get(url, timeout=5)
    cookie = {}
    for key, value in resp.cookies.items():
        cookie[key] = value
        print(f'{key}: {value}')
    security_session_verify = resp.cookies.get('security_session_verify')

    resp = requests.get(
        '{}{}'.format(url, '?security_verify_data=313932302c31303830'),
        cookies=cookie
    )

    for key, value in resp.cookies.items():
        cookie[key] = value
        print(f'{key}: {value}')
    security_session_mid_verify = resp.cookies.get('security_session_mid_verify')
    return security_session_verify, security_session_mid_verify


url = "http://www.chuangjiawang.com/admin/?index.html"
print(get_cookies(url))
