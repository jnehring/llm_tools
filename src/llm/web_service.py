from flask import Flask, render_template, request, flash
import requests
import logging

def start_service(llm, args):
    
    app = Flask(__name__)
    app.secret_key = "myllmrequest"

    @app.route("/", methods=['POST', 'GET'])
    def process():
        if request.method == 'POST':
            
            recvd_txt = request.form['multiline_txt']
            logging.info("Receive request with data=" + recvd_txt)
            
            response = llm.generate_response(recvd_txt)
            logging.info("Received answer: " + response)

            #print(response.text)
            return render_template("index.html", user_text=recvd_txt, llm_text=response)
        
        return render_template("index.html")
    
    app.run(debug=True, port=8000) 