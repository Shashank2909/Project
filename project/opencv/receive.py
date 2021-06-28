import time
import serial

def r():
    number = [b'918830994639',b'917083242732']
    data = 0
    phone = serial.Serial("/dev/ttyS0", 9600, timeout=5)
    phone.write(b'ATZ\r')
    # print(phone.readall())

    phone.write(b"AT+CMGF=1\r")
    # print(phone.readall())

    phone.write(b'AT+CMGL="ALL"\r')
    data = phone.readall()
    print("waiting....")
    time.sleep(1)
    phone.write(b'AT+CMGD=1,1\r')
    #d = phone.readall()
    time.sleep(1)
    print("-------------------------------------")
    print(data[-11:-8])
    print(data[-52:-40])
    if data[-11:-8].upper()==b'YES' and data[-52:-40] in number:
        print("true")
        return True
    else:
        print("false")
        return False

