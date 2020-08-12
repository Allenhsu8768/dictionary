# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 21:30:11 2020

@author: notbo
"""

'''此模塊為 電子辭典中客戶端的類,
可以藉由 流程控制 main 還呼叫此模塊類的方法達到功能的呼叫使用
(已達到低耦合,高內聚)'''


#導入模塊
from socket import *
import sys
import time


#導入模塊可以將密碼加密
import getpass






#寫一個類封裝函數
class Dict_client():
    def __init__(self,sockfd):
        self.sockfd = sockfd
    
    #新增 do_register 客戶端註冊函數
    def do_register(self):
        #寫一個while 循環可以判斷當確認密碼輸入不符時,必須重新再輸入一次
        while True: 
            name = input('請輸入註冊英文姓名:')
            #*cookie 將密碼做加密輸入 import getpass (相當於linux 的隱形輸入)
            passwd = getpass.getpass()
            passwd1 = getpass.getpass('Again:') #加入參數'Again:'可以確認密碼比對第一次密碼是否相符,若不相符則重新輸入
            
            #不予許輸入的字元有空格,若有空格則返回重新輸入
            if (' ' in name) or (' ' in passwd):
                print('用戶名或密碼不許有空格')
                continue
            #若密碼不符,則返回重新輸入
            if passwd != passwd1:
                print('兩次密碼不一致')
                continue
            
            #發送請求(將註冊訊息發送)
            # msg 前的 R表示 為註冊 是向服務端發起註冊的請求,讓服務端可辨識請求
            msg = 'R {} {}'.format(name,passwd) #將訊息發送請求給服務端
            self.sockfd.send(msg.encode())
            
            #等待回復
            data = self.sockfd.recv(1024).decode()
            
            # 利用返回值來打印不同情況返回給使用此類方法的函數
            if data == 'OK':
                return name
            #用戶不可重複,表示重名,要回重新輸入註冊姓名
            elif data == 'EXISTS':
                return 
            
    #新增一個登入函數
    def do_login(self):
        #利用while 循環來確認登入用戶是否存在,若輸入姓名或密碼錯誤則重新輸入,直到成功
        while True:
            name = input('請輸入使用者名稱:')
            #一樣使用 模塊 getpass 讓輸入的密碼可以進行保護
            passwd = getpass.getpass()
            passwd1 = getpass.getpass('Again') #第二次輸入密碼與第一次的密碼進行確認
            
            #傳送請求訊息給服務端
            msg = 'L {} {}'.format(name,passwd)
            self.sockfd.send(msg.encode())
            
            #等待服務端回復
            data = self.sockfd.recv(1024).decode()
            
            if data == 'OK':
                return name
            elif data == 'NOT EXISTS':
                return 
            
    #新增 do_query() 一個查單詞函數
    def do_query(self,name):
        #寫while True 循環查單詞
        while True:
            words = input('輸入要查詢的單詞(輸入空白則退出):')
            if not words:
                break
            msg = 'Q {} {}'.format(name,words)
            self.sockfd.send(msg.encode())
            
            #等待服務端訊息
            data = self.sockfd.recv(1024).decode()
            if data == 'OK':
                data = self.sockfd.recv(2048).decode()
                print('輸入的單詞為 %s,查詢解釋單詞結果為: %s' % (words,data))
            else:
                print('沒有查到此單詞解釋')
                
    
    #新增一個 do_hist() 查歷史紀錄函數
    def do_hist(self,name):
        msg = 'H {}'.format(name)
        self.sockfd.send(msg.encode())
            
        #等待服務端訊息
        data = self.sockfd.recv(128).decode()
        if data == 'OK':
            #循環接受服務端傳來的訊息(查詢結果訊息)
            while True:
                data = self.sockfd.recv(1024).decode()
                if data == '##':
                    break
                print(data)
        else:
            print('查詢不到該用戶歷史紀錄')
        
    
    
    #新增一個 login() 登入成功時,進入二級介面畫面
    def login(self,name):
        #利用while True 讓客戶端進入二級介面
        while True:
            print('''
                  =========查詢界面=========
                   1.查詞  2.歷史紀錄 3.退出
                  ==========================
                ''')
            
            try:
                cmd = input('請輸入要執行選項命令:')
            except Exception as e:
                print('命令錯誤:',e)
                continue
            
            if cmd not in ['1','2','3']:
                print('請輸入正確選項')
                sys.stdin.flush() #清除標準輸入
                continue
            elif cmd == '1':
                self.do_query(name)
            elif cmd == '2':
                self.do_hist(name)
            elif cmd == '3':
                print('跳回一級介面!')
                return