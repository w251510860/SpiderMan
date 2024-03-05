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
    "_gat": "1",
    "bm_sv": "4F2461F8AD7A3311DDEB04EA5461F7E3~YAAQHjArF+sKFDOGAQAAn3V1pxI/SLmnp7j2U5idI3XgVeOaOLbGcH0KTwBL0Ntihiid6Jz8DWM4LgI/k6kOcPa31C5NIUSrjnYGfHMfP8xQN2D9mxeJlDSFgLna36JGCbeIKtLYqdgHBVo1UnEqeWifaZRadYSB8QHPkmmbB5J5jneBgHvOYHFTVLwSlU+y/xks6ud32jJFUdWZiebfUkAzOLNmE0TyDpuS2OabBIDUFqDSTJmHXeu55KLB~1",
    "_ga": "GA1.2.1235384675.1677844064",
    "_ga_Q3MDF068TF": "GS1.1.1677846693.2.1.1677846745.8.0.0"
}
url = "https://myaccount.ea.com/cp-ui/security/sendMFACode"
data = {
    "mfa_type": "EMAIL"
}
response = requests.post(url, headers=headers, cookies=cookies, data=data)

print(response.text)
print(response)