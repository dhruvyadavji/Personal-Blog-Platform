from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

# Define the database model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    publication_date = db.Column(db.Date, nullable=False)

# Create the database tables (run once)
db.create_all()

# Routes
@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@app.route('/post/<int:id>')
def view_post(id):
    post = Post.query.get_or_404(id)
    return render_template('post_detail.html', post=post)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        publication_date = request.form['publication_date']

        new_post = Post(title=title, content=content, publication_date=publication_date)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('admin.html')

@app.route('/delete/<int:id>')
def delete_post(id):
    post_to_delete = Post.query.get_or_404(id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
