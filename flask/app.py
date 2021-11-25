from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'testing'

app.config['MONGO_dbname'] = 'users'
app.config['MONGO_URI'] = "mongodb+srv://Dev:3uDBzxdCG2EEC35@cluster0.xwipk.mongodb.net/DRBCM?retryWrites=true&w=majority"
mongo = PyMongo(app)



@app.route("/signup", methods=['POST'])
def signup():
    if request.method == 'POST':
        users = mongo.db.users
        signup_user = users.find_one({'email': request.form['email']})
        if not signup_user:
            if request.form['password']!=request.form['confirmpassword']:
                print("password and confirm password do not match")
                res={"auth":"fail"}
                return jsonify(res)
            #hashed = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt(14))
            users.insert_one({'email': request.form['email'], 'password': bcrypt.generate_password_hash(request.form['password']), 'first': request.form['first'],'last':request.form['last'],'company':request.form['company']})
            res={"auth":"success"}
            return jsonify(res)
        else:
            res={"auth":"fail"}
            return jsonify(res)

@app.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        signin_user = users.find_one({'email': request.form['email']})
        if signin_user:
            print(signin_user['password'])
            if bcrypt.check_password_hash(signin_user['password'],request.form['password']):
                print("success")
                res={"auth":"success"}
                return jsonify(res)
            else:
                print("fail")
                res = {"auth": "fail"}
                return jsonify(res)
        else:
            print("fail")
            res={"auth":"fail"}
            return jsonify(res)


@app.route("/", methods=['POST', 'GET'])
def index():
    return "Welcome from Flask"

# @app.route('/signin', methods=['GET', 'POST'])
# def signin():
#     if request.method == 'POST':
#         users = mongo.db.users
#         signin_user = users.find_one({'username': request.form['username']})

#         if signin_user:
#             if bcrypt.hashpw(request.form['password'].encode('utf-8'), signin_user['password'].encode('utf-8')) == \
#                     signin_user['password'].encode('utf-8'):
#                 session['username'] = request.form['username']
#                 return redirect(url_for('index'))

#         flash('Username and password combination is wrong')
#         return render_template('signin.html')

#     return render_template('signin.html')


# @app.route('/logout')
# def logout():
#     session.pop('username', None)
#     return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
    app.run()


