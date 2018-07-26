import boto3
import paramiko
import time
import logging
from botocore.client import Config

NOT_FOUND=-1


class n15xxcommands:
	channel=None
	sshclient=None

	def __init__(self, username, key, switchip, port):
		clone=self

		try:
			clone.sshclient = paramiko.SSHClient()
			clone.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			clone.sshclient.connect(hostname = switchip, port = port, username = username, key_filename = key)
			clone.channel = clone.sshclient.invoke_shell()
		except:
			print ('cannot connect to switch')
			raise

	def show_running_config (self):
		self.enable()
		self.exe ('show running-config')
	def tftp_backup(self, path, filename):
		self.enable()
		self.exe ('copy running-config ' + path + filename+'.txt')
		self.exe ('y')

#	def port_configuration (self, interface, stack, port, mode, dot1x, dot1x_port_control, guest_vlan, vlan):
#		self.enable()
#		self.exe('configure')
#		self.exe('interface ' + interface + ' ' + stack + port)
#		self.exe('switchport mode '+mode)
#		if (dot1x):
#			self.exe('dot1x port-control '+dot1x_port_control)
#		if (guest_vlan):
#			self.exe ('dot1x guest-vlan')
#			self.exe('dot1x guest-vlan'+vlan)
#		else:
#			self.exe('no dot1x guest-vlan')
			#run_command
	def exe(self, command, printoutput=False):

		buff_size=2024
		c=command + '\n'
		self.channel.send(c)

		#wait for results to be buffered
		while not (self.channel.recv_ready()):
			if self.channel.exit_status_ready():
				print ('Channel exiting. No data returned')
				return
			time.sleep(1)

		#print results
		while self.channel.recv_ready():
			output=self.channel.recv(buff_size)
			if printoutput==True:
				print(output)

		#WatchGuard errors have ^ in output
		#throw an exception if we get a WatchGuard error
		if output.find('^')!=NOT_FOUND or output.find('Error')!=NOT_FOUND:
			raise ValueError('Error executing firebox command: ' + output, command)

		return output
	def enable(self):
		self.exe('enable')

