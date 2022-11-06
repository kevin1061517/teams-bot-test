from flask import Flask, render_template, request
import os
import pymsteams

webhook_url = 'https://msniuedutw.webhook.office.com/webhookb2/...'

myTeamsMessage = pymsteams.connectorcard(webhook_url)

myTeamsMessage.title("Error")
myTeamsMessage.text("some Exception happen")

myTeamsPotentialAction1 = pymsteams.potentialaction(_name="Add a reply")
myTeamsPotentialAction1.addInput("TextInput", "comment", "Add a reply here", False)
myTeamsPotentialAction1.addAction("HttpPost", "Click here to reply", "https://localhost:8080/get-reply", "{{comment.value}}")
myTeamsMessage.addPotentialAction(myTeamsPotentialAction1)

myTeamsMessage.summary("Test Message")
myTeamsMessage.send()

# app = Flask(__name__)


# @app.route("/get-reply", methods=['GET'])
# def get_reply():
#     print('test')
#     reply = request.args.get('reply')
#     print(reply)
#
#     return None
#
#
# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=8080)
