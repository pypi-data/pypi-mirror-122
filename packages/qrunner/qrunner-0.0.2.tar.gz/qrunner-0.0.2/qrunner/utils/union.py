import json
import requests

host = 'https://ips-sso-pre.qizhidao.com'


def get_sms(phone):
    url = f'{host}/v1/security/inner/login_password'
    print(f'请求: {url}')
    headers = {
        'Content-Type': 'application/json'
    }
    params = {
        'clientId': '9304622189680257',
        'username': 'admin',
        'password': 'Qzd_WZ123!@#'
    }
    s = requests.Session()
    res = s.post(url, headers=headers, data=json.dumps(params), verify=False)
    print(res.text)

    url = f'{host}/v1/common/sms/sent/page/list/1/20'
    print(f'请求: {url}')
    params = {
        "contentType": "",
        "messageStatus": "",
        "phone": phone,
        "platform": "",
        "sendDate": "",
        "templateCodeRef": ""
    }
    headers = {
        'Content-Type': 'application/json'
    }
    res = s.post(url, headers=headers, data=json.dumps(params), verify=False)
    print(res)
    try:
        sms_code = res.json().get('data').get('list')[0].get('contentCode')
    except Exception as e:
        print(f'获取验证码失败: {e}')
        sms_code = None
    print(f'sms_code: {sms_code}')
    return sms_code


if __name__ == '__main__':
    get_sms('13652435335')
