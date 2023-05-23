import logging
import json

from flask import Flask
from flask import request, render_template
from flask_cors import CORS, cross_origin


def start_api(llm, args):

    app = Flask(__name__)

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.route("/api/generate", methods=['POST'])
    @cross_origin()
    def generate():
        data = request.json
        print(data)
        logging.info("Receive request with data=" + str(data))
        response = llm.generate_response(input_str=data["doc"])

        response = {
            "input_doc": data["doc"],
            "response": response
        }

        logging.info("Received answer: " + json.dumps(response))
        return json.dumps(response, indent=4)
    
    @app.route("/", methods=['GET'])
    def index():
        return render_template("index.html")

    app.run(debug=True)
