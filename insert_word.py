# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 21:35:19 2020

@author: notbo
"""

'''此模塊檔案用來將dict.txt (單詞資料)
insert 到 mysql數據庫中'''


#導入模塊
from pymysql import *
import re

# 1.建立pymyql數據庫連接
db = connect(host='localhost',
             user='root',
             passwd='a123456',
             database='dict',
             port=3306,
             charset='utf8')


# 2.建立游標對象
cur = db.cursor()



# 3.關閉數據庫連接
def close1():
    cur.close()
    db.close()

# 查看文本內容為 
#a                indef art one
# abacus           n.frame with beads that slide along parallel rods, used for teaching numbers to children, and (in some countries) for counting
# abandon          v.  go away from (a person or thing or place) not intending to return; forsake; desert
# abandonment      n.  abandoning
# abase            v. ~ oneself/sb lower oneself/sb in dignity; degrade oneself/sb ;
# abash            to destroy the self-possession or self-confidence of:disconcert
# abashed          adj. ~ embarrassed; ashamed

#單詞和解釋之間有空格
#可以利用re 正則表達式 ,搜尋字串r'/s+',切割 re.split (r'/s+',目標字符串)

# 打開文本
f = open('dict.txt')
for line in f:
    l = re.split(r'\s+',line) # 將任意空字符串利用匹配的方式刪除,會返回 ['a','indef','art','one']
    word = l[0] # 'a' 索引split後的[0] 為文本中的單字
    interpret = ' '.join(l[1:]) # 再用索引[1:] 表示 ['indef','art','one'] 全都join到字串中
    # 再利用連接數據的的游標對象進行insert的動作
    sql = 'insert into words(word,interpret) values(%s,%s)'
    try:
        cur.execute(sql,[word,interpret])
        db.commit()
    except Exception as e:
        db.rollback()
        print('filed',e)
        close1()
        
f.close()
    








