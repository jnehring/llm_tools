import logging

from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin

def start_api(llm, args):

    app = Flask(__name__)

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.route("/api/generate", methods=['POST'])
    @cross_origin()
    def generate():
        data = request.json
        logging.info("Receive request with data=" + str(data))
        response = llm.generate_response(input_str=data["doc"])
        logging.info("Received answer: " + response)
        return response

    app.run()
