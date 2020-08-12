# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 23:58:54 2020

@author: notbo
"""

'''此模塊是 電子辭典 服務端 (建立通訊框架進行數據交換)
利用 sys.fork() 多進程的 (Tcp套接字)流式套接式 方式來進行多人連接數據交換

* 此模塊檔案必須在linux(ubuntu )環境下執行

name: Allen
date:2020-08-12
email:notbook7787@gmail.com
modules:
this is a dict project 
'''


# 導入模塊
from socket import *
import os
import sys
import time
import signal

# 導入 pymysql 是將登入和註冊的訊息新增到資料庫中
from pymysql import *

# 導入dict_sever_class模塊
from dict_server_class import *

#導入 Dict_server類的方法


# 定義需要的全局變量

# 資料中以有模塊檔案 insert__word.py 可以將單詞dict.txt的資料新增
# 也可以利用 mysql 查詢語法對單詞解釋進行查詢


# 透過文本的操作查詢單詞解釋
DICT_TEXT = './dict.txt'



#定義地址
HOST = '0.0.0.0'
PORT = 8000
ADDR = (HOST,PORT)






            
    
        

# 流程控制
# 2.寫一個函數來執行服務端開啟
def main():
    #創建數據庫連接新增客戶端登入、註冊、歷史訊息資料
    db = connect(host='localhost',user='root',
                 passwd='a123456',database='dict',
                 port=3306,charset='utf8')
    
    #建立游標對象
    cur = db.cursor()
    
    
    #創建套接字
    sockfd = socket(AF_INET,SOCK_STREAM) #流式套接字 tcp : SOCK_STREAM
    sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    sockfd.bind(ADDR)
    sockfd.listen(5)
    
    #處理子進程退出(避免殭屍進程)
    # cookie:
    #導入信號模塊signal 使用方法
    #在進程當中忽略子進程狀態改變,子進程退出自動由操作系統處理
    #SIGCHLD信號,是當子進程狀態改變他會發送給父進程通知子進程狀態改變的信號
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)
    print('---------listen the port 8000---------')
    
    
    #建立while 循環,連接
    while True:
        # 利用try、except捕捉錯誤
        try:
            #等待客戶端連接
            connfd,addr = sockfd.accept()
            print('Connect from',addr)
        except KeyboardInterrupt: # Ctrl + c 退出
            sockfd.close()
            sys.exit('服務器退出')
        except Exception as e:  # 其他異常情形
            print('其他異常',e)
            continue  #返回,繼續等待客戶端連接
        
        #如果沒有發生異常,為其他客戶端連接時創進新的進程,處理請求
        #創建子進程,處理客戶端的請求
        pid = os.fork()
        
        #如果 pid == 0  #子進程處理具體請求,以下方式可以知道客戶端可以長期占有服務器,為每一個客戶端創建單獨的進程
        if pid == 0:
            #可以將複製父進程的s給關閉,因為新的客戶端連接是父進程處理的事件(父子進程兩者運行獨立互不影響)
            sockfd.close()
            
            #可以子進程中寫一個函數來處理客戶端信息
            print('執行客戶端請求')
            
        #利用類方法必須在創建在while循環前,在創建子進程中
            ## 建立dict_select 對象,導入 Dict_server類的方法使用
            dict_select = Dict_server(connfd,db)
            while True:
                # 1.接收各個客戶端請求訊息(接收客戶端傳送的選項)
                dict_select.do_child()
                
        
        
        #不加入 判斷 pid <0,
        #創建進程失敗也必須回到前面繼續等待其他客戶端連接和父進程相同
        #父進程或者創建失敗都繼續等待下個客戶端連接
        else:
            #可以將父進程的c關閉,因為客戶端接收信息改由子進程進行數據交互(父子進程兩者運行獨立互不影響)
            #而且當進程創建失敗的時候也必須要關閉客戶端連接
            connfd.close()
            continue

        
            


# 執行程式
if __name__ == '__main__':
    main()