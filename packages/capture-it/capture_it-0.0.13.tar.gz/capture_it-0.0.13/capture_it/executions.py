# -----------------------------------------------------------------------------
import os
from nettoolkit import Validation, STR, Multi_Execution

from .conection import Execute_Device

# -----------------------------------------------------------------------------

class Execute_By_Login(Multi_Execution):
	"""Execute the device capture by logging in to device.

	"""    	

	def __init__(self, 
		ip_list, 
		auth, 
		cmds, 
		path, 
		cumulative=False, 
		forced_login=False, 
		parsed_output=False,
		concurrent_connections=100,
		):
		"""Initiatlize the connections for the provided iplist, authenticate with provided auth parameters, and execute given commands.

		Args:
			ip_list (set, list, tuple): set of ip addresses to be logging for capture
			auth (dict): authentication parameters ( un, pw, en)
			cmds (set, list, tuple): set of commands to be captured
			path (str): path where output should be stored.
			cumulative (bool, optional): True: will store all commands output in a single file, 
				False will store each command output in differet file. Defaults to False.
				and 'both' will do both.
			forced_login (bool, optional): True: will try to ssh/login to devices even if ping respince fails.
				False will try to ssh/login only if ping responce was success. (default: False)
			parsed_output (bool, optional): True: will check the captures and generate the general parsed excel file.
				False will omit this step. No excel will be generated in the case. (default: False)
			concurrent_connections (int, optional): 100: manipulate how many max number of concurrent connections to be establish.
				default is 100.

		Raises:
			Exception: raise exception if any issue with authentication or connections.
		"""    		
		self.devices = STR.to_set(ip_list) if isinstance(ip_list, str) else set(ip_list)
		self.auth = auth
		if not isinstance(cmds, dict):
			raise Exception("commands to be executed are to be in proper dict format")
		self.cmds = cmds
		self.path = path
		self.cumulative = cumulative
		self.forced_login = forced_login
		self.parsed_output = parsed_output
		if parsed_output and not cumulative :
			self.cumulative='both'
		super().__init__(self.devices)
		try:
			self.max_connections = concurrent_connections
		except:
			print(f"Invalid number of `concurrent_connections` defined {concurrent_connections}, default 100 taken.")
		self.start()
		# self.end()

	def is_valid(self, ip):
		"""Validation function to check if provided ip is valid IPv4 or IPv6 address

		Args:
			ip (str): ipv4 or ipv6 address

		Returns:
			bool: True/False based on validation success/fail
		"""    		
		try:
			return ip and Validation(ip).version in (4, 6)
		except:
			print(f'Device Connection: {ip} :: Skipped due to bad Input')
			return False
		return True

	def execute(self, hn):
		"""execution function for a single device. hn == ip address in this case.

		Args:
			hn (str): ip address of a reachable device
		"""    		
		Execute_Device(hn, 
			auth=self.auth, 
			cmds=self.cmds, 
			path=self.path, 
			cumulative=self.cumulative,
			forced_login=self.forced_login, 
			parsed_output=self.parsed_output,
			)
