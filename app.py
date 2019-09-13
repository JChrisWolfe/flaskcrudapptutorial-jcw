#Find information on these modules later...
from flask import Flask, render_template, url_for
# Also find info on these modules.
from flask_sqlalchemy import SQLAlchemy
# Get system date time.
from datetime import datetime

#Next setup the application
app = Flask(__name__) #Reference this file
# We are going to tell our app where our Database is located.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #'///' is a relative path, '////' is an absolute path. We'll eventually create a DB called 'test'.
# You have to then initialize DB. 
db = SQLAlchemy(app)
# Create a model for DB.
class Todo(db.Model):
    #Set columns
    # Our primary key
    id = db.Column(db.Integer, primary_key=True)
    # Our content column
    content = db.Column(db.String, nullable=False) # We don't want content to be empty so nullable is false.
    completed = db.Column(db.Integer, default=0) # For bookkeeping purpose, don't really need or use it.
    date_created = db.Column(db.DateTime, default=datetime.utcnow) # Will set the current time created itself automatically.

    # Now to add a function that will return a string everytime we create a new element.

    def __repr__(self):
        # Everytime we make a new element this code will return the Task and the id of the Task that's just been created.
        return '<Task %r>' % self.id

    # Go to your terminal and use python3 interpriter by using 'python3' then ENTER.
    #Type 'from app import db' to import your app's database blueprint (model). Then type 'db.create_all()' to actually create the database.


#Next we need to create an index route.
# That way we do not hit 404 page when typing URL.
@app.route('/')
#We will now define function for the route.
def index():
    return render_template('index.html')
    # Let's talk about template inheritance.
    # You create one master HTML file that contains the skeleton of the format of the webpage.
    # You inheritate that format in each other pages and insert code you need in each different page. Conventionally it's named 'base.html'.

if __name__ == "__main__":
    #Just incase we run into problems set Debug to True.
    app.run(debug=True)