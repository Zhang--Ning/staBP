import serial
import time
import struct
ser = serial.Serial('/dev/tty.wchusbserial1420', baudrate=115200)
time.sleep(1)
ac_csv_file = open('ac_testdata.csv', 'w')
dc_csv_file = open('dc_testdata.csv', 'w')
i = 0
for x in range(480000):
  if(x%2000==0):
    seconds_total = x/200
    minutes = seconds_total/60
    seconds = seconds_total%60
    print str(minutes) + " minutes " + str(seconds) + " seconds elapsed."
  if i == 0:
    ac_csv_file.write(ser.readline());
    i = 1
  else:
    dc_csv_file.write(ser.readline());
    i = 0

ac_csv_file.close()
dc_csv_file.close()
