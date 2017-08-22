import serial
import time
import thread

# # Serial port parameters
serial_speed = 9600
serial_port = '/dev/tty.HC-05-DevB' # bluetooth shield hc-06
max_command_length = 5

def sendCommands(commandList):

	# carry out validation
	try:
		print "Conecting to serial port ..."
		ser = serial.Serial(serial_port, serial_speed, timeout=1)
		print "Sending commands"
		while (len(commandList) > 0):
			try:
				command = commandList[0]
				print "Command: " + command
				commandList = commandList[1:]
				ser.write(command.encode())
				time.sleep(2)
			except Exception as error:
				print "Something wrong: " + str(error)
		print "sending finish"
	except Exception as error:
		print "Something wrong: " + str(error)

def bot(args):

	commandList = list(args[0])[0:max_command_length]
	commandList.append('s')

	thread.start_new_thread(sendCommands, (commandList,))

	return "Command accepted"
