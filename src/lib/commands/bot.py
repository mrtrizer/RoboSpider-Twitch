import serial
import time
import thread
import threading

# # Serial port parameters
serial_speed = 9600
serial_port = '/dev/tty.HC-05-DevB' # bluetooth shield hc-06
max_command_length = 7

commandIsSendingGlobal = False
commandIsSendingLock = threading.Lock()

def sendCommands(commandList):
	global commandIsSendingGlobal
	global commandIsSendingLock
	# carry out validation
	try:
		print "Conecting to serial port ..."
		ser = serial.Serial(serial_port, serial_speed, timeout=1)
		print "Sending commands"
		commandIsSendingLock.acquire()
		print "Current state" + str(commandIsSendingGlobal)
		commandIsSendingGlobal = True
		print "Processing started"
		commandIsSendingLock.release()
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
	commandIsSendingLock.acquire()
	print "Current state" + str(commandIsSendingGlobal)
	commandIsSendingGlobal = False
	print "Processing finished"
	commandIsSendingLock.release()

def bot(args):

	commandList = list(args[0])[0:max_command_length]
	commandList.append('s')

	commandIsSendingLock.acquire()
	commandIsSending = commandIsSendingGlobal;
	print "Current state" + str(commandIsSendingGlobal)
	commandIsSendingLock.release()

	if (commandIsSending == True):
		return "Another command is executing"
	else:
		thread.start_new_thread(sendCommands, (commandList,))
		return "Command accepted"
