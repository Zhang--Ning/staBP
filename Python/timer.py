import serial
import time

ser = serial.Serial("/dev/tty.wchusbserial1420", baudrate = 19200, timeout = 5)
time.sleep(1)

last_time = 0

while(True):
  char = ser.read()
  if char == "\n":
    current = time.time()*1000
    print current - last_time
    last_time = current

