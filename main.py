from flask import Flask
from email_service import start_email_service

start_email_service()

app = Flask('app')

@app.route('/')
def hello_world():
  return 'Hello, World!'

app.run(host='0.0.0.0', port=8080)
