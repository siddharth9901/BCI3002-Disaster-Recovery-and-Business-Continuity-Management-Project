# from flask import Flask, request, send_file, jsonify
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

# @app.route('/get-watermark', methods=['POST'])
# def get_watermark():  # Returns watermark image to be embeded.
#     global watermark_flag
#     watermark = watermark_generator()
#     if caption != "" and 'd' in RSA_Keys.keys():
#         sig = keys.sign_caption(
#             int(RSA_Keys['d']), int(RSA_Keys['n']), caption)
#         print(sig)
#         watermark.generator(str(sig))
#         watermark_flag = True
#         # new_flag = False
#         return send_file("watermark.jpg", mimetype='image/jpg')
#     else:
#         return ""
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
import bcrypt

app = Flask(__name__)
CORS(app)
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
                return(jsonify(res))
            hashed = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt(14))
            users.insert({'email': request.form['email'], 'password': hashed, 'first': request.form['first'],'last':request.form['last'],'company':request.form['company']})
            res={"auth":"success"}
            return(jsonify(res))
        else:
            res={"auth":"fail"}
            return(jsonify(res))

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


