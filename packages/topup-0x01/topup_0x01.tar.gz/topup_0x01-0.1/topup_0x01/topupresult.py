from topup_0x01.topupx1 import Topup

# ตั้งค่า
path = "top.csv"
alert_1 = "ระบบกำลังทำการเติมเงิน"
alert_2 = "[alert] คุณได้ทำการเติมเงิน {} บาท สำเร็จ"
alert_3 = "[alert] {} ได้ทำการเติมเงินจำนวน {} บาท เมื่อ {}"

use = Topup(path, alert_1, alert_2, alert_3)

# เติมเงิน
use.topup(name, 1000)
# เช็คประวัติการเติม
use.check_topup(name)
