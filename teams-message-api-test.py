import webbrowser
from msal import ConfidentialClientApplication, PublicClientApplication
import requests

client_secret = 'Eq28Q~KW.E9d.gsE3K.QMyLt0f6twP3z9BgeXa..'
app_id = '8f5e553f-d887-4da1-8417-0b77afada1e7'
SCOPES = ['ChatMessage.Read', 'Chat.ReadBasic.All']

client = ConfidentialClientApplication(client_id=app_id, client_credential=client_secret)
# # Get Access token
authorization_url = client.get_authorization_request_url(SCOPES)
print(authorization_url)
webbrowser.open(authorization_url)

authorization_code = 'M.R3_BAY.898db802-6834-cde2-0e20-94dfe3225896'
access_token = client.acquire_token_by_authorization_code(code=authorization_code, scopes=SCOPES)
print(access_token)

access_token_id = access_token['access_token']
print(access_token_id)

headers = {'Authorization': 'Bearer ' + access_token_id}

me_url = 'https://graph.microsoft.com/v1.0/me'
user_info_response = requests.get(me_url, headers=headers)
print(user_info_response)
print(user_info_response.text)

chat_base_url = 'https://graph.microsoft.com/v1.0/users/73822e0d7b3a830b/chats'
chat_info_response = requests.get(chat_base_url, headers=headers)
print(chat_info_response)
print(chat_info_response.text)