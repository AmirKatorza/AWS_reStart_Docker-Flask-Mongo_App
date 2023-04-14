from flask import Flask, Response, json
from MongoDBAPI import *
app = Flask(__name__)


@app.route('/')
def base():
    return Response(response=json.dumps({"Status": "UP"}),
                    status=200,
                    mimetype='application/json')

@app.route()


if __name__ == "__main__":
    app.run(debug=True, port=5001, host='0.0.0.0')
