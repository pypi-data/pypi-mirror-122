import hashlib
import random
import requests
import json
import time

# ---------------------------------------------------登录相关-------------------------------------------------------------


# 获取当前时间戳
def gen_timestamp(length=None):
    timestamp = str(int(time.time())) + '000'
    if length:
        timestamp = timestamp[:length]
    return timestamp


# 未登录时signature的生成算法，根据接口请求所有value值拼成的列表生成
def gen_sig_logout(param_value_list):
    # 对参数值列表进行排序然后转成字符串
    list1 = param_value_list
    list1.sort()
    str2 = ''.join(list1)
    # 先用md5进行加密
    # input_name = hashlib.md5(str2.encode("utf-8"))
    # md5_value = input_name.hexdigest()
    # 再用sha1进行加密
    sha1_value = hashlib.sha1(str2.encode('utf-8'))
    signature = sha1_value.hexdigest()
    return signature


# 生成六位随机字符串
def gen_random_str():
    random_str = ""
    for i in range(6):
        num = random.randint(0, 9)  # 取数字
        small_letter = chr(random.randint(97, 122))  # 取小写字母
        big_letter = chr(random.randint(65, 90))  # 取大写字母
        random_str += str(random.choice([num, small_letter, big_letter]))
    return random_str


# 生成已登录时的signature，根据token和param_sig生成
def gen_sig_login(access_token, param_sig):
    # 随机生成六位字符串param
    param = gen_random_str()
    # md5加密param
    param_md5 = (hashlib.md5(param.encode("utf-8"))).hexdigest()
    # 生成加密密钥
    sig = param_md5 + access_token + param_sig
    sig_md5 = (hashlib.md5(sig.encode("utf-8"))).hexdigest()
    # 生成传输私钥
    signature = f'{sig_md5}.{param}'
    return signature


def login():
    url = f'{host}/api/qzd-bff-operation/qzd/v1/account/login'
    print(f'请求: {url}')
    params = {"account": "admin", "password": "f057a419496bda4bdad4862a4b6173b9", "time": gen_timestamp()}
    # print(params)
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'signature': gen_sig_logout(list(params.values()))
    }
    # print(headers)
    res = requests.post(url, headers=headers, data=json.dumps(params), verify=False)
    print(res.text)
    data = res.json().get('data')
    token = data.get('token')
    param_sig = data.get('paramSig')
    return token, param_sig


# 通过接口登录获取token，然后生成sig
def get_token_sig():
    token, param_sig = login()
    signature = gen_sig_login(token, param_sig)
    return token, signature

# -------------------------------------------------企业认证相关-----------------------------------------------------------


# 通过手机号查询审批id
def search_company_authId(phone):
    url = f'{host}/api/qzd-bff-operation/qzd/v1/operation/companyAuth/queryCompanyAuth'
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'signature': signature,
        'accessToken': token
    }
    params = {"searchKey": phone, "current": 1, "pageSize": 10}
    r = requests.post(url, headers=headers, data=json.dumps(params))
    # print(r.text)
    try:
        auth_id = r.json().get('data').get('records')[0].get('id')
        # logger.info(f'公司认证id: {auth_id}')
    except Exception as e:
        # logger.info(f'查询公司认证id失败: {str(e)}')
        auth_id = None
    return auth_id


# 通过手机号驳回企业认证审核
def refuse_company_auth(phone):
    # 通过手机号查询审批id
    auth_id = search_company_authId(phone)

    # 通过审批id驳回审批
    url = f'{host}/api/qzd-bff-operation/qzd/v1/operation/companyAuth/authApprove'
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'signature': signature,
        'accessToken': token
    }
    params = {"id": auth_id, "approverRemarks": "测试拒绝", "result": 2}
    r = requests.post(url, headers=headers, data=json.dumps(params))
    # logger.info(r.text)


# 通过手机号通过企业认证审批
def agree_company_auth(phone):
    # logger.info(f'手机号: {phone}')
    # 通过手机号查询审批id
    auth_id = search_company_authId(phone)

    # 通过审批id同意审批
    url = f'{host}/api/qzd-bff-operation/qzd/v1/operation/companyAuth/authApprove'
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'signature': signature,
        'accessToken': token
    }
    params = {"id": auth_id, "approverRemarks": "测试通过", "result": 1}
    r = requests.post(url, headers=headers, data=json.dumps(params))
    # logger.info(r.text)

# ----------------------------------------------版本升级相关--------------------------------------------------------------


# ios企业端新增版本
def add_ios_ent(version, update_method):
    # update_method 0-不更新、1-强制更新、2-手动更新
    info_dict = {
        'version': version,
        'update_method': update_method,
        'download_url': 'https://apps.apple.com/cn/app/id1411199252',
        'platform': 1
    }
    _add_version(info_dict)


# ios员工端新增版本
def add_ios_emp(version, update_method):
    # update_method 0-不更新、1-强制更新、2-手动更新
    info_dict = {
        'version': version,
        'update_method': update_method,
        'download_url': 'https://apps.apple.com/cn/app/id1411199252',
        'platform': 11
    }
    _add_version(info_dict)


# 安卓企业端新增版本
def add_adr_ent(version, version_code, download_url, update_method):
    # update_method 0-不更新、1-强制更新、2-手动更新
    info_dict = {
        'version': version,
        'version_code': version_code,
        'update_method': update_method,
        'download_url': download_url,
        'platform': 2
    }
    _add_version(info_dict)


# 安卓员工端新增版本
def add_adr_emp(version, version_code, download_url, update_method):
    # update_method 0-不更新、1-强制更新、2-手动更新
    info_dict = {
        'version': version,
        'version_code': version_code,
        'update_method': update_method,
        'download_url': download_url,
        'platform': 10
    }
    _add_version(info_dict)


# 新增版本配置并上线
def _add_version(info_dict):
    version = info_dict.get('version')
    version_code = ''
    update_method = info_dict.get('update_method')  # update_method 0-不更新、1-强制更新、2-手动更新
    platform = info_dict.get('platform')  # 2-安卓、1-ios
    if platform in [2, 10]:
        version_code = info_dict.get('version_code')
    download_url = info_dict.get('download_url')

    update_text = '123456789012345678901234567890123456789012345678901234567890123456'
    if update_method == 0:
        update_text = '不更新' + update_text
    elif update_method == 1:
        update_text = '强制更新' + update_text
    elif update_method == 2:
        update_text = '手动更新' + update_text
    print(update_text)

    url = f'{host}/api/qzd-bff-operation/app/v1/version/addOrUpdate'
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'signature': signature,
        'accessToken': token
    }
    params = {
        "version": version,
        "updateTime": 1627660800000,
        "description": f"<p>{update_text}</p>",
        "platform": platform,
        "publisher": "admin",
        "downloadUrl": download_url,
        "updateMethod": update_method,
        "anewLoginFlag": "",
        "popUp": update_text,
        "status": 1
    }
    print(f'参数:\n{params}')
    if platform in [2, 10]:
        params['versionCode'] = version_code
    r = requests.post(url, headers=headers, data=json.dumps(params))
    print(f'响应数据: {r.text}')
    res_data = r.json()
    code = res_data.get('code')
    if code == 0:
        print('新增配置成功')
    else:
        print(f'新增配置失败: {res_data.get("msg")}')
        raise AssertionError(f'新增配置失败: {res_data.get("msg")}')


# 获取新增的版本id
def _get_version_id(vid):
    print('获取新增的版本id:')
    url = f'{host}/api/qzd-bff-operation/app/v1/version/getUpdateInfoPage'
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'signature': signature,
        'accessToken': token
    }
    params = {
        'current': 1,
        'pageSize': 10,
        'platform': 0
    }
    r = requests.post(url, headers=headers, data=json.dumps(params))
    # print(r.text)
    record_list = r.json().get('data').get('records')
    # print(record_list)
    record_id_list = []
    for record in record_list:
        _version = record.get('version')
        if _version == vid:
            record_id = record.get('id')
            record_id_list.append(record_id)
    print(f'record_id: {record_id_list}')
    return record_id_list


# 下线版本
def _offline_version(version_id_list):
    for version_id in version_id_list:
        url = f'{host}/api/qzd-bff-operation/app/v1/version/onlineOffline'
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'signature': signature,
            'accessToken': token
        }
        params = {
            'id': version_id,
            'status': 0
        }
        r = requests.post(url, headers=headers, data=json.dumps(params))
        print(r.text)


# 删除版本
def _delete_version(version_id_list):
    for version_id in version_id_list:
        url = f'{host}/api/qzd-bff-operation/app/v1/version/deleteUpdateInfo'
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'signature': signature,
            'accessToken': token
        }
        params = {
            'id': version_id
        }
        r = requests.post(url, headers=headers, data=json.dumps(params))
        print(r.text)


# 下线并删除版本记录
def delete_version(vid):
    vid_list = _get_version_id(vid)
    _offline_version(vid_list)
    _delete_version(vid_list)

# --------------------------------------------------初始化数据------------------------------------------------------------


host = 'https://yunying-pre.qizhidao.com'
token, signature = get_token_sig()


if __name__ == '__main__':
    version = '1.1.1'
    version_code = '123456'
    download_url = 'https://www.baidu.com'
    add_ios_ent(version, 0)
    add_ios_emp(version, 1)
    add_adr_ent(version, version_code, download_url, 1)
    add_adr_emp(version, version_code, download_url, 2)

