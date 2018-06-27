from flask import Flask, render_template
import json

from python import fitting_master as fm
from python import database as db
from python import dataframe as df

app = Flask(__name__)
sql = db.SQL()


# mysql = MySQL()
# # MySQL configurations
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'database'
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_PORT'] = 3307
# mysql.init_app(app)


@app.route('/')
def main():
    # cur = mysql.connection.cursor()
    # cur.execute("SELECT * FROM testtable")
    # rv = cur.fetchall()
    ##    print str(rv)
    return render_template('index.html')


@app.route("/Graph/", methods=['POST'])
def generateGraph():
    # 40: "Speed Made Good (Kts)"
    # 38: "Wind Force"

    # cur = mysql.connection.cursor()
    # field1 = "Speed Made Good (Kts)"
    # field2 = "Wind Force"
    # cur.execute(
    #     "SELECT `" + field1 + "`, `" + field2 + "` FROM vomsii_data WHERE `" + field1 + "` IS NOT NULL and `" + field2 + "` IS NOT NULL and `" + field1 + "` != 'nan' and `" + field2 + "` != 'nan'")
    #
    # result_set = list(cur.fetchall())
    # # result_set =
    # xdata = []
    # ydata = []
    #
    # for item in result_set:
    #     xdata.append(item[0])
    #     ydata.append(item[1])
    #
    # cur.close()

    ##    cur = mysql.connection.cursor()
    ##    cur.execute("SELECT `"+ field2 + "` FROM vomsii_data WHERE `"+ field2 + "` IS NOT NULL and `"+ field2 + "` != 'nan'")
    ##    result_setY = list(cur.fetchall())
    ##    for item in result_setY:
    ##        ydata.append(item[0])
    ##
    ##    cur.close()

    sql = db.SQL()

    # Use this if you want all vessels
    # vessel = None

    # Use this if you want just one vessel
    vessel = 'AJA IPSA'

    dff = sql.get_vessel(vessel=vessel)
    col_names = sql.get_column_names()

    x_axis = col_names[39]
    y_axis = col_names[37]

    result_set = dff.get_2D_data(x_axis=x_axis, y_axis=y_axis, clean=True)

    xdata = list(result_set[x_axis])
    ydata = list(result_set[y_axis])

    print len(xdata), len(ydata)
    graphDiv = fm.generateGraphTest(graphMode=2, xData=xdata, yData=ydata)
    return render_template('testGraph.html', div_placeholder=graphDiv);


@app.route("/Test/",methods=['POST','GET'])
def getColumns():
    # cur = mysql.connection.cursor()
    # cur.execute("select column_name from information_schema.columns where table_name ='vomsii_data'")
    # rv = cur.fetchall()
    # Converting all data from unicode to ascii
    # cleanRV = [[s.encode('ascii') for s in columnList] for columnList in rv]

    sql = db.SQL()
    ########replace with your database table########
    cleanRV = sql.get_column_names('test_data')

    # Initialize a dictionary to convert the returned data as lists does not work with flask
    # cursor = mysql.connection.cursor()
    # cursor.execute(
    #     "select distinct`Vessel Name` from vomsii_data where `vessel name` is not null Order by `vessel name` ASC")
    resultValue = cursor.fetchall()

    resultValue = sql.get_vessel_names('test_data')

    vnDict = {}
    for item in resultValue:
        # vnDict[item[0]] = item[0]
        vnDict[item] = item
    return render_template('test.html', dataColumns=json.dumps(cleanRV),dataColumns=json.dumps(resultValue))

if __name__ == '__main__':
    app.run(debug=True)
