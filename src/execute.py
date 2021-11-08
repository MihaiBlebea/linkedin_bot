import requests
import argparse

from ln_oauth import auth, headers


class LifecycleState():
	DRAFT: str = "DRAFT"
	PUBLISHED: str = "PUBLISHED"

class Publisher():

	profile_url = "https://api.linkedin.com/v2/me"

	post_url = "https://api.linkedin.com/v2/ugcPosts"

	credentials_file = "credentials.json"

	def __init__(self):
		pass

	def __get_user_information(self):
		'''
		Get user information from Linkedin
		'''
		r = requests.get(self.profile_url, headers=self.__get_headers())
		
		if r.status_code != 200:
			return None

		return r.json()

	def __get_headers(self):
		return headers(self.__get_access_token())

	def __get_access_token(self):
		return auth(self.credentials_file)

	def post_update(self, message: str):
		# Get user id to make a UGC post
		user_info = self.__get_user_information()
		if user_info is None:
			return None

		urn = user_info['id']

		# UGC will replace shares over time.
		author = f'urn:li:person:{urn}'

		post_data = {
			"author": author,
			"lifecycleState": LifecycleState.PUBLISHED,
			"specificContent": {
				"com.linkedin.ugc.ShareContent": {
					"shareCommentary": {
						"text": message
					},
					"shareMediaCategory": "NONE"
				}
			},
			"visibility": {
				"com.linkedin.ugc.MemberNetworkVisibility": "CONNECTIONS"
			}
		}

		r = requests.post(
			self.post_url, 
			headers=self.__get_headers(), 
			json=post_data
		)

		if r.status_code != 200:
			return None

		return r.json()

def main():
	parser = argparse.ArgumentParser(
		prog= "linkedin_bot", 
		usage="%(prog)s [options]", 
		description="post update on linkedin.",
	)

	parser.add_argument(
		"-m",
		dest="message",
		required=True, 
		help="message to post",
	)

	parser.add_argument(
		"-f",
		dest="force",
		required=False, 
		default=False,
		help="force to post the same message without checking the db",
	)

	args = parser.parse_args()

	publisher = Publisher()
	publisher.post_update(args.message)

if __name__ == '__main__':
	main()
