#!/usr/bin/python
import numpy as np
import serial
import rospy
from sensor_msgs.msg import NavSatFix


def gps_talker():
	# create publisher node
	rospy.init_node('gps_talker1',anonymous=True)
	gps_pub=rospy.Publisher('gps/fix',NavSatFix, queue_size=10)

	msg=NavSatFix()
	seq=0
	fix=0

	raw = serial.Serial("/dev/ttyACM0", baudrate=115200,timeout=5)
	f=open("location.txt","w")
	f.write('Lat,Long,Alt\n')
	try:
		while not rospy.is_shutdown():
			check=raw.readline().decode("utf-8")
			# print (check[:3].decode("utf-8")== "Fix")
			if check[:3] == "Fix":
				fix = int(raw.readline().decode("utf-8"))
				print ("fix: {}".format(fix))
				if fix == 1:                        
					lat=raw.readline().decode("utf-8")
					log=raw.readline().decode("utf-8")
					alt=raw.readline().decode("utf-8")
					print ("lat: {}".format(lat))
					print ("log: {}".format(log))
					print ("alt: {}".format(alt))
					f.write(lat)
					f.write(log)
					f.write(alt)
					seq += 1
					msg.header.seq=seq
					msg.header.stamp=rospy.Time.now()
					msg.header.frame_id = 'world'
					msg.status.status=fix
					msg.status.service =int(0)
					msg.latitude=float(lat)
					msg.longitude=float(log)
					msg.altitude=float(alt)
					msg.position_covariance_type=int(0)
					gps_pub.publish(msg)


	except KeyboardInterrupt:
		raw.close()
		f.close()
     

if __name__ == '__main__':
	try:
		gps_talker()
	except rospy.ROSInterruptException:
		pass
