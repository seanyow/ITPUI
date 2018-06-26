from flask import Flask, render_template
from flask_mysqldb import MySQL
from python import fitting_master as fm
import json

app = Flask(__name__)


mysql = MySQL()
# MySQL configurations
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'database'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3307
mysql.init_app(app)

@app.route('/')
def main():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM testtable")
    rv = cur.fetchall()
##    print str(rv)
    return render_template('index.html')

@app.route("/Graph/", methods=['POST'])
def generateGraph():
    cur = mysql.connection.cursor()
    field1 = "Speed Made Good (Kts)"
    field2 = "Wind Force"
    cur.execute("SELECT `"+ field1 + "`, `"+ field2 + "` FROM vomsii_data WHERE `"+ field1 + "` IS NOT NULL and `"+ field2 + "` IS NOT NULL and `" + field1 + "` != 'nan' and `" + field2 + "` != 'nan'")
    result_set = list(cur.fetchall())
    xdata = []
    ydata = []

    for item in result_set:
        xdata.append(item[0])
        ydata.append(item[1])

    cur.close()

##    cur = mysql.connection.cursor()
##    cur.execute("SELECT `"+ field2 + "` FROM vomsii_data WHERE `"+ field2 + "` IS NOT NULL and `"+ field2 + "` != 'nan'")
##    result_setY = list(cur.fetchall())
##    for item in result_setY:
##        ydata.append(item[0])
##
##    cur.close()
    print len(xdata), len(ydata)
    graphDiv = fm.generateGraphTest(graphMode=2, xData=xdata, yData=ydata)
    return render_template('testGraph.html', div_placeholder=graphDiv);

@app.route("/Test/")
def getColumns():
        cur = mysql.connection.cursor()
        cur.execute("select column_name from information_schema.columns where table_name ='vomsii_data'")
        rv = cur.fetchall()
        # Converting all data from unicode to ascii
        cleanRV = [[s.encode('ascii') for s in columnList] for columnList in rv]
        # Initialize a dictionary to convert the returned data as lists does not work with flask
        colDict = {}
        for item in cleanRV:
            colDict[item[0]] = item[0]
        #passing result to dataColumns as a json string
        return render_template('test.html', dataColumns=json.dumps(colDict))

if __name__ == '__main__':
    app.run(debug=True)
