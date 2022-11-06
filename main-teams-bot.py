from flask import Flask, render_template, request
import os

app = Flask(__name__)


@app.route("/get-reply", methods=['GET'])
def get_reply():
    reply = request.args.get('reply')
    print(reply)

    return 'hi z'


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)