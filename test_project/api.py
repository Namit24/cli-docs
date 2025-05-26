from flask import Flask

app = Flask(__name__)

class ApiServer:
    def handle_request(self):
        return "OK"