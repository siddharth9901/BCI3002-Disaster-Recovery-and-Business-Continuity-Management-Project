from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta
import time
import string
import random
import hashlib

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
            secret=''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase+
                             string.digits, k=128))
            users.insert_one({'email': request.form['email'], 'password': bcrypt.generate_password_hash(request.form['password']), 'first': request.form['first'],'last':request.form['last'],'company':request.form['company'],'secret':secret})
            res={"auth":"success","secret":secret}
            return jsonify(res)
        else:
            res={"auth":"fail"}
            return jsonify(res)

@app.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        print(request.form)
        users = mongo.db.users
        signin_user = users.find_one({'email': request.form['email']})
        if signin_user:
            print(signin_user['password'])
            if bcrypt.check_password_hash(signin_user['password'],request.form['password']):
                print("success")
                secret=signin_user['secret']
                #print(len(secret))
                matrix=list()
                temp=list(secret)
                #print(temp)
                row=list()
                for i in range(0,len(temp),2):
                    temp2=secret[i]+secret[i+1]
                    #print(temp2)
                    row.append(temp2)
                    if(len(row)==8):
                        matrix.append(row)
                        row=[]
                        #print(matrix)
                #print(matrix)
                otps = list()
                #print(time.time())
                #print(int(time.time()) //10000)
                for i in range((int(time.time())//100)-1,(int(time.time())//100)+2):
                    otp=i
                    row=(otp//3)%8
                    column=(otp//5)%8
                    otp=matrix[row][column]+str(otp)
                    #print(otp)
                    otp=int(hashlib.sha512(otp.strip().encode('utf-8')).hexdigest(), 16)%1000000
                    #print(otp)
                    otps.append(otp)
                print(otps)
                print(request.form['otp'],otps[1])
                if int(request.form['otp']) in otps:
                    token = jwt.encode({
                        'email': signin_user['email'],
                        'exp': datetime.utcnow() + timedelta(minutes=60)
                    }, app.config['SECRET_KEY'])
                    res = {"auth": "success","token":token.decode('UTF-8')}
                    return jsonify(res)
                else:
                    print("fail3")
                    res = {"auth": "fail"}
                    return jsonify(res)
                # return '''<script> console.log('script')</script>'''
            else:
                print("fail1")
                res = {"auth": "fail"}
                return jsonify(res)
        else:
            print("fail2")
            res={"auth":"fail"}
            return jsonify(res)


@app.route("/", methods=['POST', 'GET'])
def index():
    return "Welcome from Flask"

if __name__ == "__main__":
    app.run(debug=True)
    app.run()


