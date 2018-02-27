#!/usr/bin/env python
def checkForValideLine(line):
	if splitedLine[3] !="" and splitedLine[4] !="" and splitedLine[5] !="" and re.match("[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", splitedLine[4].lower()):
		return True
	else:
		return False
def parceToDhcp(filename, skip):
	f = open(filename,'r')
	lineIndex = 0
	if skip:
		f.readline()
		lineIndex = lineIndex + 1
	config = ""
	for line in f:
		lineIndex = lineIndex + 1
		splitedLine = line.split(',')
		if checkForValideLine(splitedLine):
			config = config + "host {} {} hardware ethernet {} ; fixed-address {} ; {}\n".format(splitedLine[3].strip()
				,chr(123), splitedLine[4].strip().lower().replace("-",":"),
				splitedLine[5].strip(),chr(125))
		else:
			sys.stderr.write ("[error] The line was excluded due some error {}\n".format(lineIndex))
	print (config)
	return
def parceToIptablesLimits(filename, skip):
	# 192.168.69.199 199 6 700
	f = open(filename,'r')
	lineIndex = 0
	if skip:
		f.readline()
		lineIndex = lineIndex + 1
	config = ""
	for line in f:
		lineIndex = lineIndex + 1
		splitedLine = line.split(',')
		if splitedLine[3] !="" and splitedLine[4] !="" and splitedLine[5] !="" :
			config = config + "{} {} {} {}\n".format(splitedLine[5].strip(), lineIndex,
				splitedLine[6].strip(),splitedLine[7].strip())
		else:
			sys.stderr.write ("[error] The line was excluded due some error {}\n".format(lineIndex))
	print (config)
	return

def parceToIptablesAccess():
	print ("Iptables")
	return

if __name__ == "__main__":
	import argparse
	import os.path
	import sys
	import re
	parser = argparse.ArgumentParser(description="CSV to dhcp and iptables parser")
	parser.add_argument("-f","--file",required=True,
						metavar='FILE', dest="filename", type=str, 
						help="File name with host name, mac and ip address")
	parser.add_argument("-s", "--service",required=True, metavar='string', type=str, 
						help="Value like a dhcp or iptable")
	parser.add_argument("--includetitle", 
						default=True,
						action="store_false",
						dest="includetitle",
						help="To include title or first line of document")
	parser.add_argument("--debug", 
						default=False,
						action="store_true",
						dest="debug",
						help="For enable the debug messages and additional information")
	args = parser.parse_args()
	if args.debug:
		print ("File name value :{}".format(args.filename))
		print ("Service value :{}".format(args.service))
		print ("Include titel value :{}".format(args.includetitle))

	if args.service == "dhcp":
		parceToDhcp(args.filename, args.includetitle)
	elif args.service == "iptableslimits":
		parceToIptablesLimits(args.filename, args.includetitle)
	else:
		print ("The --service key must has value dhcp or iptables only. You set '{}', it is incorrect".format(args.service))
	