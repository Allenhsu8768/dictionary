# 1.電子辭典需求
	# 功能說明: 英英辭典(英文單詞用英文來解釋)
	#  1.用戶可以登入和註冊
	#     1.1 登入憑藉用戶名密碼即可
	#     1.2 註冊要求用戶必須填寫用戶名和密碼其他內容自訂
	#     1.3 用戶名要求不能夠重複

	#  2.用戶數據要求使用數據庫長期保存(可以選擇使用 mysql 和 mongodb 、範例是使用mysql)
	#     數據表自訂(要求能夠存儲中文)

	#  3.能夠滿足多個用戶同時登入操作需求
	#    必須選擇多進程、多線程併發(範例是利用多進程)

	#  4.功能分為客戶端和服務端,客戶端主要發起請求,服務端處理請求,
	#    用戶啟動客戶端進入一級介面(範例是使用簡單的print 打印介面)
	#     一級介面功能 1.登入、2.註冊、3.退出

	#  5.用戶登入後即進入二級介面
	#     二級介面功能 1.查單詞  2.查歷史紀錄 3.退出
	#             單詞本: 每行一個單詞
	#                     單詞和解釋之間一定有空格
	#                     後面的單詞一定比前面的大
	#                 2個方案選擇
	#                    1.直接進行文本操作直接把一行顯示出來
	#                    2.編寫程序將單詞存儲到數據庫中,通過數據庫查找

	#            二級功能解釋
	#                 1.查單詞:輸入單詞,顯示單詞意思,可以循環查詢
	#                         輸入'##'表示退出查詢
	#                 2.查看歷史紀錄: 查看當前用戶的歷史查詞紀錄(可以查看所有紀錄,也可以查看最近10條)
	#                         什麼人name  查什麼詞 word  在什麼時間 time
	#                 3.退出: 推出到一級介面,相當於註銷




#2. (電子辭典)項目架構流程如下:
# 1.確定技術點
	#   什麼併發(進程、線程併發)、什麼套接字(流式套接字)、
	# 什麼數據庫(mongodb、mysql都可以)、文件處理還是數據庫查詢? (範例:兩種方法都有表現)
	# 如果是數據庫查詢如何將單詞存入數據庫.


	# 2.建立數據表(所有的數據庫都必須建立在服務端)
	#   建立幾個表 每個表什麼字段(欄位),表關係
	#  建立一個庫 dict
	#      庫中需要建立3個表
	#          1.用戶信息: 
	#               功能:註冊、登入
	#               欄位: id 、name、passwd(密碼)

	#          2.歷史紀錄時間: 
	#               功能:查詢歷史紀錄(查單詞的時候插入紀錄)、查單詞
	#               欄位: id 、 name 、 word(單詞) 、time(時間)
	#          3.存單詞:
	#               功能:查單詞
	#               欄位:id 、word 、 interpret(解釋)
		  
	# 3.項目分析 仿照ftp 和聊天室 進行項目分析



	# 4.搭建通信框架



	# 5.分析有幾個功能如何封裝,每個功能具體實現什麼內容



#3.電子辭典 項目分析如下:

	# 1.服務器: 登入、 註冊 、查詢 、歷史紀錄

	# 2.客戶端:打印介面、發出請求、接收反饋、打印結果

	# 技術點: 1.併發(多進程併發、多線程併發:範例使用多進程sys.fork)
	#         2.套接字(tcp套接字:詞義的傳輸對準確性比較確實)
	#         3.數據庫 mysql
	#         4.查詞 ( 1.文本查詢)


	# 工作流程: 
	#        1.創建數據庫
	#        2.存儲數據(將文本單詞存到數據庫中)
	#        3.搭建通信框架 
	#        4.建立併發關係
	#        5.實現具體功能封裝


#4.通信框架流程圖如資料夾內檔案





