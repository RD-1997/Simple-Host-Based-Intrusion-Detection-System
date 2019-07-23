from flask import Flask, render_template
import db

# defining the flask app
app = Flask(__name__)

# initializing db connection
conn = db.connect()
cursor = conn.cursor()



@app.route("/", methods=['GET'])
def web():
    return render_template('index.html')

if __name__ == '__main__':
  #  app.run(ssl_context='adhoc')
  app.run()