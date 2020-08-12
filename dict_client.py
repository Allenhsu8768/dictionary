# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 12:34:42 2020

@author: notbo
"""

'''此模塊是 電子辭典 客戶端 (建立通訊框架進行數據交換)
利用 sys.fork() 多進程的 (Tcp套接字)流式套接式 方式來進行多人連接數據交換

* 此模塊檔案必須在linux(ubuntu )環境下執行

name: Allen
date:2020-08-12
email:notbook7787@gmail.com
modules:
this is a dict project 
'''


#導入模塊
from socket import *
import sys
import time


#導入模塊 dict_client_calss 模塊
from dict_client_class import *



            

#流程控制
#將客戶端創建網路連接
def main():
    # 利用 sys.argv的方式在客戶端連接時,輸入地址
    # 客戶端連接必須加入地址 addr
    if len(sys.argv) < 3:
        print('argv is error !')
        return
    
    #變數綁定客戶端輸入的地址
    HOST = sys.argv[1]
    PORT = int(sys.argv[2]) #sys.argv返回的是一個字串,必須轉型為int
    ADDR = (HOST,PORT)
    
    #創建套接字(客戶端)
    sockfd = socket(AF_INET,SOCK_STREAM)
    
    #捕獲異常
    try:
        sockfd.connect(ADDR)
    except Exception as e:
        print('連接服務端失敗 !','\n連接錯誤訊息:',e)
        return
    print('連接成功')    
    #調用類的方法必須在while 循環前建立對象
    #建立dict_select對象,且調用模塊dict_client_class 中的類方法(功能)
    dict_select = Dict_client(sockfd)
    
    #利用while循環傳送及接收服務端訊息
    while True:
        #連接成功進入到二級介面
        print('''
              ========Welcome==========
              -- 1.註冊 2.登入 3.退出--
              =========================
              ''')
              
        #加入try防止客戶端隨意地輸入其他字元,防止異常產生
        try:
            cmd = input('請輸入您要執行的選項:')
        except Exception as e:
            print('命令錯誤,異常輸入:',e)
            continue
        
        if cmd not in ['1','2','3']:
            print('請輸入正確選項')
            sys.stdin.flush() #清除標準輸入(防止快速輸入,會和上次輸入沾黏在一塊,確認每次輸入能夠被單獨識別)
        
        # 如果客戶端選擇 1.註冊
        elif cmd == '1':
            r = dict_select.do_register()
            if r:
                print('註冊成功!')
                #註冊成功,將回傳的r參數,傳入可以直接調用類裡面的二級介面
                dict_select.login(r)
            

            #如果註冊失敗,會回到一級介面重新做選擇
            else:
                print('註冊用戶已存在,請重新註冊確認姓名!')

                
        # 如果客戶端選擇 2.登入
        elif cmd == '2':
            l = dict_select.do_login()
            
            if l: #表示為真True,登入成功
                print('登入成功')
                #登入成功,將回傳的l參數傳入 調用類的 login()函數 進入二級介面
                dict_select.login(l)                    
            else:
                print('輸入的名稱密碼可能尚未註冊,或是輸入密碼有誤,請重新確認!')
        
        #如果客戶端選擇 3.退出
        elif cmd == '3':
            sockfd.send(b'E')
            sys.exit('bye,謝謝使用!')
                
    




#啟動函數
if __name__ == '__main__':
    main()
    