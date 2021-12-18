from os import listdir
import requests
from bs4 import BeautifulSoup

from Constants import FAIL


class ThirdPartyServerData:
    def __init__(self):
        return
    
    """Hàm lấy giá vàng"""
    def get_gold_list(date):
        all_golds = {}
        """Sử dụng thư viện requests để lấy html response"""
        #URL = "https://www.sjc.com.vn/xml/tygiavang.xml"
        URL = f"https://tygia.com/api.php?column=0&cols=1&title=1&chart=0&gold=1&rate=0&expand=2&nganhang=VIETCOM&ngay={date}"
        try:
            html_text = requests.get(URL)
        except requests.exceptions.ConnectionError:
            raise requests.exceptions.ConnectionError
        except requests.exceptions.Timeout:
            raise requests.exceptions.Timeout
        else:
            try:
                soup = BeautifulSoup(html_text,"lxml")
                """Lấy ngày đang tra cứu từ html"""
                present_day = soup.find("span",id = "datepk1")
                
                """Dựa vào class và id để tìm lấy dữ liệu từ html"""
                list_gold = soup.find_all("tr",class_ = "rmore rmore1")
                list_gold.append(soup.find("tr",id = "SJCH_Ch_Minh"))
                list_gold.append(soup.find("tr",id = "SJCH_N_i"))
                list_gold.append(soup.find("tr", id = "DOJIH_N_iAVPL"))
                list_gold.append(soup.find("tr", id = "DOJIH_Ch_MinhAVPL"))
                list_gold.extend(soup.find_all("tr",class_ = "rmore3"))
                list_gold.extend(soup.find_all("tr",class_ = "rmore4"))
                list_gold.extend(soup.find_all("tr",class_ = "rmore5"))
                """Danh sách trả về gồm loại vàng,giá mua,giá bán"""
                values = []
                for gold in list_gold:
                    if gold:
                        """Tìm đến thẻ chứa loại vàng"""
                        name = gold.find("td",class_ = "c1 text-left")
                        
                        """Tìm đến thẻ chứa giá mua"""
                        buy = name.find_next("td")
                        
                        """Nếu tồn tại thì trích xuất giá mua ra"""
                        if buy.find_all('div'):
                            buy_price = buy.div.div.span.text
                        else:
                            """Nếu không có thẻ mua thì cho nó bằng 0"""
                            buy_price = "0"
                        
                        """Tìm đến thẻ chứa giá mua"""
                        sell = buy.find_next("td")
                        
                        """Nếu tồn tại thì trích xuất giá mua ra"""
                        if sell.find_all('div'):
                            sell_price = sell.div.div.span.text
                        else:
                            """Nếu không có thẻ mua thì cho nó bằng 0"""
                            sell_price = "0"
                        
                        """Xoá khoảng trắn thừa trong loại vàng"""
                        name = " ".join(name.text.split())
                        
                        
                        """Trường hợp đặc biệt đối với Mi Hồng 950 third party bị lộn giá mua với giá bán"""
                        """Đã kiểm chứng với nhiều trang lấy giá vàng khác"""
                        if gold['id'] != "1OTHERMi_H_ng_950SJC":
                            values.append({
                                        "name" : name,
                                        "buy" : buy_price, 
                                        "sell" : sell_price}
                                        )
                        else:
                            values.append({
                                        "name" : name,
                                        "buy" : sell_price, 
                                        "sell" : buy_price}
                                        )
                """Trả về dạng dict với key là ngày tra"""
                all_golds[present_day.text] = values 
                return all_golds
            except:
                return None







'''

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ThirdPartyServerData:
    def __init__(self):
        return
    
    """Hàm lấy giá vàng"""
    def get_gold_list(date):
        all_golds = {}
        """Sử dụng thư viện requests để lấy html response"""
        URL = "https://www.sjc.com.vn/xml/tygiavang.xml"
        try:
            xml_text = requests.get(URL, verify= False)
        except requests.exceptions.ConnectionError:
            raise requests.exceptions.ConnectionError
        except requests.exceptions.Timeout:
            raise requests.exceptions.Timeout
        else:
            soup = BeautifulSoup(xml_text.content,"lxml")
            try:
                
                """Lấy ngày đang tra cứu từ xml"""
                day = str(soup.find("ratelist"))
                present_day = day[day.rfind("PM") + 3:day.rfind("PM") + 13]
                
                """Dựa vào class và id để tìm lấy dữ liệu từ xml"""

                list_gold = [str(soup.find("city", attrs = {'name':"Hà Nội"}))]
                list_gold.append(soup.find("city", attrs = {'name':"Đà Nẵng"}))
                list_gold.append(soup.find("city", attrs = {'name':"Nha Trang"}))
                list_gold.append(soup.find("city", attrs = {'name':"Cà Mau"}))
                list_gold.append(soup.find("city", attrs = {'name':"Huế"}))
                list_gold.append(soup.find("city", attrs = {'name':"Bình Phước"}))
                list_gold.append(soup.find("city", attrs = {'name':"Biên Hòa"}))
                list_gold.append(soup.find("city", attrs = {'name':"Miền Tây"}))
                list_gold.append(soup.find("city", attrs = {'name':"Quãng Ngãi"}))
                list_gold.append(soup.find("city", attrs = {'name':"Long Xuyên"}))
                list_gold.append(soup.find("city", attrs = {'name':"Bạc Liêu"}))
                list_gold.append(soup.find("city", attrs = {'name':"Quy Nhơn"}))
                list_gold.append(soup.find("city", attrs = {'name':"Phan Rang"}))
                list_gold.append(soup.find("city", attrs = {'name':"Hạ Long"}))
                list_gold.append(soup.find("city", attrs = {'name':"Quảng Nam"}))
               
                """Danh sách trả về gồm loại vàng,giá mua,giá bán"""
                values = []
                for gold in list_gold:
                    if gold == None:
                        continue
           
                    name = str(gold)
                    name = name[name.rfind("name=") + 6: name.find("\">")]
                    name = "SJC " + name

                    buy_price  = str(gold)
                    buy_price = buy_price[buy_price.rfind("buy=") + 5: buy_price.rfind("buy=") + 11]
                    buy_price = buy_price.replace('.', ',')

                    sell_price = str(gold)
                    sell_price = sell_price[sell_price.rfind("sell=") + 6: sell_price.rfind("sell=") + 12]
                    sell_price = sell_price.replace('.', ',')

                    values.append({
                                "name" : name,
                                "buy" : sell_price, 
                                "sell" : buy_price}
                                )
                """Trả về dạng dict với key là ngày tra"""
                all_golds[present_day] = values 
                return all_golds
            except:
                return None


URL = "https://www.sjc.com.vn/xml/tygiavang.xml"
        #URL = f"https://tygia.com/api.php?column=0&cols=1&title=1&chart=0&gold=1&rate=0&expand=2&nganhang=VIETCOM&ngay={date}"

xml = requests.get(URL, verify= False)
soup = BeautifulSoup(xml.content, 'lxml') 

xll = soup.find("city", attrs = {'name':"Hồ Chí Minh"})
xxl2 = xll.find("item", attrs = {'type': "Vàng SJC 1L - 10L"})
gold = xll.find('item')
#print(str(gold).replace('.', ','))
#print(xxl2)

day = str(soup.find("ratelist"))

#print(day[day.rfind("PM") + 3:day.rfind("PM") + 13]) # Ngày


list_gold = [str(soup.find("city", attrs = {'name':"Hà Nội"}))]
ds = str(soup.find("city", attrs = {'name':"Nha Trang"}))
list_gold.append(ds)
print(list_gold)
hanoi = soup.find("city", attrs = {'name':"Hà Nội"})
# print(hanoi)

name = str(hanoi)
print(name.find("\">"))
name = name[name.rfind("name=") + 6: name.find("\">")]
print(name)

# buy_price  = str(hanoi)
# buy_price = buy_price[buy_price.rfind("buy=") + 5: buy_price.rfind("buy=") + 11]
# print(buy_price.replace('.', ','))

# sell_price = str(hanoi)
# sell_price = sell_price[sell_price.rfind("sell=") + 6: sell_price.rfind("sell=") + 12]
# print(sell_price.replace('.', ','))


ngay = {}
vang = ThirdPartyServerData.get_gold_list(ngay)

print(vang)

import time
from datetime import datetime,timedelta
date = datetime.now()
print(date)
date = date.strftime("%Y%m%d")


'''
