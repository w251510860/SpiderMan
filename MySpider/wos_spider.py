import datetime
import json
import time
import pandas as pd
from datetime import datetime
from datetime import timedelta
from datetime import timezone

from appium.webdriver.webdriver import WebDriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

headers = {
    "authority": "www.webofscience.com",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,la;q=0.6,ca;q=0.5,cy;q=0.4,ja;q=0.3,so;q=0.2,th;q=0.1,es;q=0.1,und;q=0.1,pt;q=0.1,lb;q=0.1,fr;q=0.1",
    "cache-control": "max-age=0",
    "referer": "https://access.clarivate.com/",
    "sec-ch-ua": "\"Not_A Brand\";v=\"99\", \"Google Chrome\";v=\"109\", \"Chromium\";v=\"109\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
}

cookies = {
    "WOSSID": "USW2EC0CEFXflnd3G8elZqnZEHYrB",
    "dotmatics.elementalKey": "SLsLWlMhrHnTjDerSrlG",
    "sessionid": "7iz9qgq7fpiyrvab3jl7vcrdgk0bxlbs",
    "OptanonAlertBoxClosed": "2023-02-20T09:35:51.561Z",
    "_abck": "20C13A30CF05887A569C3FA777251564~0~YAAQPFgDF/erq4eGAQAAsKudkAlRcaXydaVpOj376Tzc4zdadn5v/qWIpX+Bw9MUSjpz45PdcmdMTQaCdMQ61gcJ0RmtvWOtJMF2/M7re51UZemGDm/gsVj1DYq4j9zXt7ZmRS4L1pL77MFEc0PpkbX6z+kl7hOUtifce76dPaJpJMLHm6BXkS1P8gK0lb+aPtvWRwXK/YfLRVm8HjMD7HQEGB4acpD1CChhGvdOdFrhEul36jpalX08WhoMy8FbwTOnf4FONDlC9pMfYY5qOTRVnExzroqLOhk7uxYX7cOqgOsH6e3luyjwZME5YGeLFAfpfZ2VBs1LM4J4/CEERGU4+BVZDOdb7BwfgaV9njj2LfNcrJmJjxt4fXUP/fAKhrPU3Z7COd1o3q9AblFI5CqkQpmRJYs9d8yH2bIe~-1~-1~-1",
    "bm_sz": "B7ADA8536AA1D57C44CEDB0143CBA4C0~YAAQPFgDF/qrq4eGAQAAsKudkBJuW+SVX3qsSs9lXJ4+mbxpzXo140gwbDrBGZpiUVBnqmnyJCbw7x7CGCJlT4Vu2C0u3k3UKKldV8Mdd/Ho0dqtA/KE8fDHwXp/0ooRU2vMTJbD0CKLInrO6+gVnwbSn0k+hrWNHBUodcHAzYmMbdKQCuaz9Oy0yavV2Ib9EreNZEOfjqU30EL4jYFYNQ6sIE4HGeuuBkqukDx4nq7kGFRE8GgBVn2yEcUPmO6H63GKyx1K4fNqQBd/pCpSXOhQzeRAuK7zCXwf5+Cy9YpxvuwqSSapG6g=~3293752~3621937",
    "_sp_ses.840c": "*",
    "ak_bmsc": "54F88EB9CB68FB9E52C2A23C9B3B0346~000000000000000000000000000000~YAAQPFgDFxWsq4eGAQAAq72dkBKDzhF6TTVzfHKPn4Kz33s5nbFFiA/gEqYmDqj7vB2s2D/R1X3JfMPCy0SE8JaEWCWsv32FrOgQjJOO6VuP7Ss82eOdLsZzpM4erkA9rrDY6M5unb6/ObXgtmjlZ3t89j5V/BWSFvMiPgiKaVZJWc8ek90hc+eBCcr3KVb8Nv9UkpUd6lzAd5NQpxsOIeMseIlTmsIhqrSv2/aX3IVfHh0EiN73M0/BMj41/GFl4ufjy3NTwvNa8ySjQRqP8Vhs3bMZnHfrJSxpHj19Olffx8UkIop2+QkrT9eT9KRucmSE41/7AyVmu5cnFS/37+7Y8jnKDNZ7h+gRKQwCphdgbLr7NlPxClRqukHtCOaC0M1S84yS24XRUN7127sNDOU450ht2qK5lg6MJ2GlTPz4HNr8Mz4fd6OL7vVRs/dHXPHjsTCFObvj69eunyOxZ434ygTv1N68qFS9jtjtHH3RL6RRQt82Rzz5fmN0P628",
    "_sp_id.840c": "3a1b4863-80e8-4ecb-9cdf-5c8c7635556c.1676885746.8.1677465186.1677414358.34341fa4-6920-4f68-b4e5-95fd20bdd7a9.7ef9b077-ea95-4b5b-a2e8-e123471ba964.e48c0528-fd3d-4fe0-9449-d459e7142b64.1677463517913.18",
    "OptanonConsent": "isGpcEnabled=0&datestamp=Mon+Feb+27+2023+10%3A33%3A07+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=6.39.0&isIABGlobal=false&hosts=&consentId=d0fd0e36-638d-4725-a549-eb1e4db32cee&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0004%3A1%2CC0005%3A1%2CC0002%3A1&geolocation=HK%3BHWC&AwaitingReconsent=false",
    "bm_sv": "03681ACFB1AA06C2AC27225EEAAB7780~YAAQR2YzuL3XR42GAQAAhoW3kBLsdgXtaq0s9wzJ1kPbWFd5BGzb7gn5kjPKu2bY0ruQ+/z2ZFgC+MNfPm+NxrLYmM89lwewXPUMNp9MjeH5xIHwfBh86IbyF9W+Jw8jbtv9mx6GKHJuNXw9hCpjDOVtBwswl0jU5SWxfh9tCmEmbfPEYrOr6MAYBk/CyaObLF+SG7eie9sQR4urJ4HiprF7FPj/pyBlEVL+02P0IDQ7YLWRTTQwiVzQWbridyHn8l3dVSGyaw==~1",
    "RT": "\"z=1&dm=www.webofscience.com&si=e16913bd-b694-4871-ac13-51e3b1f4e585&ss=lem6gdsd&sl=7&tt=c9p&bcn=%2F%2F684d0d4c.akstat.io%2F&obo=1&ld=108xj&ul=119u6\""
}
# 1> 获取chrome参数对象
chrome_options = Options()
# 2> 添加无头参数r,一定要使用无头模式，不然截不了全页面，只能截到你电脑的高度
# chrome_options.add_argument('--headless')
# 3> 为了解决一些莫名其妙的问题关闭 GPU 计算
chrome_options.add_argument('--disable-gpu')
# 4> 为了解决一些莫名其妙的问题浏览器不动
chrome_options.add_argument('--no-sandbox')


def login(driver, u_name, password, url):
    driver.get(url)
    username = driver.find_element(By.XPATH, value='//input[@name="email"]')
    username.send_keys(u_name)
    time.sleep(2)
    pwd = driver.find_element(By.XPATH, value='//input[@name="password"]')
    pwd.send_keys(password)
    time.sleep(2.5)
    login = driver.find_element(By.XPATH, value='//button[@name="login-btn"]')
    login.send_keys(Keys.ENTER)
    time.sleep(5)


def search(driver: WebDriver, key_ward):
    retrieval = driver.find_element(By.XPATH, value='//input[@name="search-main-box"]')
    retrieval.send_keys(key_ward)
    confirm = driver.find_element(By.XPATH, value='//button[@type="submit"]')
    confirm.send_keys(Keys.ENTER)
    time.sleep(5)
    return driver


def scroll_(driver: WebDriver):
    # 执行这段代码，会获取到当前窗口总高度
    js = "return action=document.body.scrollHeight"
    # 初始化现在滚动条所在高度为0
    height = 0
    # 当前窗口总高度
    new_height = driver.execute_script(js)
    while height < new_height:
        # 将滚动条调整至页面底部
        for i in range(height, new_height, 100):
            driver.execute_script('window.scrollTo(0, {})'.format(i))
            time.sleep(0.5)
        height = new_height
        time.sleep(2)
        new_height = driver.execute_script(js)
    return driver


def acc_cookie(driver: WebDriver):
    try:
        # 底部弹窗出现是否接受cookie
        cookie = driver.find_element(By.XPATH, value='//button[@id="onetrust-accept-btn-handler"]')
        if cookie:
            cookie.send_keys(Keys.ENTER)
    except Exception as e:
        pass
    return driver


def get_all_document(driver: WebDriver):
    driver = scroll_(acc_cookie(driver))
    # 开始解析数据
    documents = driver.find_elements(By.XPATH, value='//app-summary-title/h3/a')
    urls = []
    for document in documents:
        url = document.get_attribute("href")
        urls.append(url)
    return urls, driver


def get_all_urls(driver: WebDriver, key_ward):
    # 获取所有url
    driver = search(driver, key_ward)
    all_paper_url = []
    count = 0
    try:
        while True:
            urls, driver = get_all_document(driver)
            all_paper_url.extend(urls)
            next_page = driver.find_element(By.XPATH, value='//button[@data-ta="next-page-button"][1]')
            next_page.send_keys(Keys.ENTER)
            count += 1
            if count >= 1:
                break
    except Exception as e:
        print('异常 or 查询结束')
    return list(set(all_paper_url))


def get_author_info_by_url(driver: WebDriver, url):
    # 获取作者信息
    while True:
        try:
            driver.get(url)
            break
        except Exception as e:
            print(f'请求异常，休息1min重试: {url}')
            time.sleep(60)
    time.sleep(2)
    current_url = driver.current_url
    address_list = ''
    title = ''
    author = ''
    email = ''
    try:
        title = driver.find_elements(By.XPATH, value='//h2[@id="FullRTa-fullRecordtitle-0"]')[0].text
        authors = driver.find_elements(By.XPATH, value='//span[starts-with(@id, "author-")]//span[@lang="en"]')
        authors = [author_en.text for author_en in authors]
        author = ','.join(authors)
        address_list = driver.find_elements(By.XPATH, value='//a[starts-with(@id, "address")]/span[2]')
        address_list = [address_en.text for address_en in address_list]
        email = driver.find_elements(By.XPATH, value='//a[@cdxanalyticscategory="wos-author-email-addresses"]')[0].text
    except Exception as e:
        print(f'current_url: {current_url} 缺失部分信息')
    print(f'title: {title}  authors: {author}  url: {current_url}  email: {email}')
    return [title, address_list, author, email, current_url]


def get_current_time():
    utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)
    SHA_TZ = timezone(
        timedelta(hours=8),
        name='Asia/Shanghai',
    )
    return utc_now.astimezone(SHA_TZ)


def catch_by_key_word(driver: WebDriver, key_word: str = 'Network security'):
    # 获取所有url
    urls = get_all_urls(driver, key_word)
    save_info = []
    # 可讲收集到的url直接读取出来
    # content = open('./url.txt').read().replace("'", '"')
    # urls = json.loads(content)
    # 抓取author info
    print(f'urls -> {urls}')
    print('==' * 20)
    for url in urls:
        save_info.append(get_author_info_by_url(driver, url))
        time.sleep(2)
    print('==' * 20)
    print(f'save_info -> {save_info}')
    print('==' * 20)
    list_2_excel(save_info, file_name=key_word)


def list_2_excel(data: list, title: list = None, file_name: str = 'test'):
    title = ['标题', '地址', '作者', '邮箱', '原链接'] if not title else title
    save_info = pd.DataFrame(columns=title, data=data)
    save_info.to_excel('./' + file_name + '.xlsx', encoding='utf-8')


def run():
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
    })
    driver.get('https://www.baidu.com/')
    for name, value in cookies.items():
        driver.add_cookie({'name': name, 'value': value})
    start_page = 'https://www.webofscience.com/wos/alldb/basic-search'
    driver.get(start_page)
    acc_cookie(driver)
    key_word = 'Endogenous security'
    catch_by_key_word(driver, key_word)
    driver.close()


if __name__ == '__main__':
    run()
    # save_info = [['Lightweight Group Secret Key Generation Leveraging Non-Reconciled Received Signal Strength in Mobile Wireless Networks', ['Southeast Univ, Sch Informat Sci & Engn, Nanjing, Jiangsu, Peoples R China'], 'Li, GY,Hu, LJ,Hu, AQ,IEEE', 'https://www.webofscience.com/wos/alldb/full-record/WOS:000484917800223'], ['Analysis and presentation of MPEG-compressed TV news feeds', [], 'Falkemeier, G.,Kao, O.', 'https://www.webofscience.com/wos/alldb/full-record/INSPEC:6296922']]
    # list_2_excel(save_info)
