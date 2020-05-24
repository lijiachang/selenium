from flask import Flask
from flask import request
from flask import Response
from flask_request_params import bind_request_params
import json

app = Flask(__name__)
app.before_request(bind_request_params)


@app.route("/", methods=["GET"])
def hello_world():
    # text = request.args.get("txt")
    text = request.params["json"]
    action = request.params["action"]
    res = {"res": text}

    print text, action

    # return "my first Flask demo! \n{}".format(text)
    return Response(json.dumps(res))


if __name__ == "__main__":
    app.run(debug=True)
