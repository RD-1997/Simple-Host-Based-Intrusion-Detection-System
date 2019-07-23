from flask import Flask, render_template
import mysql.connector as mysql

# defining the flask app
app = Flask(__name__)


# initializing database connection
db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "welkom123",
    database = "implementation"
)
cursor = db.cursor()


@app.route("/", methods=['GET'])
def web():
    return render_template('index.html')

if __name__ == '__main__':
  #  app.run(ssl_context='adhoc')
  app.run()