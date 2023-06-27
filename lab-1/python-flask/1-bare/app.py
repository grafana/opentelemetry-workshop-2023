# Configure app
import flask
app = flask.Flask(__name__)

# Handle requests to http://localhost:4321/error
@app.route('/error')
def error():
    return eval('0/0')

# Handle requests to http://localhost:4321/
@app.route('/')
def home():
    return 'ok'

# Run the app when executing this file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4321)
