# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 21:15:54 2020

@author: notbo
"""

'''此模塊為 電子辭典中服務端的類,
可以藉由 流程控制 main 還呼叫此模塊類的方法達到功能的呼叫使用
(已達到低耦合,高內聚)'''

# 導入模塊
from socket import *
import os
import sys
import time


# 導入 pymysql 是將登入和註冊的訊息新增到資料庫中
from pymysql import *






# 1.創建一個類來進行與客戶端進行數據的交換
class Dict_server():
    # 將main中父進程創建子進程的所有變數傳參到 此類中,再將參數做初始化結構
    def __init__(self,connfd,db):
        self.connfd = connfd
        self.db = db
    
    #1.建立一個函數和客戶端溝通進行數據交換的動作(接收客戶端執行的選項)
    def do_child(self):
        #while 循環接收客戶端請求
        while True:
            data = self.connfd.recv(1024).decode()
            print(self.connfd.getpeername(),':',data) #打印客戶端請求內容, getpeername()<<<打印哪一個客戶端法來的請求
            
            # 加入 not data 客戶端可能 ctrl + c 退出,導致data為空
            if not data or data[0] == 'E':
                print('客戶端',self.connfd.getpeername(),'退出服務器!')
                #子進程退出,也要將連接給關閉才不會報錯
                self.connfd.close()
                #系統也要關閉
                sys.exit(0)
                
            #客戶端發起註冊請求 'R'
            elif data[0] == 'R':
                self.do_register(data) #調用類的註冊函數
            #客戶端發起登入請球 'L'
            elif data[0] == 'L':
                self.do_login(data)
            
            #客戶端登入成功,輸入二級介面查詢單詞操作 'Q'
            elif data[0] == 'Q':
                self.do_query(data)
            
            #客戶端登入成功,輸入二級介面查詢歷史紀錄操作 'H'
            elif data[0] == 'H':
                self.do_hist(data)
                
    #2.客戶端登入函數
    def do_login(self,data):
        print('登入信息確認中!')
        l = data.split(' ') #做空格切割 name,passwd
        name = l[1]
        passwd = l[2]
                
        #建立游標對象
        cursor = self.db.cursor()
        
        #判斷用戶使否存在建立及密碼是否存在sql查詢語法
        sql = 'select * from user where name = %s and passwd = %s'
        
        #利用try 捕捉查詢錯誤
        try:
            cursor.execute(sql,[name,passwd])
            msg1 = cursor.fetchone()
        except Exception as e:
            print('Error for ',e)
            self.db.rollback()
            cursor.close()
        
        if msg1 == None:
            self.connfd.send(b'NOT EXISTS')
        else:
            self.connfd.send(b'OK')
            print('%s登入成功' % name)
            return
        
    #3.客戶端註冊
    def do_register(self,data):
        print('註冊操作')
        l = data.split(' ')#做空格切割 name,passwd
        name = l[1]
        passwd = l[2]
        
        #建立游標對象
        cursor = self.db.cursor()
        
        #判斷用戶是否存在建立sql語法查詢
        sql = 'select * from user where name = %s'
        
        #利用try捕桌查詢資料庫的錯誤
        try:
            cursor.execute(sql,name)
            r = cursor.fetchone() #因為用戶姓名不重複,所以只需要查詢一條紀錄即可
        except Exception as e:
            print('Error for:',e)
            self.db.rollback()
            cursor.close()
            
        #如果用戶存在則 r 不為 None,如果不存在返回值
        if r != None:
            self.connfd.send(b'EXISTS')
            print('用戶',self.connfd.getpeername(),'註冊名稱已存在!')
            return
        else:
            # 將資料寫入的my sql語法
            sql = 'insert into user(name,passwd) values(%s,%s)'            
            #利用 try 捕捉新增錯誤
            try:
                cursor.execute(sql,[name,passwd])
                self.db.commit()
                #若新增成功則傳送訊息給 客戶端
                self.connfd.send(b'OK')
                
            except Exception as e:
                self.db.rollback()
                self.connfd.send(b'FaLL')
                cursor.close()
            else:
                print('用戶',self.connfd.getpeername(),'註冊成功 !')
            #新增完成後必須斷開數據庫連接游標
            cursor.close()

        

    #4.客戶端查詞
    def do_query(self,data):
        print('單詞查詢操作')
        data1 = data.split(' ') 
        name = data1[1]
        words = data1[2].lower()
        
        
        #方法1.利用sql查詢方式
        #建立游標對象
        cursor = self.db.cursor()
        
        #利用try捕捉錯誤
        try:
            print('查詢的單詞為%s' % words)
            #此sql查詢單字單詞解釋
            sql = 'select * from words where word = %s'
            #執行sql查詢
            cursor.execute(sql,words)
            
            # 獲取查詢sql1結果
            r = cursor.fetchone()
            #此sql2 新增 insert into 歷史紀錄 name、time、word
            sql1 = 'insert into hist(name,word,time) values(%s,%s,%s)'
            cursor.execute(sql1,[name,words,time.ctime()])
            self.db.commit()

            #將查詢的資料返回給客戶端
            if r != None:
                self.connfd.send(b'OK')
                time.sleep(0.1) #防止傳回的訊息沾黏
                data1 = r[2] #傳回的是一個元組,有三個欄位(id:,words:,interpret),切片r[2]
                self.connfd.send(data1.encode())
            else:
                self.connfd.send(b'Fall')
                return
        except Exception as e:
            self.db.rollback()
            #關閉游標對象
            cursor.close()
            print('Error for',e)
        cursor.close()
            
            
        
        #方法2 直接利用文本查詢,新增紀錄和方法1相同
        # try:
        #     f = open(DICT_TEXT)
        # except:
        #     self.connfd.send(b'Fall')
        #     f.close()
        #     return
        
        # #利用循環提取首單詞
        # while True:
        #     for line in f:
        #         #獲取美行首單詞
        #         tmp = line.split(' ')[0]
        #         if tmp > words: #如果tmp 大於 word 就不必要再查詢單詞因為查詢不到,單詞的字數是由小到大
        #             self.connfd.send(b'fall')
        #             f.close()
        #             return
        #         elif tmp == words:#這時候表示查詢到了
        #             self.connfd.send(b'OK')
        #             time.sleep(0.1)
        #             self.connfd.send(line.encode())
        #             f.close()
        #             return
        #     self.connfd.send(b'fall')
        #     f.close()
            
        
    #5.客戶端查歷史紀錄       
    def do_hist(self,data):
        print('歷史操作')
        data1 = data.split(' ')
        name = data1[1]
        
        #建立游標對象
        cursor = self.db.cursor()
        
        #建立sql查詢語法
        sql = 'select * from hist where name = %s'
        try:
            cursor.execute(sql,name)
            
            #獲取查詢資料
            r = cursor.fetchall()
            
            #如果沒有歷史紀錄,傳回 客戶端b'fall'
            if not r:
                self.connfd.send(b'fall')
                return
            else:
                self.connfd.send(b'OK')
                time.sleep(0.1)#防止沾包
                
            for i in r:
                # i遍歷的會是元組(id:,name:,word:,time:)
                msg = '%s %s %s' % (i[1],i[2],i[3]) #切片訊息為 i[1],i[2],i[3] 
                print(msg)
                self.connfd.send(msg.encode())
                time.sleep(0.2)
            time.sleep(0.2)
            self.connfd.send(b'##')
                    
                

        except Exception as e:
            self.db.rollback()
            print('Error for',e)
        
        #關閉游標對象
        cursor.close()