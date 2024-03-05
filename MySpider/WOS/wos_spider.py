#  This software shall not be used for commercial purposes, only for learning communication
#  Copyright (c) 2022-2023. All rights reserved.

import datetime
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
    "bm_mi": "BBCC4A791D5BE284A37B35F99CEDDFD0~YAAQD2YzuFgIQ0SGAQAAbHchkRIAitV/4ov98WWCnco9cYJjiUXfv8q9fL4/zq+Y7+O9qep+XCjzgqRS9qnDbJplHoqJ8neXcCx/nusXaeFLGFKeNIlmJtsDnNOIQuwLl2+ylOQwJ7YIRDt6aAJEgXhWk06FI2I3HYYk67UyHAUpfxhTVf5lRaEJVzkbg1h7x9RYWPvEZ+U/OEGNM8STb/VMNlNfTQMQe5r9Z9wc8oPCjcczK7oVElZKYQTgDeLmXcfjDkWZ0iIciVLAG49ACEiYyvgDFD84++LVIZX0y/Qc7gw6HLAds1owNGzDOGzo8CXbR5uHrRdXa1Ccd7ODNOonhhgderreWlUuAyQklEk8YR9ZEQ==~1",
    "ak_bmsc": "14432C631D8144B2A4ACAE470DE92548~000000000000000000000000000000~YAAQD2YzuL8KQ0SGAQAA8o8hkRLMA9vEu9MVGP/2lm53EJ1ezNmHCh+r+0RkUjrI1Pw3l9bRtTDTg0ZHcpDXlyq6o1c0mmW3qbb1ikuk+mQqHgn1Z5cq+THhhcKlD5GFZjKx13+mk/+Bgo9hPnWW0OCTuuzZ2t601NiSkNFa7Q1I701LeqlEi97ynNxkZyiDdXRYZvBMlUkjeutVrTdcK4DvYo9LwNOLBFT3+Unzy/s4RC7MsEGBQVcwnSgE45RKdUTyUJ3W7OuLxcn6nMyYjdRplv05OahzY35n7kTt9Nn+dV6X52uPEp+iRu2SCCmGpWhMCjlHz901uTeblq8/h6Cm3GwpsfubnIAw5gof6nVfAPnmoZE0WaAPJosARxYlpqleRYiwfelpT2KZ97doeIlwPt2U8F8uMVRbMvJgVn8e2icpKNHJZyvutIUvu9gP0x5SuXySX7ZpDVmeaV7RotQg",
    "_sp_id.840c": "3a1b4863-80e8-4ecb-9cdf-5c8c7635556c.1676885746.9.1677472467.1677465237.11a2f10c-af67-4426-925c-9c4fcdff3c1f.34341fa4-6920-4f68-b4e5-95fd20bdd7a9.7198a8c3-ef3a-462c-8908-ca14bafc3783.1677467769221.30",
    "OptanonConsent": "isGpcEnabled=0&datestamp=Mon+Feb+27+2023+12%3A34%3A27+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=6.39.0&isIABGlobal=false&hosts=&consentId=d0fd0e36-638d-4725-a549-eb1e4db32cee&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0004%3A1%2CC0005%3A1%2CC0002%3A1&geolocation=HK%3BHWC&AwaitingReconsent=false",
    "bm_sv": "AE12EC7C1A68E3103A5AA7F0B08DDF84~YAAQl2YzuOmvfIaGAQAA4pgmkRKzOx+Lkq+uiRqfMnBDoeQsHRP1ixgpfVZdIrpdnsK5l60P52VieP5Sk4GKhee+/xBTZaq1w141N2fLWc+aAmWMNj+f+4jKvK/ZosDK8FvLxCey73dipjoSo7ZcC8tHFs60/NmoQN2cPjr5NT/dUuP8AW7jThirmeusp5rfA6J/1PfTDkH7mmhlOMexRHZE/v7zP+xRAAsWLI2H5dtVcdbTEzB3/nRPHUeLWcL7gtmxVikV~1",
    "RT": "\"z=1&dm=www.webofscience.com&si=e16913bd-b694-4871-ac13-51e3b1f4e585&ss=lembslhs&sl=0&tt=0&bcn=%2F%2F684d0d4b.akstat.io%2F&ul=7xjl\""
}
chrome_options = Options()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')


def search(driver: WebDriver, key_ward):
    retrieval = driver.find_element(By.XPATH, value='//input[@name="search-main-box"]')
    retrieval.send_keys(key_ward)
    confirm = driver.find_element(By.XPATH, value='//button[@type="submit"]')
    confirm.send_keys(Keys.ENTER)
    time.sleep(5)
    return driver


def scroll_(driver: WebDriver):
    js = "return action=document.body.scrollHeight"
    height = 0
    new_height = driver.execute_script(js)
    while height < new_height:
        for i in range(height, new_height, 100):
            driver.execute_script('window.scrollTo(0, {})'.format(i))
            time.sleep(0.5)
        height = new_height
        time.sleep(2)
        new_height = driver.execute_script(js)
    return driver


def acc_cookie(driver: WebDriver):
    try:
        cookie = driver.find_element(By.XPATH, value='//button[@id="onetrust-accept-btn-handler"]')
        if cookie:
            cookie.send_keys(Keys.ENTER)
    except Exception as e:
        pass
    return driver


def get_all_document(driver: WebDriver):
    driver = scroll_(acc_cookie(driver))
    documents = driver.find_elements(By.XPATH, value='//app-summary-title/h3/a')
    urls = []
    for document in documents:
        url = document.get_attribute("href")
        urls.append(url)
    return urls, driver


def get_all_urls(driver: WebDriver, key_word, end_page: int = None):
    driver = search(driver, key_word)
    all_paper_url = []
    end_no = driver.find_elements(By.XPATH, value='//span[@class="end-page ng-star-inserted"]')[0].text
    count = 0
    end_page = end_page if end_page else int(end_no)
    try:
        while True:
            print(f'抓取关键词: {key_word}, 当前抓取第{count + 1}页，共{end_no}页')
            urls, driver = get_all_document(driver)
            print(f'抓取到论文地址: {urls}')
            print('===' * 40)
            all_paper_url.extend(urls)
            next_page = driver.find_element(By.XPATH, value='//button[@data-ta="next-page-button"][1]')
            next_page.send_keys(Keys.ENTER)
            count += 1
            if end_page and count >= end_page:
                break
    except Exception as e:
        print(e)
        print('异常 or 查询结束')
    return list(set(all_paper_url))


def get_author_info_by_url(driver: WebDriver, url):
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
        authors = [author.text for author in authors]
        author = ','.join(authors)
        address_list = driver.find_elements(By.XPATH, value='//a[starts-with(@id, "address")]/span[2]')
        address_list = [address_en.text for address_en in address_list]
        email = driver.find_elements(By.XPATH, value='//a[@cdxanalyticscategory="wos-author-email-addresses"]')[0].text
    except Exception as e:
        print(f'current_url: {current_url} 缺失部分信息')
    print(f'title: {title}  authors: {author}  url: {current_url}  email: {email}')
    return [title, address_list, author, email, current_url]


def catch_by_key_word(driver: WebDriver, key_word: str = 'Network security'):
    urls = get_all_urls(driver, key_word)
    save_info = []
    print(f'urls -> {urls}')
    print('===' * 40)
    for url in urls:
        save_info.append(get_author_info_by_url(driver, url))
        time.sleep(2)
    print('===' * 40)
    print(f'save_info -> {save_info}')
    print('===' * 40)
    list_2_excel(save_info, file_name=key_word)


def list_2_excel(data: list, title: list = None, file_name: str = 'test'):
    title = ['标题', '地址', '作者', '邮箱', '原链接'] if not title else title
    save_info = pd.DataFrame(columns=title, data=data)
    save_info.to_excel('./datasets/' + file_name + '.xlsx', encoding='utf-8')


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
    keywords = ['Key Information extract']
    for key_word in keywords:
        catch_by_key_word(driver, key_word)
    driver.close()


if __name__ == '__main__':
    run()
