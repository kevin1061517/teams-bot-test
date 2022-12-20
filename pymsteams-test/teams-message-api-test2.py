import requests
import json
from urllib import parse
import re

get_token_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
get_token_header = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
channel_message_url = 'https://graph.microsoft.com/v1.0/me'
channel_message_reply_url = 'https://graph.microsoft.com/v1.0/me'
body_data = parse.urlencode({'client_id': '8f5e553f-d887-4da1-8417-0b77afada1e7',
                             'client_secret': 'Eq28Q~KW.E9d.gsE3K.QMyLt0f6twP3z9BgeXaNI',
                             'grant_type': 'client_credentials',
                             'redirect_url': 'https://localhsot',
                             'scope': 'https://graph.microsoft.com/.default'})


class Message:
    def __init__(self, message_id, created_date_time, created_message_user, web_url, content, reply_message_list=None):
        if reply_message_list is None:
            reply_message_list = []
        self.message_id = message_id
        self.created_date_time = created_date_time
        self.created_message_user = created_message_user
        self.web_url = web_url
        self.content = content
        self.reply_message_list = reply_message_list

    def print_info(self):
        print(f'''Message: message_id: {self.message_id}, "
              content: {self.content},
              web_url: {self.web_url},
              created_date_time: {self.created_date_time},
              created_message_user: {self.created_message_user}, 
              reply_message_list: {self.reply_message_list}''')


def generate_authorization_token():
    # Get token
    get_token_response = requests.post(get_token_url, headers=get_token_header, data=body_data).text
    token_content = json.loads(get_token_response)
    access_token = token_content['access_token']
    print(access_token)

    return access_token


def get_channel_message_raw_data():
    access_token = generate_authorization_token()
    # Get message
    channel_message_headers = {"Authorization": "Bearer " + access_token}
    channel_message_response = requests.get(channel_message_url, headers=channel_message_headers)
    print(channel_message_response.text)
    return channel_message_response.text


def get_channel_message_reply(message_id):
    access_token = generate_authorization_token()
    # Get message
    channel_message_reply_headers = {"Authorization": "Bearer " + access_token}
    channel_message_reply_response = requests.get(channel_message_reply_url + message_id,
                                                  headers=channel_message_reply_headers)
    data = channel_message_reply_response.text
    data = json.loads(data)

    reply_message_list = []
    for message in data['value']:
        message_id = message['id']
        created_date_time = message['createdDateTime']
        created_message_user = message['from']['user']['displayName'] if message['from'] else 'System'
        web_url = message['webUrl']
        content = message['body']['content']
        reply_message = Message(message_id, created_date_time, created_message_user, web_url, content)
        reply_message_list.append(reply_message)

    return reply_message_list


def extractMessageContent(data):
    data = json.loads(data)
    for message in data['value']:
        message_id = message['id']
        created_date_time = message['createdDateTime']
        created_message_user = message['from']['user']['displayName'] if message['from'] else 'System'
        web_url = message['webUrl']
        content = message['body']['content']
        # reply_message_list = get_channel_message_reply(message_id)

        message = Message(message_id, created_date_time, created_message_user, web_url, content)
        message.print_info()


if __name__ == '__main__':
    # raw_data = get_channel_message_raw_data()
    raw_data = r'''{
    "@odata.context": "https://graph.microsoft.com/beta/$metadata#teams('02bd9fd6-8f93-4758-87c3-1fb73740a315')/channels('19%3Ad0bba23c2fc8413991125a43a54cc30e%40thread.skype')/messages",
    "@odata.count": 4,
    "value": [
        {
            "id": "1501527481624",
            "replyToId": null,
            "etag": "1501527481880",
            "messageType": "message",
            "createdDateTime": "2017-07-31T18:58:01.624Z",
            "lastModifiedDateTime": "2017-07-31T18:58:01.88Z",
            "lastEditedDateTime": null,
            "deletedDateTime": null,
            "subject": null,
            "summary": null,
            "chatId": null,
            "importance": "normal",
            "locale": "en-us",
            "webUrl": "https://teams.microsoft.com/l/message/19%3Ad0bba23c2fc8413991125a43a54cc30e%40thread.skype/1501527481624?groupId=02bd9fd6-8f93-4758-87c3-1fb73740a315&tenantId=dcd219dd-bc68-4b9b-bf0b-4a33a796be35&createdTime=1501527481624&parentMessageId=1501527481624",
            "onBehalfOf": null,
            "policyViolation": null,
            "eventDetail": null,
            "from": {
                "application": null,
                "device": null,
                "user": {
                    "id": "24fcbca3-c3e2-48bf-9ffc-c7f81b81483d",
                    "displayName": "Diego Siciliani",
                    "userIdentityType": "aadUser",
                    "tenantId": "dcd219dd-bc68-4b9b-bf0b-4a33a796be35"
                }
            },
            "body": {
                "contentType": "html",
                "content": "<div>We've got some new folks this week! Please introduce yourselves whether you're new or have been here forever. <span contenteditable=\"false\" title=\"smile\" type=\"(smile)\" style=\"height: 20px; width: 20px; max-height: 20px; max-width: 20px;\" class=\"animated-emoticon-20-smile\"><img alt=\"smile\" itemid=\"smile\" itemscope=\"\" itemtype=\"http://schema.skype.com/Emoji\" src=\"https://static-asm.secure.skypeassets.com/pes/v1/emoticons/smile/views/default_20\" style=\"width: 20px; height: 20px;\" class=\"emoticon-smile\"></span></div>"
            },
            "channelIdentity": {
                "teamId": "02bd9fd6-8f93-4758-87c3-1fb73740a315",
                "channelId": "19:d0bba23c2fc8413991125a43a54cc30e@thread.skype"
            },
            "attachments": [],
            "mentions": [],
            "reactions": [
                {
                    "reactionType": "like",
                    "createdDateTime": "2017-07-31T18:58:01.88Z",
                    "user": {
                        "application": null,
                        "device": null,
                        "user": {
                            "id": "40079818-3808-4585-903b-02605f061225",
                            "displayName": null,
                            "userIdentityType": "aadUser"
                        }
                    }
                }
            ]
        },
        {
            "id": "1501527474654",
            "replyToId": null,
            "etag": "1501527474654",
            "messageType": "message",
            "createdDateTime": "2017-07-31T18:57:54.654Z",
            "lastModifiedDateTime": "2017-07-31T18:57:54.654Z",
            "lastEditedDateTime": null,
            "deletedDateTime": null,
            "subject": null,
            "summary": null,
            "chatId": null,
            "importance": "normal",
            "locale": "en-us",
            "webUrl": "https://teams.microsoft.com/l/message/19%3Ad0bba23c2fc8413991125a43a54cc30e%40thread.skype/1501527474654?groupId=02bd9fd6-8f93-4758-87c3-1fb73740a315&tenantId=dcd219dd-bc68-4b9b-bf0b-4a33a796be35&createdTime=1501527474654&parentMessageId=1501527474654",
            "onBehalfOf": null,
            "policyViolation": null,
            "eventDetail": null,
            "from": {
                "application": null,
                "device": null,
                "user": {
                    "id": "8b209ac8-08ff-4ef1-896d-3b9fde0bbf04",
                    "displayName": "Joni Sherman",
                    "userIdentityType": "aadUser",
                    "tenantId": "dcd219dd-bc68-4b9b-bf0b-4a33a796be35"
                }
            },
            "body": {
                "contentType": "html",
                "content": "<div>Hey Team, the new employee handbook is here! Be sure to read through and familarize yourself with it. Let me know if you have any questions! </div>"
            },
            "channelIdentity": {
                "teamId": "02bd9fd6-8f93-4758-87c3-1fb73740a315",
                "channelId": "19:d0bba23c2fc8413991125a43a54cc30e@thread.skype"
            },
            "attachments": [],
            "mentions": [],
            "reactions": []
        },
        {
            "id": "1501527470147",
            "replyToId": null,
            "etag": "1501527471842",
            "messageType": "message",
            "createdDateTime": "2017-07-31T18:57:50.147Z",
            "lastModifiedDateTime": "2017-07-31T18:57:51.842Z",
            "lastEditedDateTime": null,
            "deletedDateTime": null,
            "subject": null,
            "summary": null,
            "chatId": null,
            "importance": "normal",
            "locale": "en-us",
            "webUrl": "https://teams.microsoft.com/l/message/19%3Ad0bba23c2fc8413991125a43a54cc30e%40thread.skype/1501527470147?groupId=02bd9fd6-8f93-4758-87c3-1fb73740a315&tenantId=dcd219dd-bc68-4b9b-bf0b-4a33a796be35&createdTime=1501527470147&parentMessageId=1501527470147",
            "onBehalfOf": null,
            "policyViolation": null,
            "eventDetail": null,
            "from": {
                "application": null,
                "device": null,
                "user": {
                    "id": "4782e723-f4f4-4af3-a76e-25e3bab0d896",
                    "displayName": "orgid:4782e723-f4f4-4af3-a76e-25e3bab0d896",
                    "userIdentityType": "aadUser",
                    "tenantId": "dcd219dd-bc68-4b9b-bf0b-4a33a796be35"
                }
            },
            "body": {
                "contentType": "html",
                "content": "<div>Meetings for Directors.</div><attachment id=\"1501527469903\"></attachment>"
            },
            "channelIdentity": {
                "teamId": "02bd9fd6-8f93-4758-87c3-1fb73740a315",
                "channelId": "19:d0bba23c2fc8413991125a43a54cc30e@thread.skype"
            },
            "attachments": [
                {
                    "id": "1501527469903",
                    "contentType": "meetingReference",
                    "contentUrl": null,
                    "content": "{\"exchangeId\":\"AQMkAGI5MWY5ZmUyLTJiNzYtNDE0ZC04OWEwLWM3M2FjYmM3NwAzZWYARgAAA_b2VnUAiWNLj0xeSOs499YHAMT2RdsuOqRIlQZ4vOzp66YAAAIBDQAAAMT2RdsuOqRIlQZ4vOzp66YAAAIJOQAAAA==\",\"organizerId\":null,\"meetingJoinUrl\":null}",
                    "name": "Directors Meeting",
                    "thumbnailUrl": null,
                    "teamsAppId": null
                }
            ],
            "mentions": [],
            "reactions": []
        },
        {
            "id": "1501527449589",
            "replyToId": null,
            "etag": "1501527449589",
            "messageType": "systemEventMessage",
            "createdDateTime": "2017-07-31T18:57:29.589Z",
            "lastModifiedDateTime": "2017-07-31T18:57:29.589Z",
            "lastEditedDateTime": null,
            "deletedDateTime": null,
            "subject": null,
            "summary": null,
            "chatId": null,
            "importance": "normal",
            "locale": "en-us",
            "webUrl": "https://teams.microsoft.com/l/message/19%3Ad0bba23c2fc8413991125a43a54cc30e%40thread.skype/1501527449589?groupId=02bd9fd6-8f93-4758-87c3-1fb73740a315&tenantId=dcd219dd-bc68-4b9b-bf0b-4a33a796be35&createdTime=1501527449589&parentMessageId=1501527449589",
            "from": null,
            "onBehalfOf": null,
            "policyViolation": null,
            "body": {
                "contentType": "html",
                "content": "<systemEventMessage/>"
            },
            "channelIdentity": {
                "teamId": "02bd9fd6-8f93-4758-87c3-1fb73740a315",
                "channelId": "19:d0bba23c2fc8413991125a43a54cc30e@thread.skype"
            },
            "attachments": [],
            "mentions": [],
            "reactions": [],
            "eventDetail": {
                "@odata.type": "#microsoft.graph.membersAddedEventMessageDetail",
                "visibleHistoryStartDateTime": "0001-01-01T00:00:00Z",
                "members": [
                    {
                        "id": "48d31887-5fad-4d73-a9f5-3c356e68a038",
                        "displayName": null,
                        "userIdentityType": "aadUser"
                    },
                    {
                        "id": "c8913c86-ceea-4d39-b1ea-f63a5b675166",
                        "displayName": null,
                        "userIdentityType": "aadUser"
                    },
                    {
                        "id": "626cbf8c-5dde-46b0-8385-9e40d64736fe",
                        "displayName": null,
                        "userIdentityType": "aadUser"
                    },
                    {
                        "id": "b66ecf79-a093-4d51-86e0-efcc4531f37a",
                        "displayName": null,
                        "userIdentityType": "aadUser"
                    },
                    {
                        "id": "df043ff1-49d5-414e-86a4-0c7f239c36cf",
                        "displayName": null,
                        "userIdentityType": "aadUser"
                    },
                    {
                        "id": "089a6bb8-e8cb-492c-aa41-c078aa0b5120",
                        "displayName": null,
                        "userIdentityType": "aadUser"
                    },
                    {
                        "id": "87d349ed-44d7-43e1-9a83-5f2406dee5bd",
                        "displayName": null,
                        "userIdentityType": "aadUser"
                    },
                    {
                        "id": "2ed03dfd-01d8-4005-a9ef-fa8ee546dc6c",
                        "displayName": null,
                        "userIdentityType": "aadUser"
                    },
                    {
                        "id": "e3d0513b-449e-4198-ba6f-bd97ae7cae85",
                        "displayName": null,
                        "userIdentityType": "aadUser"
                    },
                    {
                        "id": "40079818-3808-4585-903b-02605f061225",
                        "displayName": null,
                        "userIdentityType": "aadUser"
                    },
                    {
                        "id": "08fa38e4-cbfa-4488-94ed-c834da6539df",
                        "displayName": null,
                        "userIdentityType": "aadUser"
                    },
                    {
                        "id": "8b209ac8-08ff-4ef1-896d-3b9fde0bbf04",
                        "displayName": null,
                        "userIdentityType": "aadUser"
                    },
                    {
                        "id": "4782e723-f4f4-4af3-a76e-25e3bab0d896",
                        "displayName": null,
                        "userIdentityType": "aadUser"
                    },
                    {
                        "id": "074e56ea-0b50-4461-89e5-c67ae14a2c0b",
                        "displayName": null,
                        "userIdentityType": "aadUser"
                    },
                    {
                        "id": "16cfe710-1625-4806-9990-91b8f0afee35",
                        "displayName": null,
                        "userIdentityType": "aadUser"
                    },
                    {
                        "id": "e8a02cc7-df4d-4778-956d-784cc9506e5a",
                        "displayName": null,
                        "userIdentityType": "aadUser"
                    },
                    {
                        "id": "24fcbca3-c3e2-48bf-9ffc-c7f81b81483d",
                        "displayName": null,
                        "userIdentityType": "aadUser"
                    },
                    {
                        "id": "2804bc07-1e1f-4938-9085-ce6d756a32d2",
                        "displayName": null,
                        "userIdentityType": "aadUser"
                    },
                    {
                        "id": "ec63c778-24e1-4240-bea3-d12a167d5232",
                        "displayName": null,
                        "userIdentityType": "aadUser"
                    }
                ],
                "initiator": {
                    "application": null,
                    "device": null,
                    "user": {
                        "id": "48d31887-5fad-4d73-a9f5-3c356e68a038",
                        "displayName": null,
                        "userIdentityType": "aadUser"
                    }
                }
            }
        }
    ]
}'''
    extractMessageContent(raw_data)
