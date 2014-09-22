#Simple data structure that contains the login informatiom

_authconfig = {
    'dvwa': ('admin', 'password'),
    'bodgeit': ('cac4487@rit.edu', 'password')
}

def get_auth_info(auth_name):
	if auth_name in _authconfig:
		return _authconfig[auth_name]
	else:
		return ()