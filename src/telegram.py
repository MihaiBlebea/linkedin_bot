import requests

def send_message(message : str, bot_token : str, chat_id : str) -> dict:
	data = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
	url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
	r = requests.post(url, data=data)
	
	if r.status_code != 200:
		return None

	return r.json()
