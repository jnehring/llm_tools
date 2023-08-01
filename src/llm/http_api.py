import logging
import json
import traceback

from datetime import datetime

from flask import Flask, jsonify
from flask import request, render_template
from flask_cors import CORS, cross_origin

def log_query(data):
    f = open("querylog.txt", "a")
    d = datetime.now().isoformat()
    f.write(d + " " + str(data) + "\n")
    f.close()

def start_api(llm, args):

    app = Flask(__name__)

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.route("/api/generate", methods=['POST'])
    @cross_origin()

    def generate():
        try:
            data = request.json
            
            #logging.info("Receive request for /api/generate with data=" + str(data))

            assert type(data) == dict
            assert "doc" in data.keys()
            assert type(data["doc"]) == str

            response = llm.generate_response(data["doc"], request.args)

            response = {
                "input_doc": data["doc"],
                "response": response
            }

            logging.info("Received answer: " + json.dumps(response))

            if args.log_all_queries:
                log_query(json.dumps(response))

            return jsonify(response)
        except Exception as e:
            e = traceback.format_exc(limit=None, chain=True)
            msg = "Exception from /api/generate\n"
            msg += traceback.format_exc(limit=None, chain=True) + "\n"
            msg += json.dumps(data, indent=4)
            msg += "----------------"
            logging.error(msg)

            response = {
                "status": "error",
                "exception": traceback.format_exc(limit=None, chain=True),
            }
            return jsonify(response), 500
    
    @app.route("/api/cond_log_prob", methods=['POST'])
    @cross_origin()
    def cond_log_prob():
        try:
            data = request.json
            #logging.info("Receive request for /api/cond_log_prob with data=" + str(data))

            assert type(data) == dict
            assert "doc" in data.keys()
            assert "targets" in data.keys()
            assert type(data["doc"]) == str

            if type(data["targets"]) == str:
                data["targets"] = [data["targets"]]

            assert type(data["targets"]) == list
            for x in data["targets"]:
                assert type(x) == str

            response = llm.cond_log_prob(data["doc"], data["targets"])

            response = {
                "input_doc": data["doc"],
                "targets": data["targets"],
                "cond_log_prob": response
            }

            if args.log_all_queries:
                log_query(json.dumps(response))

            return jsonify(response)

        except Exception as e:
            e = traceback.format_exc(limit=None, chain=True)
            msg = "Exception from /api/generate\n"
            msg += traceback.format_exc(limit=None, chain=True) + "\n"
            msg += json.dumps(data, indent=4)
            msg += "----------------"
            logging.error(msg)

            response = {
                "status": "error",
                "exception": traceback.format_exc(limit=None, chain=True),
            }
            return jsonify(response), 500
        
    @app.route("/api/single_cond_log_prob", methods=['POST'])
    @cross_origin()
    def single_cond_log_prob():
        try:
            data = request.json
            logging.info("Receive request for /api/single_cond_log_prob with data=" + str(data))

            assert type(data) == dict
            assert "doc" in data.keys()
            assert "targets" in data.keys()
            assert type(data["doc"]) == str
            assert type(data["targets"]) == str

            response = llm.single_cond_log_prob(data["doc"], data["targets"], request.args)

            response = {
                "input_doc": data["doc"],
                "single_cond_log_prob": response
            }

            logging.info("Received single conditional log probabilities: " + json.dumps(response))
            return jsonify(response)

        except Exception as e:
            e = traceback.format_exc(limit=None, chain=True)
            msg = "Exception from /api/single_cond_log_prob\n"
            msg += traceback.format_exc(limit=None, chain=True) + "\n"
            msg += json.dumps(data, indent=4)
            msg += "----------------"
            logging.error(msg)

            response = {
                "status": "error",
                "exception": traceback.format_exc(limit=None, chain=True),
            }
            return jsonify(response), 500

    @app.route("/", methods=['GET'])
    def index():
        return render_template("index.html")

    app.run(debug=True, host="0.0.0.0", port=args.port, use_reloader=False)
