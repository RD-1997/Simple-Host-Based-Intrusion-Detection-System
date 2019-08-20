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

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


##################################### START INFORMATION TILES #####################################

authcount = 0
for k, v in df.iterrows():
    if v[6] == "unchanged":
        authcount += 1

# counting the total files for visualization purposes
totalfiles = df.shape[0]

# creating percentage of altered files
authPerc = (authcount / totalfiles) * 100
authPerc = round(authPerc, 2)

##################################### END INFORMATION TILES #####################################

##################################### START PIE CHART #####################################

pieFrame = pd.DataFrame()
pieFrame = df[['state']]
pieFrame['num'] = 1
pieFrame = pieFrame.groupby('state', as_index=False).agg(sum)

plt.pie(
    pieFrame['num'],
    labels=pieFrame['state'],
    shadow=True,
    startangle=90,
    autopct='%1.1f%%',
)

plt.axis('equal')
plt.title('Overall file state')
plt.savefig('static/images/piechart.png', bbox_inches='tight')
plt.show()

##################################### END PIE CHART #####################################
print("hello world")

##################################### START TABLE FILES WITH NO SCAN ########################

queryScan = "select * from files WHERE last_scan <= curdate() - interval 1 day;"
cursor.execute(queryScan)

# storing the values in a dataframe so it can easily used for visualization
dfScan = pd.DataFrame(cursor.fetchall())
dfScan.columns = cursor.column_names

##################################### END TABLE FILES WITH NO SCAN #########################


##################################### START BAR CHART #####################################

df['num'] = 1
df['last_scan'] = [d.date() for d in df['last_scan']]

Lawldf = pd.DataFrame()
Lawldf = df[['last_scan', 'num']]

Lawldf = Lawldf.groupby('last_scan', as_index=False).agg(sum)

dateScan = Lawldf['last_scan']
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