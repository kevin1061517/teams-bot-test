import webbrowser
from msal import ConfidentialClientApplication
import requests

client_secret = 'Eq28Q~KW.E9d.gsE3K.QMyLt0f6twP3z9BgeXaNI'
app_id = '8f5e553f-d887-4da1-8417-0b77afada1e7'
SCOPES = ['User.Read']

client = ConfidentialClientApplication(client_id=app_id, client_credential=client_secret)


def get_authorization_code():
    # # Get Access token
    authorization_url = client.get_authorization_request_url(SCOPES)
    print(authorization_url)
    webbrowser.open(authorization_url)


def get_access_token(authorization_code):
    access_token = client.acquire_token_by_authorization_code(code=authorization_code, scopes=SCOPES)
    print(access_token)
    access_token_id = access_token['access_token']
    print(access_token_id)
    return access_token_id


def get_profile():
    me_url = 'https://graph.microsoft.com/v1.0/me'
    user_info_response = requests.get(me_url, headers=headers)
    print(user_info_response)
    print(user_info_response.text)


def get_chat_response():
    chat_base_url = 'https://graph.microsoft.com/v1.0/users/73822e0d7b3a830b/chats'
    chat_info_response = requests.get(chat_base_url, headers=headers)
    print(chat_info_response)
    print(chat_info_response.text)


if __name__ == '__main__':
    get_authorization_code()
    z_authorization_code = 'M.R3_BAY.9283d41f-e9d8-7386-5754-da23303787fa'
    while True:
        z_authorization_code = input("Input your access_token")
        if z_authorization_code != '':
            break

    z_access_token_id = get_access_token(z_authorization_code)
    headers = {'Authorization': 'Bearer ' + z_access_token_id}

    get_profile()
    get_chat_response()
