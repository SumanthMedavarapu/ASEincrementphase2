from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer


app = Flask(__name__)

app.secret_key = 'mysecret'

app.config['MONGO_DBNAME'] = 'test'
app.config['MONGO_URI'] = 'mongodb+srv://sumanth:sumanth123@sumanth-mzjwn.mongodb.net/test?retryWrites=true&w=majority'

mongo = PyMongo(app)
english_bot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")
trainer = ChatterBotCorpusTrainer(english_bot)
#trainer.train("chatterbot.corpus.english")
trainer.train("static\my_export.json")

trainer = ListTrainer(english_bot)

#trainer.train([
 #   "How are you?",
  #  "I am good.",
   # "That is good to hear.",
   # "Thank you",
    #"You are welcome.",
#])

trainer.train([
    "Greetings!",
    "Hello",
])

#trainer.export_for_training('./my_export.json')


@app.route('/')
def index():
    if 'username' in session:
        return render_template("test4.html")
        

    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if bcrypt.checkpw(request.form['pass'].encode('utf-8'), login_user['password']):

        #if bcrypt.checkpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
        #if bcrypt.checkpw(bytes(request.form['pass'], 'utf-8'), hashpass) == hashpass:
        #if bcrypt.checkpw(pass, hashed):
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            global hashpass
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password' : hashpass,'phonenumber' : request.form['Mobile'],
            'userAddress' : request.form['Address']})              
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('register.html')
@app.route("/get")
def getBotResponse():
    userText = request.args.get('msg')
    print("hai")
    return str(english_bot.get_response(userText))

@app.route('/logout',methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    
    app.run(debug=True)
