import RPi.GPIO as GPIO
import serial 
import time

def send():
    SERIAL_PORT = "/dev/ttyS0"

    ser = serial.Serial(SERIAL_PORT,baudrate=9600,timeout=5)

    ser.write("AT+CMGF=1\r".encode())
    print("Text mode enabled...")
    time.sleep(3)
    ser.write('AT+CMGS="7083242732"\r'.encode())
    msg = "chor ailo"+chr(26)
    print("sending message....")
    time.sleep(3)
    ser.write(msg.encode())
    time.sleep(3)
    print("message sent....")

send()
