#!/usr/bin/python

"""
http://docs.python.org/library/email-examples.html


Need the following options:
-t, to address
-f, from address
-s, subject
-m, file with message
-l,log file
--server=smtp.blah.com:port
--user
--pass
"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from optparse import OptionParser, OptionGroup
from time import gmtime, strftime

def load_content(path_to_content):
	try:	
		file = open(path_to_content, 'r')
		body = MIMEText(file.read(), 'html')
		file.close()
		return body, True
	except Exception:
		return None, False
	

def check_smtp(smtp_server):
	port_check = smtp_server.split(':')
	if len(port_check) > 1:
		return smtp_server
	else:
		return smtp_server + ":25"
	

def build_message(msg_subject, msg_to, msg_from, msg_body):
	msg = MIMEMultipart()
	msg['Subject'] = msg_subject
	msg['From'] = msg_from
	msg['To'] = msg_to
	msg.attach(msg_body)
	return msg
	
def send_message(server,(username, password), 
				 sender, receiver, message):
		server_values = server.split(':')
		if len(server_values) != 2:
			error_msg = "Invalid format of server, expecting <server_name>:<port>"
			print(error_msg)
			return False, error_msg
		else:
			server, server_port = server.split(':')
			smtpObj = smtplib.SMTP(server, int(server_port))
			if username != None:
				smtpObj.login(username, password)
			smtpObj.sendmail(sender, receiver, message.as_string())
			smtpObj.quit()
			return True, None

def get_time_stamp():
	log_time = strftime("%Y%m%d%H%M%S", gmtime())
	return log_time	
	
def write_to_log(log, text):
	file = open(log, 'a')
	file.write("{0}\t{1}".format(get_time_stamp(), text))
	file.close()

def help_msg():
	response = "\nPlease use -h or --help to review possible options.\n"
	response += "At minimum, you must provide a to, from, subject and message\n"
	response += "\nExample:\n"
	response += "\tquick_mail.py -t target@mail.com -f badguy@badmail.com \n\t-s \"its me!\" -m msg.html --server=flyinglemur.com:25\n"
	return response
	
def set_options():
	parser =OptionParser(usage="%prog [options]", version="%prog 1.0.1")
	parser.add_option("-t", action="store", dest='TO_ADDR', default=None, 
								help="The target's email")
	parser.add_option("-f", action="store", dest='FROM_ADDR', default=None,
								help='The from address')
	parser.add_option('-s', action="store", dest='SUBJECT', default=None,
								help='Subject of the email')
	parser.add_option('-m', action="store", dest='MSG',
								help='The path to message content')
	parser.add_option('-l', action="store", dest='LOG_FILE', default='qmail_log.txt',
								help='Path and name of the log file, by default all log messages are written to ./qmail_log.txt')
	group = OptionGroup(parser, "SMTP Server options", "Provide values for authenticating to your service to send mail from.  Note: if you are sending directly to a target service you may not need to supply credentials.")
	group.add_option('--server', action="store", dest='SERVER', default=None,
								help='The address and port of the server; example: someMailService.com:25')
	group.add_option('--user', action="store", dest='USER', default=None,
								help='Username for the account, if needed')
	group.add_option('--pass', action="store", dest='PASS', default=None,
								help='Password for the account if needed')								
	parser.add_option_group(group)
	options, args = parser.parse_args()
	return options	
	
if __name__ == '__main__':
	options = set_options()
	if options.TO_ADDR == None or options.FROM_ADDR == None or options.MSG == None:
		print(help_msg())
	else:
		print("Sending to => {0}".format(options.TO_ADDR))
		body, status = load_content(options.MSG)
		if status == True:
			message = build_message(options.SUBJECT, options.TO_ADDR, options.FROM_ADDR, body)
			server = check_smtp(options.SERVER)
			try:
				status, error_msg = send_message(server,(options.USER, options.PASS), options.FROM_ADDR, options.TO_ADDR, message)
				if status == True:
					print("Successfully sent email")
					write_to_log(options.LOG_FILE, 
					"Successfully sent email:\tTo:{0}\tFrom:{1}\tSubject:{2}\n".format(options.TO_ADDR, options.FROM_ADDR, options.SUBJECT))
				else:
					write_to_log(options.LOG_FILE, 
					"Failed to send email, {3}:\tTo:{0}\tFrom:{1}\tSubject:{2}\n".format(options.TO_ADDR, options.FROM_ADDR, options.SUBJECT, error_msg))
			except Exception as e:
				print("Error in sending message: {0}".format(e))
		elif status == False:
			error_msg = "Failed to open message content"
			print(error_msg)
			write_to_log(options.LOG_FILE, 
			"Failed to send email, {3}:\tTo:{0}\tFrom:{1}\tSubject:{2}\n".format(options.TO_ADDR, options.FROM_ADDR, options.SUBJECT, error_msg))
		
