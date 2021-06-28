import time
import serial

def r():
    number = "917083242732"
    data = 0
    phone = serial.Serial("/dev/ttyS0", 9600, timeout=5)
    phone.write(b'ATZ\r')
    # print(phone.readall())

    phone.write(b"AT+CMGF=1\r")
    # print(phone.readall())

    phone.write(b'AT+CMGL="ALL"\r')
    data = phone.readall()
    print("waiting....")
    time.sleep(6)
   # phone.write(b'AT+CMGD=1,4\r')
    d = phone.readall()
    time.sleep(5)
    print("-------------------------------------")
    print(data[-11:-8])
    print(data[-52:-40])
    if data[-11:-8].upper()=='YES' and data[-52:-40]==number:
        return True
    else:
        return False
          

r()
