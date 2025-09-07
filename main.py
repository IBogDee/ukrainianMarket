from flask import Flask, request, render_template, make_response, g
import sqlite3
import secrets, string


app = Flask(__name__)
DATABASE = 'market.db'

#Security Section
def Generate_Random_Cookie_Value(length=16):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(length))

@app.after_request
def Add_Security_Headers(Response):
    Response.headers.setdefault("Content-Type", "text/html; charset=utf-8")
    Response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    Response.headers["Content-Security-Policy"] = "default-src 'self'"
    Response.headers["X-Content-Type-Options"] = "nosniff"
    Response.headers["X-Frame-Options"] = "DENY"
    return Response
    

#Database Handling (Getting DB and Closing Connection) 
def Get_DB():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def Close_Connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


#Web routes
@app.route("/index")
@app.route("/home")
@app.route("/")
def index():
    randomID = Generate_Random_Cookie_Value()
    response  = make_response(render_template("index.html"))
    response.set_cookie('ukrainianMarket', 
    randomID, 
    max_age=3600,  #  hour (in seconds)
    expires=None,  
    path='/',      
    domain=None,   
    secure=True,   
    httponly=True  
    )
    return response

@app.route("/search" , methods=["GET", "POST"])
def search():
    results = []
    if request.method == "POST":
        item_name = request.form["item_name"]
        db = Get_DB()
        cursor = db.cursor()
        cursor.execute("SELECT name, price, category FROM items WHERE LOWER(name) LIKE ?", ('%' + item_name.lower() + '%',))
        results = cursor.fetchall()
    return render_template("search.html", results=results)
    ukrainianMarket = request.cookies.get('ukrainianMarket')

@app.route("/add", methods=["GET", "POST"])
def add():
    message = None
    if request.method == "POST":
        item_name = request.form["item_name"]
        price = request.form["price"]
        category = request.form["category"]

        db = Get_DB()
        cursor = db.cursor()
        cursor.execute("INSERT INTO items (name, price, category) VALUES (?, ?, ?)", (item_name, price, category))
        db.commit()
        message = "Item added successfully!"
    return render_template("add.html", message=message)
    ukrainianMarket = request.cookies.get('ukrainianMarket')

if __name__ == '__main__':
    app.run(debug=True)