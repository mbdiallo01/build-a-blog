from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'hsskk3877f'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route("/", methods=['GET'])
def main():

    tasks = Blog.query.all()
    return render_template("blogs.html", tasks=tasks)



@app.route('/newpost', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        new_post = Blog(title, body)
        if len(title) == 0 or len(body) == 0:
            flash('Please enter information in both title and body area', 'error')

            return redirect('/newpost')
        db.session.add(new_post)
        db.session.commit()

        return redirect('/blog')

    return render_template("newpost.html")

@app.route('/blog', methods=['POST', 'GET'])
def newpost():
    
    tasks = Blog.query.all()
    return render_template('blog.html', tasks=tasks)

@app.route('/blog?id=<id>', methods=['GET'])
def blog(id):
    
    post = Blog.query.filter_by(id=int(id))
    return render_template('/blog.html', tasks=post)

@app.route('/blogs')
def blogs():
    
    return redirect('/')

if __name__ == "__main__":
    app.run()