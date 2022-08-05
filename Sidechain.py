
DEFAULT_SEARCH_LIMIT = 30

class Sidechain:

	"""
	 Gets metadata for a contract address
	    contract_address : str
	    returns Sidechain Metadata
	"""
	def metadata(contract_address):
	    pass


	"""
	For a wallet address, get a list of contracts where they’ve downloaded stems
	along with time of download
	    wallet_address : Wallet Address
	    returns [{contract_address : Contract Address, timestamp : int}] 
	"""
	def get_downloads(wallet_address):
	    pass



	"""
	authorization required
	Downloads stems and adds contract to a wallets’ list of downloads
	    body: 
	        wallet_address : Wallet Address
	        contract_address : Contract Address
	    returns [{track_name : String, file : File Link}]
	"""
	def download_stems(wallet_address, contract_address):
	    pass

	"""
	Gets a list of contract addresses
	    params :
	        sort : “trending” | “recent” | “top”
	        search : String
	        limit : int (default : 30)
	        offset : int (default : 0) 
	    returns [Contract Address]
	"""
	def get_works(sort, search, limit = DEFAULT_SEARCH_LIMIT, offset = 0):
	    pass


	#authorization required
	"""
	Posts a comment to a contract address
	    body :
	        wallet_address : Wallet Address
	        contract_address : Contract Address
	        text : String
	"""
	def comment_work():
	    pass


	#authorization required
	"""
	Likes a contract address
	    body :
	        wallet_address : Wallet Address
	        contract_address : Contract Address
	"""
	def like_work():
	    pass

	"""
	Given a user, get collection of created works
	    user : Wallet Address
	    returns  [Contract Address]
	"""
	def get_works_by_user(user):
	    pass


	"""
	Given required metadata params, create a work
	    body:
	        data : Sidechain Metadata
	"""
	def upload_work():
	    pass
