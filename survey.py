from flask import Flask, render_template, request, redirect, flash
from mysqlconnection import connectToMySQL
app = Flask(__name__)
app.secret_key = 'ayoooooooo'

@app.route('/')
def index():
    return render_template("index.html")
#---------------------------------------------------------------

@app.route("/users/<id>")
def read_user(id):
    mysql = connectToMySQL('survey_validation')
    query = 'SELECT * FROM users WHERE ID =' + id
    user = mysql.query_db(query)
    return render_template("show.html", new_user = user)

@app.route('/process', methods=['POST'])
def process():
    print(request.form)
    is_valid = True
    if len(request.form['name']) < 2:
        is_valid = False
        flash("Please enter your full name", "name")
    if  "location" not in request.form: 
        is_valid = False
        flash("Please pick a location", "locationflash")
    if "language" not in request.form:
        is_valid = False
        flash("Please pick atleast one language", "languageflash")
    if len(request.form['comment']) > 120:
        is_valid = False
        flash("Please enter a comment that's less than 120 characters ", "comment")
    if not is_valid:
        return redirect("/")
    else:
        mysql= connectToMySQL('Survey_validation')
        query = "INSERT INTO Survey_validation.users (name, location, language, comment, created_at, updated_at) VALUES (%(fn)s, %(lo)s,%(ln)s,%(cm)s, NOW(), NOW());"

    data = {
        "fn": request.form["name"],
        "lo": request.form["location"],
        "ln": request.form["language"],
        "cm": request.form["comment"]
    }
    flash("Friend successfully added!")
    id = mysql.query_db(query, data)
    return redirect("/users/" + str(id))
        # eventually we may have a different success route
if __name__=="__main__":
    app.run(debug=True)
    

    # name_from_form = request.form['name']
    # location_from_form = request.form['location']
    # language_from_form = request.form.getlist('language')
    # comment_from_form = request.form['comment']
