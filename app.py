#Find information on these modules later...
from flask import Flask, render_template, url_for, request, redirect
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
@app.route('/', methods=['POST','GET']) #We need to add a param called methods. So that the page can accept HTTP's GET and POST Methods. We'll also need this when te webpage sends data to our 'test.db'. '/' is 'localhost/' or '127.0.0.1/' aka the home page. If set the value to “/my-page” for example, it would set the page to 127.0.0.1/my-page.

#We will now define function for the route.
def index():
    '''
        GET is used to request data from a specified resource.
        GET is one of the most common HTTP methods.
            -GET requests can be cached
            -GET requests remain in the browser history
            -GET requests can be bookmarked
            -GET requests should never be used when dealing with sensitive data
            -GET requests have length restrictions
            -GET requests is only used to request data (not modify)
        POST is used to send data to a server to create/update a resource.
            -POST requests are never cached
            -POST requests do not remain in the browser history
            -POST requests cannot be bookmarked
            -POST requests have no restrictions on data length
    '''
    if request.method == 'POST':
        task_content = request.form['content'] #The 'name' or 'id' on index.html <form> tag.
        #Create an object instant of 'Todo'.
        new_task = Todo(content=task_content) #The task that's being add from DB.

        try:
            db.session.add(new_task) #Add the Task
            db.session.commit() # Really 'commit' or do the adding the task to the 'test.db'
            return redirect('/') # Redirect page back to "index.html".
        #If it does happen to fail.
        except:
            return 'There was an issue adding your task.'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all() #This will look at 'test.db' and output what's init by the date it was created.
        return render_template('index.html',tasks=tasks) #Since this is a 'GET' our value from above 'tasks' will be rendered to render_template() method in it's 'tasks' param.

        # Let's talk about template inheritance.
        # You create one master HTML file that contains the skeleton of the format of the webpage.
        # You inheritate that format in each other pages and insert code you need in each different page. Conventionally it's named 'base.html'.

# We will work on updating a listed task.
@app.route('/update/<int:id>', methods=['GET','POST']) #Refer to code below under app.route('/delete/etc.') and app.route(..., methods) on about line 36.
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        #When updating be sure to create your update logic or Jinja Debug will appear.
        task.content = request.form['content'] #Setting DB task content record to update.html <form> input box value.

        try:
            db.session.commit() # Do commit the record change.
            return redirect('/')
        except:
            return 'There was an issue updating your task.'
    else:
        return render_template('update.html', task=task)

# We need to work on deleting from the 'test.db'
@app.route('/delete/<int:id>') #int:id identifies our primary key from Todo Class model and 'test.db', the Id.

def delete(id):
    task_to_delete = Todo.query.get_or_404(id) #Will attempt to get the task by ID, if it can't it will show a 404 page.

    try:
        db.session.delete(task_to_delete) #Set to Delete task by id.
        db.session.commit() #Actual do the deletion.
        return redirect('/')
    except:
        return "There was a problem deleting that task."
if __name__ == "__main__":
    #Just incase we run into problems set Debug to True.
    app.run(debug=True)