# -*-coding:utf-8-*-


from selenium import webdriver
import selenium
import json
import time
from selenium.webdriver.chrome.service import Service
import os

#
# driver = webdriver.Firefox()
# driver.get("https://twitter.com/login")
# time.sleep(60)
# cookies = driver.get_cookies()
# with open("qrsncookies.txt", "w") as fp:
#     json.dump(cookies, fp)
# # https://twitter.com/login

# option = webdriver.FirefoxOptions()
# option.add_argument("headless")
# option.add_argument('--no-sandbox')
# driver = webdriver.Firefox(firefox_options=option)
# driver.get("https://twitter.com/login")
# with open("qrsncookies.txt", "r") as fp:
#     cookies = json.load(fp)
#     for cookie in cookies:
#         driver.add_cookie(cookie)
#
# driver.get("https://twitter.com")
# print driver.title

def read_cookies():



    # c_service = Service('E:\work\\twbot\chromedriver.exe')
    c_service = Service('/opt/google/chrome/chromedriver')
    c_service.command_line_args()
    c_service.start()

    #chrome
    option = webdriver.ChromeOptions()
    # option.set_headless()
    option.add_argument("--headless")
    option.add_argument("--no-sandbox")
    driver = webdriver.Chrome(chrome_options=option)
    # driver = webdriver.Chrome()

    #firefox
    # option = webdriver.FirefoxOptions()
    # # option.add_argument("headless")
    # # option.add_argument('--no-sandbox')
    # option.set_headless()
    # driver = webdriver.Firefox(firefox_options=option)

    driver.get("https://mobile.twitter.com")
    with open("qrsncookies.txt", "r") as fp:
        cookies = json.load(fp)
        for cookie in cookies:
	    if 'expiry' in cookie:
                del cookie['expiry']
            driver.add_cookie(cookie)

    driver.get("https://mobile.twitter.com/home")
    print driver.title
    time.sleep(20)
    return driver, c_service


def publishing(list):
    driver, c_service = read_cookies()
    # time.sleep(10)
    # print(list)
    # driver.find_element_by_xpath('//*[@id="global-new-tweet-button"]').click()
    driver.find_element_by_xpath('/html/body/div/div/div/div[2]/header/div/div/div/div/div[3]/a').click()
    print("click tw")
    time.sleep(10)
    driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[1]/div[2]/div/div/div/div[2]/div[2]/div/div[3]/div/div/div/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div[2]/div').send_keys(list[0])
    print("send text")
    time.sleep(10)
    lenth = len(list)
    for lis in list[1:lenth]:
        lis = lis.strip()
        if lis is None:
            break

        # driver.find_element_by_xpath(
        #     '//*[@id="Tweetstorm-tweet-box-0"]/div[2]/div[2]/div[1]/span[1]/div/div/label/input').send_keys(
        #     "/home/centos/shell/tianxiubot/" + lis)
        driver.find_element_by_xpath(
            '/html/body/div/div/div/div[1]/div[2]/div/div/div/div[2]/div[2]/div/div[3]/div/div/div/div[1]/div/div/div/div/div[2]/div[2]/div/div/div[1]/input').send_keys(
            "/home/centos/shell/tianxiubot/" + lis)
        # print("click publish")
	# /home/centos/shell/tianxiubot/
        # E:\work\\twbot\\tianxiubot\\
        # print(lis)
        time.sleep(1)

    time.sleep(1)
    # driver.find_element_by_xpath('//*[@id="Tweetstorm-tweet-box-0"]/div[2]/div[2]/div[2]/span/button[2]').click()
    driver.find_element_by_xpath('/html/body/div/div/div/div[1]/div[2]/div/div/div/div[2]/div[2]/div/div[3]/div/div/div/div[1]/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[4]').click()
    print("click publish")
    time.sleep(30)
    driver.quit()
    c_service.stop()
    os.system('bash killchrome.sh')

def publish(list):
    try:
        publishing(list)
    except Exception as e:
        os.system('bash killchrome.sh')
        print("publishing error")
	print(e)

# time.sleep(3)

#
# driver = read_cookies()
# # time.sleep(5)
# driver.find_element_by_xpath('//*[@id="tweet-box-home-timeline"]').click()
# time.sleep(5)
# driver.find_element_by_xpath('//*[@id="tweet-box-home-timeline"]').send_keys("hello luxun")
# time.sleep(10)
# driver.find_element_by_xpath(
#     '//*[@id="timeline"]/div[2]/div/form/div[3]/div[1]/span[1]/div/div/label/input').send_keys(
#     "D:\work\weiboimg\\4281283040890712.png")
#
# time.sleep(1)
# driver.find_element_by_xpath('//*[@id="timeline"]/div[2]/div/form/div[3]/div[2]/button/span[1]').click()


