import tweepy

# Replace with your actual API credentials
TWITTER_API_KEY = "bdq4SFZcn0dKanbhIxsePOG6r"
TWITTER_API_SECRET = "Tr0EO3oceus2SfwubR0GbwVItfZ5NzzdqNSjocexef8pCoUmth"
TWITTER_ACCESS_TOKEN = "1851594670251319296-wSK5FD2VQ1CRTzrfAS0pVW9cmguq5O"
TWITTER_ACCESS_SECRET = "FdN1IwZYwe7tFDGoNBBc8N1utEcmzrI92FX6hKLhNBIfm"

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
api = tweepy.API(auth)

# Test API functionality
try:
    api.verify_credentials()
    print("Authentication successful!")
    api.update_status("Hello world! This is Gnosis testing its wings!")
except tweepy.errors.Unauthorized as e:
    print("Error: Unauthorized")
    print(e)
except Exception as e:
    print("Error:", e)
