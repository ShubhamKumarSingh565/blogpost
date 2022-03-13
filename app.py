# from crypt import methods
from datetime import datetime
from email.policy import default
from turtle import title
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String[100], nullable=False)   # nullable=False means can't leave it 
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String[20], nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    def __repr__(self) :
        return 'Blog post ' + str(self.id)



all_posts = [
    {
        'title': 'Post 1',
        'content': 'This is the content of post 1. Ukrene-Russia conflict.',
        'author': 'E Balagurusamy'
    },
    {
        'title': 'Post 2',
        'content': 'This is the content of post 2. India-Chaina conflict.'
    }
]

@app.route('/')
def hello_world():
    return render_template('index.html')



@app.route('/posts', methods=['GET', 'POST'])  # got a forum to get data and post it
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)   # add new post into database
        db.session.commit()      # save data into database permanently
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('posts.html', posts=all_posts)    # posts is a variable and all_posts is a data



@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)      # here post means to get the post having id
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')



@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id)      # here post means to get the post having id
    if request.method == "POST":
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)


@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    if request.method == "POST":
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new_post.html')


if __name__ == "__main__":
    app.run(debug=True)

