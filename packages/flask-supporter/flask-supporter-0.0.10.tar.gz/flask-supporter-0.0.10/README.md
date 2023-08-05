# flask-supporter

Supported APIs
<pre>
from flask import Flask
import flask_supporter

app = Flask(__name__)

@app.route('/')
def index():
    return '''
index
    '''

'''
#https://dashboard.ngrok.com/get-started/setup
!pip install pyngrok
!pip install flask-ngrok
!pip install flask-supporter
!ngrok authtoken YOUR_AUTH_TOKEN
'''
flask_supporter.utils.run_with_ngrok(app)
app.run()
</pre>
