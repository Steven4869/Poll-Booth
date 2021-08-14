from flask import Flask,render_template,request,redirect,session,jsonify
import mysql.connector
import os
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    port='3306',
    database='pythonlogin'
)
cursor = conn.cursor()
app = Flask(__name__)
app.secret_key=os.urandom(24)

@app.route('/')
def home():
    return render_template('login.html')
@app.route('/register')
def register():
    return render_template('register.html')
@app.route('/home')
def dashboard():
    if 'user_id' in session:
        return render_template('index.html')
    else:
        return redirect('/')
@app.route('/add_team', methods=['POST'])
def add_team():
    team_name = request.form.get('team_name')
    members_poll = request.form.get('members')
    description = request.form.get('description')
    cursor.execute("""INSERT INTO `post` (`team_name`, `members`, `description`) VALUES ('{}','{}','{}')""".format(team_name, members_poll, description))
    conn.commit()
    return redirect('/home')

@app.route('/add_user',methods=['POST'])
def add_user():
    name= request.form.get('name')
    username = request.form.get('username')
    password = request.form.get('password')
    cursor.execute("""INSERT INTO `accounts` (`name`,`username`,`password`) VALUES ('{}','{}','{}')""".format(name,username,password))
    conn.commit()
    return "User registered successfully"
@app.route('/add_poll', methods=['POST'])
def add_poll():
    title = request.form.get('title')
    cursor.execute("""INSERT INTO `polls` (`title`) VALUES ('{}')""".format(title))
    conn.commit()
    return redirect('/home')

@app.route('/create_poll')
def create_poll():
    return render_template('create_poll.html')
@app.route('/login_validation', methods=['POST'])
def login_validation():
    username = request.form.get('username')
    password = request.form.get('password')
    cursor.execute("""SELECT * FROM `accounts` WHERE `username` LIKE '{}' AND `password` LIKE '{}'""".format(username,password))
    users = cursor.fetchall()
    if len(users)>0:
        session['user_id'] = users[0][0]
        return redirect('/home')
    else:
        return redirect('/')
@app.route('/polldata',methods=['GET','POST'])
def polldata():
    cursor.execute("""SELECT * FROM polls""")
    pollframe = cursor.fetchall()
    frameworkArray =[]
    for row in pollframe:
        frameworkObj = {
            'id': row["id"],
            'name': row["title"]
        }
        frameworkArray.append(frameworkObj)
        return jsonify({'htmlresponse': render_template('response.html', frameworklist =frameworkArray)})
@app.route('/poll')
def poll():
    cursor.execute("""SELECT * FROM polls""")
    framework = cursor.fetchall()
    return render_template('poll.html', framework= framework)
@app.route('/team')
def team():
    cursor.execute("""SELECT * FROM post""")
    teams = cursor.fetchall()
    return render_template('team.html', teams=teams)
@app.route('/create_teams')
def create_teams():
    return render_template('create_teams.html')
@app.route("/insert",methods=["POST","GET"])
def insert():
    if request.method == 'POST':
        # poll_option = request.form.get('poll_option')
        # print(poll_option)
        # cursor.execute("""INSERT INTO `poll_result`(`data`) VALUES ('{}') """.format(poll_option))
        # conn.commit()
        # conn.close()
        # msg = 'success'
        if 'submit_button' in request.form:
            user_answer = request.form["poll_option"]
            return user_answer
    # return jsonify(msg)
@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')
@app.route('/members')
def members():
    cursor.execute("""SELECT name FROM accounts """)
    data = cursor.fetchall()
    return render_template('members.html',data=data)
if __name__ == "__main__":
    app.run(debug=True)
