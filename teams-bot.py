from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/get-reply", methods=['GET'])
def get_reply():
    reply = request.args.get('reply')
    print(reply)

    return 'hi z'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)