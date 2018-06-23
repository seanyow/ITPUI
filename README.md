Important Notes:

Install this version as the latest does not work.
pip install mysqlclient==1.3.9 

Change your database port accordingly - default is 3306

One cursor can only load 1 SQL Statement. Needs to use .close() to reuse
Alternatively can search on executeMany()

For AngularJS expressions, use {% raw %} and {% endraw %} due to AngularJS and Jinja clashes. Example in templates/index.html

To display graph, do not use {% raw %}. Instead use {{ variableName|safe }}. Example in templates/testGraph.html

Useful Links:
https://realpython.com/flask-by-example-updating-the-ui/

https://code.tutsplus.com/tutorials/creating-a-web-app-from-scratch-using-python-flask-and-mysql--cms-22972

