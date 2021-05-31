import time
import serial

phone = serial.Serial("/dev/ttyS0", 9600, timeout=5)

try:
    phone.write(b'ATZ\r') 
    print(phone.readall())

    phone.write(b"AT+CMGF=1\r")  
    print(phone.readall())

    while 1:
        phone.write(b'AT+CMGL="ALL"\r') 
        data = phone.readall()
        print(data)
        time.sleep(5)
finally:
    phone.close()
