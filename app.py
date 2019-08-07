from flask import Flask, render_template
import db
import pandas as pd
import matplotlib.pyplot as plt

# defining the flask app
app = Flask(__name__)

# initializing db connection
conn = db.connect()
cursor = conn.cursor()

# retrieving all the values from the database
query = "SELECT * FROM files"
cursor.execute(query)

# storing the values in a dataframe so it can easily used for visualization
df = pd.DataFrame(cursor.fetchall())
df.columns = cursor.column_names

##################################### START INFORMATION TILES #####################################

authcount = 0
for k, v in df.iterrows():
    if v[3] == "AUTHENTIC":
        authcount += 1

# counting the total files for visualization purposes
totalfiles = df.shape[0]

# creating percentage of altered files
authPerc = (authcount / totalfiles) * 100
authPerc = round(authPerc, 2)

##################################### END INFORMATION TILES #####################################

##################################### START PIE CHART #####################################

pieFrame = pd.DataFrame()
pieFrame = df[['authenticity']]
pieFrame['num'] = 1
pieFrame = pieFrame.groupby('authenticity', as_index=False).agg(sum)

plt.pie(
    pieFrame['num'],
    labels=pieFrame['authenticity'],
    shadow=True,
    startangle=90,
    autopct='%1.1f%%',
)

plt.axis('equal')
plt.title('Overall file authenticity')
plt.savefig('static/images/piechart.png', bbox_inches='tight')
plt.show()

##################################### END PIE CHART #####################################


##################################### START TABLE FILES WITH NO SCAN ########################

queryScan = "select * from files WHERE lastscan <= curdate() - interval 1 day;"
cursor.execute(queryScan)

# storing the values in a dataframe so it can easily used for visualization
dfScan = pd.DataFrame(cursor.fetchall())
dfScan.columns = cursor.column_names

##################################### END TABLE FILES WITH NO SCAN #########################


##################################### START BAR CHART #####################################

df['num'] = 1
df['lastscan'] = [d.date() for d in df['lastscan']]

Lawldf = pd.DataFrame()
Lawldf = df[['lastscan', 'num']]

Lawldf = Lawldf.groupby('lastscan', as_index=False).agg(sum)

print(Lawldf)
dateScan = Lawldf['lastscan']
files = Lawldf['num']

plt.bar(dateScan, files, 1)
axes = plt.gca()
plt.xticks(rotation=90)
plt.yticks(fontsize='8')
plt.ylabel("date")
plt.xlabel("Files")
plt.title("Total new files per day")

# saving the bar chart
plt.savefig('static/images/ipchart.png', bbox_inches='tight')
plt.show()

##################################### END BAR CHART #####################################


# starting web app
@app.route("/", methods=['GET'])
def web():
    return render_template('index.html', data=df, perc=authPerc, total=totalfiles, scandata=dfScan)

if __name__ == '__main__':
  #  app.run(ssl_context='adhoc')
  app.run()