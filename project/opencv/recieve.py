import time
import serial

number = []
file = open("phonebook.txt","r")
lines = file.readlines()
file.close()

for line in lines:
    number.append((line.strip()).encode())
    
    
def r():
    global number
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
        return "YES"
    if data[-11:-9].upper()==b'NO' and data[-52:-40] in number:
        return "NO"
    else:
        return "STOP"

