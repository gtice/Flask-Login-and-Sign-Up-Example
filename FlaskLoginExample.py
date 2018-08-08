"""
Basic login page Flask app.
Note that this version of the code is not even remotely secure - please DON'T plug in
real usernames and passwords! We'll make a secure version of this webpage in lesson
3.2.
Based on a tutorial from realpython.com:
    https://realpython.com/blog/python/introduction-to-flask-part-2-creating-a-login-page/
"""
__author__ = "Charlie Friend"


from flask import Flask, render_template, request, redirect
#from flask_socketio import SocketIO
import hashlib

app = Flask(__name__)

USERNAME = 'admin'
PASSWORD = 'nimda'

#usernames = ['ginny', 'admin', 'cat']
#hi, nimda, dog
#passwords = ['8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4', '37bd45d638c2d11c49c641d2e9c4f49f406caf3ee282743e0c800aa1ed68e2ee', 'cd6357efdd966de8c0cb2f876cc89ec74ce35f0968e11743987084bd42fb8944']
usernames = []
passwords = []
chats = []



@app.route("/home")
def home():
    user_id = request.cookies.get('userID')
    print(user_id)
    user_password = request.cookies.get('user_pword')
    print(user_password)
    if user_id == None or user_password == None:
        return "You must log in to view this page"
    else:
        myChat = "hello\ncat\ndog"
        myOtherChat=['pig','cat','dog']
        return render_template("hello.html", chat=myOtherChat)



@app.route("/chat", methods=["GET", "POST"])
def chat():
    error = None
    user_id = request.cookies.get('userID')
    print(user_id)
    if user_id == None:
        return "Please log in to view this page"
    # If we are POSTing to the /login route, then check the credentials!
    if request.method == "POST":
        requested_message = request.form['message']
        chats.append(user_id + " : " + requested_message)
        #print("user " + requested_message)
        return render_template("chat.html", chat=chats)


    return render_template("chat.html", chat=chats)




@app.route("/", methods=["GET", "POST"])
def login():
    error = None

    # If we are POSTing to the /login route, then check the credentials!
    if request.method == "POST":
        requested_username = request.form['username']
        requested_password = request.form['password']
        print("user " + requested_username)

        password_bin = requested_password.encode()
        password_hash = hashlib.sha256(password_bin).hexdigest()

        for i in range(0,len(usernames)):
            print("i: " + str(i) + " " + usernames[i])
            if requested_username == usernames[i]:
                print("username is equal")
            if requested_password == passwords[i]:
                print("password is equal")

            if requested_username == usernames[i] and password_hash == passwords[i]:
                print("Logged in!")
                response = redirect("/home")
                response.set_cookie('userID', requested_username)
                response.set_cookie('user_pword', requested_password)
                return response

            else:
                error = "Incorrect username or password! Please try again!"
                print("Login failed!")

        error = "Incorrect username or password! Please try again!"
        print("Login failed!")
    return render_template('login.html', error=error)




@app.route("/signup", methods=["GET", "POST"])
def signup():
    error = None

    # If we are POSTing to the /login route, then check the credentials!
    if request.method == "POST":
        requested_username = request.form['username']
        requested_password = request.form['password']

        password_bin = requested_password.encode()
        password_hash = hashlib.sha256(password_bin).hexdigest()

        # Write the username to a file
        with open("all_usernames.txt", "a") as outfile:
            outfile.write(requested_username)
            outfile.write("\n")
            usernames.append(requested_username)

        # Write the password hash to a file
        with open("all_passwords.txt", "a") as outfile:
            outfile.write(password_hash)
            outfile.write("\n")
            passwords.append(password_hash)

        return redirect("/")

    return render_template('signup.html', error=error)






if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=5000)
    #read in file, and store usernames and passwords in the usernames and passwords lists
    # Read the password from the password hasher program
    try:
        with open("all_usernames.txt", "r") as infile:
            for line in infile:
                line = line.rstrip('\n')
                usernames.append(line)
    except:
        print("no username file created yet ")

    try:
        with open("all_passwords.txt", "r") as infile:
            for line in infile:
                line = line.rstrip('\n')
                print(line)
                print("end of line")
                passwords.append(line)
    except:
        print("no passwords file created yet")

    app.run(host='0.0.0.0', ssl_context=("mypublickey.pem", "myprivatekey.pk"))