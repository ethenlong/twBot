# -*-coding:utf-8-*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import requests
import time
import re
# from PIL import Image, ImageFont, ImageDraw
import math
from urllib import urlretrieve
import webbrowser
# import csv
# from loginTwitter import Fetcher
import tianxiudriver
import selenium
from PIL import Image
headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Referer': 'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=https%3A%2F%2Fm.weibo.cn%2F'
                   '&sudaref=passport.weibo.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
}


cookie = {
        'M_WEIBOCN_PARAMS': 'luicode%3D10000011%26lfid%3D231093_-_selffollowed%26fid%3D1005056593871464%26uicode%3D10000011',
        'SUB': '_2A252yUwiDeRhGedG41YT9ynNyTmIHXVSMlRqrDV6PUJbkdAKLXT7kW1NURfos6Cj6kwM23lrbOd_ta8Y6bcqRicZ',
        'SCF': 'AntktLVOfUR7wa8PPndqRbAR3xuXzQ7gvHA4jFJuvsMyuVpQtCqxT3BjFtxZ9GRt3P47Nk5RnGeltZoRrsZBB1A.',
        '_T_WM': '9be7e40600d31988d24c0c64bc241c4e',
        'SSOLoginState': '1540177010',
        'WEIBOCN_FROM': '1110003030',
        'SUHB': '0auRL17fAvRRhZ',
        'MLOGIN': '1',
}

def cutPic(path, fileNmae):
    fn = fileNmae.split('.')
    baseName = fn[0]
    # ext = fn[1]
    img = Image.open(path+"/"+fileNmae)
    w, h = img.size
    rate = h/w
    #print rate
    count = h/4
    #print count
    if rate >= 4:
        for i in range(4):
            box = (0, i * count, w, (i + 1) * count + 10)
            img.crop(box).save(path + "/" + baseName + str(i) + ".jpg")
            print(path + "/" + baseName + str(i) + ".jpg")
        return True, baseName
    else:
        return False, baseName

def get_time():
    localtime = time.asctime(time.localtime(time.time()))
    return localtime

def login():

    url = 'https://passport.weibo.cn/sso/login'
    param = {
        'username': 'ethenlong@163.com',
        'password': 'gjhlh1111',
        'savestate': 1,
        'r': 'http://m.weibo.cn/'
    }
    s = requests.Session()
    s.post(url, param, headers)

def img_download(path,img_url):
    # http://wx1.sinaimg.cn/large/007f122Jly1fw5iq926cgj30xg07i3zz.jpg
    img_name = re.findall(r'large/(.+)', img_url)[0]
    # print(img_name)
    try:
        urlretrieve(img_url, path+img_name)
    except IOError as e:
        print("time out error")
    return img_name

def write_csv(filename, text):
    with open(filename,'a+') as f:
        f.write(text.encode('utf-8')+'\n')
        f.close()


def download_video(path, url):
    from urllib2 import urlopen
    import subprocess
    f = urlopen(url)
    data = f.read()
    tmpdate = "tem.mp4"
    with open(tmpdate, 'wb') as vdo:
        vdo.write(data)
    subprocess.call(['ffmpeg', '-i', tmpdate, path])
    print("video download done")


def get_first_page():
    url = 'https://m.weibo.cn/api/container/getIndex?'
    parma1 = {
        'containerid': '102803_ctg1_4388_-_ctg1_4388',
        'openApp': '0'
        # 搞笑 containerid: 102803_ctg1_4388_-_ctg1_4388
        # 热门 containerid: 102803
        # 汽车 containerid: 102803_ctg1_5188_-_ctg1_5188
    }
    res = requests.get(url=url, params=parma1, cookies=cookie, headers=headers)
    blgs = res.json().get('data').get('cards')
    for item in blgs:
        if item.get('card_type') != 9:
            blgs.remove(item)
    # print(res.json())
    since_id = res.json().get('data').get('cardlistInfo').get('since_id')
    # print(blgs)
    for blg in blgs:
        # print(blg)
        create_tm = blg.get('mblog').get('created_at')
        text = blg.get('mblog').get('text')
        blg_id = blg.get('mblog').get('id')
        a_elements = re.findall(r'<a(.*?)/a>', text)
        for elem in a_elements:
            text = text.replace('<a' + elem + '/a>', '')


        rule = re.compile(r'<(.*?)>', re.S)
        del_str = re.findall(rule, text)
        for del_s in del_str:
            text = text.replace('<'+del_s+'>', '')

        print(text)

        # print(create_tm + " , " + text + '\n')
        pic_list = []
        pics = []
        # video = ''
        try:
            pics = blg.get('mblog').get('pics')
            # print(pics)
            # video = blg.get('mblog').get('page_info').get('media_info').get('stream_url')
            # if video != '':
            #     from urllib2 import urlopen
            #     print(video)
            #     download_video("tianxiubot/"+blg_id+".mp4", video)
        except AttributeError as e:
            print(e)
        if pics is None:
            print("pics is none")
        else:
            for pic in pics:
                print(pic.get('large').get('url'))
                try:
                    img = img_download("tianxiubot/", pic.get('large').get('url'))
                    pic_list.append(img)
                except AttributeError as e:
                    print(e)
        print('end')
        if pic_list != []:
            pic_all = ''
            for pic in pic_list:
                check, basename = cutPic("tianxiubot", pic)
                if check:
                    for i in range(4):
                        pic_all = pic_all + ',' + basename + str(i) + ".jpg"
                else:
                    pic_all = pic_all + ',' + pic
            write_csv("tianxiubot/bot.txt", text + pic_all)
        # elif video != '':
        #     write_csv("tianxiubot/bot.txt", text + ","+blg_id+".mp4")
    return since_id

def cleanFile(filename):
    with open(filename, 'w') as f:
        f.write('')
        f.close()

def tweet():
    import codecs
    with codecs.open("tianxiubot/bot.txt", 'r', encoding='utf-8') as weibo:
        lines = weibo.readlines()
        for line in lines:
            line = line.replace('\n', '')
            lis = line.split(',')
            # print(lis)
            # tianxiudriver.publish(lis)

            tianxiudriver.publish(lis)

            weibo.close()
            print("publish down " + get_time())

            time.sleep(420)


        # for line in weibo.readlines():
        #     line = line.replace('\n', '')
        #     lis = line.split(',')
        #     print(lis)
        #     webdriver.publish(lis)
        #     time.sleep(3600)


if __name__=='__main__':
    print(get_time())
    cleanFile("tianxiubot/bot.txt")
    get_first_page()
    tweet()


    # login()
    # get_first_page()
