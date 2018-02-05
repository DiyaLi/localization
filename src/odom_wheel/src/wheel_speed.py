import serial
import time
from binascii import unhexlify
import math
import binascii
import rospy
from std_msgs.msg import Float64
import numpy as np

def printmsg(ser):
    out = ser.read()
    output = ""
    while out is not "":
        output +=out
        out=ser.read()
    print('Receiving...'+output)

if __name__ == '__main__':
    # Open a file for save test result
    file = open('Oct_10_test.txt','w')
    file.write("Test Start!!! \n")

    rospy.init_node('wheel_encoder',anonymous=True)
	wheel_pub=rospy.Publisher('wheel/vel',Float64, queue_size=10)

	msg=Float64()

    # Setup OBD2
    ser = serial.Serial('COM13', 115200, timeout=1)
    # setup port for FPGA
    # port =serial.Serial(

    #         "COM23",
    #         baudrate=9600,
    #         parity=serial.PARITY_NONE,
    #         stopbits=serial.STOPBITS_ONE,
    #         bytesize=serial.EIGHTBITS,
    #         writeTimeout = 10,
    #         timeout = 1)


    # # setup parameter for frame rate control
    # ImgL = 1.428
    # #dist = 2.6
    # n = 5

    # #overP = 1-(dist-ImgL)/4/ImgL
    # s = ImgL/n

    if ser.isOpen():
        print(ser.name + ' is open...')
        ser.write('ATI\r\n')
        printmsg(ser)
        ser.write('ATZ\r\n')
        printmsg(ser)
        #ser.write('ATDP\r\n')
        # you may need to change for different car
        ser.write('ATSP6\r\n')
        printmsg(ser)
        ser.write('ATL1\r\n')
        printmsg(ser)
        #ser.write('ATE1\r\n')
        ser.write('ATH1\r\n')
        printmsg(ser)
        #ser.write('ATS1\r\n')
        ser.write('ATAL\r\n')
        printmsg(ser)
        # you may need to change for different car
        ser.write('ATTP6\r\n')
        printmsg(ser)
        ser.write('AT SH 7E0\r\n')
        printmsg(ser)

    try:
        while True:
            start=time.clock()
            print 'Test Started',start
            cmd="01 0D"
            #cmd = raw_input("Enter command or 'exit':")
            #time.sleep(0.2)
            if cmd == 'exit':
                ser.close()
                exit()
            else:
                ser.write(cmd.encode('ascii')+'\r\n')
                out = ser.read()
                output = ""
                while out is not ">":
                    output +=out
                    out=ser.read()
                print('Receiving...'+output)
                #time.sleep(0.1)
                test=output.split('\r\n')
                tmp=test[-3]
                print "Trans_msg...",tmp[12:]
                result="".join(tmp[12:].split()[::-1])
                result=int(result,16)
                convV=result*0.621371
                print "Vehicle Speed...",result,"km/h"
                print "Vehicle Speed...",convV,"mph"

        #############################################################################
                # # Test with adding arduino part
                # # Calculate the desired frame rate
                speed = result/3.6
                msg.data=speed
                wheel_pub.publish(msg)


                #frameR = int((1.1*speed-overP*ImgL)/((1-overP)*ImgL))
                # frameR = int(speed/s)
                # check if frameR smaller than the minimum frame rate
                #if frameR < 0:
                    #frameR = 0
                # if frameR > 100:
                #     frameR = 100

                # print "frame rate: ", frameR

                # # convert the value to binary string
                # binaryString='{0:08b}'.format(frameR)
                # # convert the binary to ascii
                # sendData="".join([chr(int(binaryString[i:i+8],2)) for i in range(0,len(binaryString),8)])

                # port.write(sendData)
                # print 'Data send to FPGA ', frameR
                # time.sleep(0.01)

                currentT = (time.clock()-start)*1000
                print "Current time: ",currentT,"ms"
                #time.sleep(0.3)

                # save data into txt file
                # file.write("Time in ms: "+str(currentT)+'\n')
                # file.write("Vehicle Speed in kph: "+str(result)+'\n')
                file.write("Vehicle Speed in m/s: "+str(speed)+'\n')
                # file.write("Vehicle Speed in mph: "+str(convV)+'\n')

                # file.write("Frame rate in fps: "+str(frameR)+'\n')
    except KeyboardInterrupt:
        file.close()
        ser.close()
        # port.close()

