from flask import Flask, render_template, request,url_for,session
from backend import fetch,signup_user,available,booking_db,githublogin
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)

oauth=OAuth(app)
app.config["GITHUB_CLIENT_ID"] ="8091792263012eed1798"
app.secret_key="d9167cc14359f21bd878d43cb7787c07246e23ae"
github = oauth.register (
  name = 'github',
    client_id = app.config["GITHUB_CLIENT_ID"],
    client_secret = app.secret_key,
    access_token_url = 'https://github.com/login/oauth/access_token',
    access_token_params = None,
    authorize_url = 'https://github.com/login/oauth/authorize',
    authorize_params = None,
    api_base_url = 'https://api.github.com/',
    client_kwargs = {'scope': 'user:email'},
)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session['username']=username
        value=fetch(username,password)
        if value==True:
            return render_template("welcome.html", name=username)
        else:
            return render_template("signup.html")      
    return render_template('login.html')



# Github login route
@app.route('/login/github')
def github_login():
    github = oauth.create_client('github')
    redirect_uri = url_for('github_authorize', _external=True)
    return github.authorize_redirect(redirect_uri)


# Github authorize route
@app.route('/login/github/authorize')
def github_authorize():
    github = oauth.create_client('github')
    token = github.authorize_access_token()
    resp = github.get('user').json()
    print(f"\n{resp}\n")
    session['username']=resp['login']
    name=resp['login']
    value=githublogin(name)
    if value==True:
        return render_template("welcome.html", name=resp['login'])
    return render_template('welcome.html', name=resp['login'])

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        value=signup_user(username,password)
        if value==True:
            return render_template("welcome.html", name=username)
        else:
            return "Signup unsuccessful!"
    return render_template('signup.html')
   
@app.route('/availability')
def availability():
    rooms = available()
    return render_template('availability.html',rooms=rooms)

@app.route('/booking',methods=['GET', 'POST'])
def booking():
    rooms=available()
    return render_template('booking_form.html',rooms=rooms)

@app.route('/book', methods=['GET', 'POST'])
def book_room():
    uname=session.get('username')
    if request.method == 'POST':
        room_id = int(request.form['room_id'])
        num_people = int(request.form['num_people'])
        num_days = int(request.form['num_days'])
        rooms=available()
        value=booking_db(uname,room_id,num_people,num_days)
        if (value!=False):
            return render_template('booking_confirmation.html', room_id=room_id, num_people=num_people, num_days=num_days,price=(value*num_days))
        else:
            return render_template('login.html')

    return render_template('booking_form.html',rooms=rooms)

if __name__ == '__main__':
    app.run(debug=True)
