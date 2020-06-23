# -*-coding:utf-8-*-
import re

text = '''哈哈哈哈哈哈哈哈我的老父亲太有意思了<span class="url-icon"><img alt=[笑cry] src="https://h5.sinaimg.cn/m/emoticon/icon/default/d_xiaoku-d320324f00.png" 
                style="width:1em; height:1em;" /></span> '''

print(text)
rule1 = re.compile(r'<(.*?)>', re.S)
elems = re.findall(rule1, text)
for ele in elems:
    text = text.replace('<'+ele+'>', '')
print(text)
rule = re.compile(r'<img(.*?)/>', re.S)
elems2 = re.findall(rule, text)
for ele in elems2:
    text = text.replace('<img' + ele + '/>', '')
