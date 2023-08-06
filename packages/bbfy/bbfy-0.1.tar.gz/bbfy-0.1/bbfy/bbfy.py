# Import important imports
import requests
import base64
import datetime
import pytz

# ? Decorators
# * Decorator to check if there is a token
def require_token(method):
	def wrapper(ref, *args, **kwargs):
		if not ref.has_access_token:
			raise Exception('This needs an access token!')
		if ref.did_expired_token():
			raise Exception('This token already expired!')
		
		return method(ref, *args, **kwargs)
	return wrapper


# Create the spotify api class
class Bubufy:
	"""
	API to consume spotify data
	"""
	# ? Attributes needed to create the object
	__client_id       = None
	__client_secret   = None
	__redirect_uri    = None
	__code_for_token  = None
	__access_token    = None
	__refresh_token   = None
	__expiration_time = None
	has_access_token  = False


	# * Constructor to be initialized
	def __init__(self, __client_id, __client_secret, __redirect_uri=None):
		"""Initialize the api with corresponding parameters

		Args:
			__client_id (string): Client id from your spotify app, you can get it from
			the dashboard in https://developer.spotify.com/
			__client_secret (string): As the client id this is required and you can also 
			get it from the developer dashboard for spotify
			__redirect_uri (string, optional): If your application runs on a web server
			you must provide a redirect url for the user to be redirected after been 
			logged in. Defaults to None for non web applications.
		"""
		self.__client_id     = __client_id
		self.__client_secret = __client_secret
		self.__redirect_uri  = __redirect_uri


	# ! Handle possible errors
	def detect_error(self, r):
		status = r.status_code
		e = False
		if not status in range(200, 300):
			print('----------------')
			print(f'Error, status: {status}')
			print('----------------')
			e = True
		
		return status, e


    # * Method to get the auth url
	def get_auth_url(self, scopes=''):
		# Define the endpoint
		endpoint = 'https://accounts.spotify.com/authorize'
		# Define the query parameters
		query_parameters = {
            'client_id'    : self.__client_id,
            'response_type': 'code',
        }
		# Check if there is redirect uri
		if self.__redirect_uri:
			query_parameters['redirect_uri'] = self.__redirect_uri
		# Add scopes if exist, if not just going to be able to access public data
		if scopes:
			query_parameters['scope'] = ','.join(scopes)
		
		# Requesting get for authorization.
		r = requests.get(
            endpoint, 
            params=query_parameters
		)

		# Handle error things
		status, e = self.detect_error(r)
		if e:
			print('--------------')
			print('We cannot get the auth url')
			print('--------------')
			raise Exception(f'Sorry, auth url not collected: {status}')

		return r.url
    

	# * Method to set the code for the token
	def set_code_for_token(self, code=None):
		if not code:
			raise Exception("You need to pass a code")
		
		self.__code_for_token = code
		return self


	""" Methods to handle the token logic """
	# * Set the token
	def set_token(self, token=None, expiration_time=None):
		# If a token is specified, just define it
		if token and expiration_time:
			self.__access_token    = token
			self.has_access_token  = True
			self.__expiration_time = expiration_time
			return self
		# Create the endpoint and query parameters
		endpoint = 'https://accounts.spotify.com/api/token'
		query_parameters = {
			'grant_type'   : 'authorization_code',
            'code'         : self.__code_for_token,
		}
		if self.__redirect_uri:
			query_parameters['redirect_uri'] = self.__redirect_uri

		# Define headers with the encode base 64 credentials
		client_credentials = f'{self.__client_id}:{self.__client_secret}'
		client_credentials_b64 = base64.b64encode(client_credentials.encode()).decode()
		headers = {
            'Authorization' : f'Basic {client_credentials_b64}'
        }

		# Make the post request
		r = requests.post(
			url=endpoint,
			data=query_parameters, 
			headers=headers
		)
		# Handle errors
		status, e = self.detect_error(r)
		if e:
			print('-------------')
			print('We can not set the token')
			print('-------------')
			raise Exception(f'Sorry, no token available: {status}')
		
		# Store the token
		response = r.json()
		self.__access_token   = response['access_token']
		self.has_access_token = True
		# Set the expiration
		self.set_expiration_time(response)
		# Set the refresh token
		self.set_refresh_token(response['refresh_token'])
		

	# * Store the expiration token time
	def set_expiration_time(self, response):
		expires_in = response['expires_in']
		time_now   = datetime.datetime.now()
		self.__expiration_time = time_now + datetime.timedelta(seconds = expires_in)


	# * Check if it is expired
	def did_expired_token(self):
		# Transform both to aware dates with pytz
		time_now = datetime.datetime.now()
		time_now = time_now.replace(tzinfo=pytz.UTC)
		expiration = self.__expiration_time.replace(tzinfo=pytz.UTC)
		return expiration < time_now


	# * Set the refresh token
	def set_refresh_token(self, refresh_token):
		self.__refresh_token = refresh_token


	# * Get the headers for use the spotify api
	@require_token
	def __get_headers_authorization(self):
		return {
			'Accept'       : 'application/json',
			'Content-Type' : 'application/json',
			'Authorization': f'Bearer {self.__access_token}' 
		}


	def refresh_access_token(self):
		# Create the endpoint and query parameters
		endpoint = 'https://accounts.spotify.com/api/token'
		query_parameters = {
			'grant_type'   : 'refresh_token',
			'refresh_token': self.__refresh_token,
		}
		# Get the headers
		headers = self.__get_headers_authorization()
		# Make post request
		r = requests.post(
			url=endpoint,
			data=query_parameters,
			headers=headers
		)
		# Handle errors
		status, e = self.detect_error(r)
		if e:
			print('-------------')
			print('We can not set the token from this refreshed token')
			print('-------------')
			raise Exception(f'Sorry, no token available, for refresh token: {status}')

		# Store the token
		response = r.json()
		self.__access_token   = response['access_token']
		self.has_access_token = True
		# Set the expiration
		self.set_expiration_time(response)
		# Check if did expired
		self.set_did_expired()
		# Set the refresh token
		self.set_refresh_token(response['refresh_token'])


	# * Method that request for user data
	@require_token
	def get_user_data(self):
		# Create endpoint and headers
		endpoint = 'https://api.spotify.com/v1/me'
		headers = self.__get_headers_authorization()

		# Make the get request
		r = requests.get(endpoint, headers=headers)

		# Handle Errors
		status, e = self.detect_error(r)
		if e:
			print('-------------')
			print('We can not collect user info')
			# print(r.text)
			print('-------------')
			raise Exception(f'Sorry, something went wrong:{status}')
		
		# Return the data
		return r.json()

	
	# * Method to get the top favorite artists or tracks
	@require_token
	def get_top(self, type='tracks', time_range='medium_term', limit='20', offset='0'):
		# Create the endpoint and query parameters
		endpoint = 	f'https://api.spotify.com/v1/me/top/{type}'
		query_parameters = {
			'time_range': time_range,
			'limit': limit,
			'offset': offset,
		}
		# Get the authorization headers
		headers = self.__get_headers_authorization()

		# Make the get request
		r = requests.get(
			url=endpoint,
			params=query_parameters,
			headers=headers
		)

		# Handle errors
		status, e = self.detect_error(r)
		if e:
			print('-------------')
			print('We can not collect user top data')
			# print(r.text)
			print('-------------')
			raise Exception(f'Sorry, something went wrong:{status}')

		# Return the data if no erros
		return r.json()


	# * Method to get the top favorite artists or tracks
	@require_token
	def get_recent(self, limit='20', after=None, before=None):
		# Create the endpoint and query parameters
		endpoint = 	'https://api.spotify.com/v1/me/player/recently-played'
		query_parameters = {
			'limit': limit,
		}
		if after:
			query_parameters['after'] = after
		elif before:
			query_parameters['before'] = before
		# Get the authorization headers
		headers = self.__get_headers_authorization()

		# Make the get request
		r = requests.get(
			url=endpoint,
			params=query_parameters,
			headers=headers
		)

		# Handle errors
		status, e = self.detect_error(r)
		if e:
			print('-------------')
			print('We can not collect user recent data')
			print('-------------')
			raise Exception(f'Sorry, something went wrong:{status}')

		# Return the data if no erros
		return r.json()


	# ! Method not recommended to use
	def get_access_token(self):
		return self.__access_token, self.__expiration_time


if __name__ == "__main__":
	pass