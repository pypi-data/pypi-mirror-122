import csv
import time
import datetime

class Topup:
    # constructor
    # def __init__(self, name, money = 0.0):
    #     self.name = name
    #     self.money = money
    def __init__(self, path, alert_1, alert_2, alert_3):
        self.path = path
        self.alert_1 = alert_1 
        self.alert_2 = alert_2 
        self.alert_3 = alert_3 


    def topup(self, name, money):
        time_ = datetime.datetime.now()
        now_time = time_.strftime("%H:%M | %x")
        print(self.alert_1)
        time.sleep(2)
        with open(self.path, 'a+', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            # write the data
            data = [name, money, now_time]
            writer.writerow(data)
            print((self.alert_2).format(money))
        # print("[alert] คุณได้ทำการเติมเงิน {} บาท สำเร็จ".format(money))

    
    # ตรวจสอบการเติมเงิน
    def check_topup(self, name):
        with open(self.path, 'r', encoding='utf-8') as file:
            read = csv.reader(file)
            for i in read:
                # print(i)
                if name == i[0]:
                    print((self.alert_3).format(i[0], i[1], i[2]))
                    # print("[alert] {} ได้ทำการเติมเงินจำนวน {} บาท เมื่อ {}".format(i[0], i[1], i[2]))
