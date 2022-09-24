from flask import Flask, redirect, url_for, render_template


app = Flask(__name__)
lst = ['Narm', 'Ebar', 'Gahnstemme']
@app.route('/')
def home():
    return render_template('index.html')





@app.route("/<name>/") # can pass a string from URL as an argument through <name>. this name is then used in this function
def user(name):
    return render_template(
    'index.html',
     content=lst,
     )
@app.route('/admin/')
def admin():
    return redirect(url_for('user', name= 'Admin!')) # redirect to user function and provides an argument for 'name' parameter

if __name__ =='__main__':
    app.run()

