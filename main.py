from flask import Flask, render_template, url_for, request, flash, redirect
from init_db import get_connection


app = Flask(__name__)
app.config['SECRET_KEY'] = '1111'
DATABASE_NAME ='flaskdb'



def get_post(post_id): #add new post
    with get_connection(DATABASE_NAME) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"""SELECT id, title, content, auther, created FROM posts WHERE id = {post_id}""")
            post = cursor.fetchone()

    return {
        'id': post[0],
        'title': post[1],
        'content': post[2],
        'auther': post[3],
        'created': post[4]
    }

@app.route('/')
def index(): #connected with our data base
    with get_connection(DATABASE_NAME) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT id, title, content, auther, created FROM posts""")
            posts = cursor.fetchall()


    posts_data = list()
    for post in posts:
        posts_data.append(
            {
                'id': post[0],
                'title': post[1],
                'content': post[2],
                'auther': post[3],
                'created': post[4]
            }
        )
    return render_template('index.html', posts=posts_data)


@app.route('/posts/<int:post_id>')
def post(post_id): #add post
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route('/create-post', methods=['GET', 'POST'])
def create(): #creat post
    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        auther = request.form['auther']

        if not title or not content or not auther:
            flash('Title, content and auther are required')
        else:
            with get_connection(DATABASE_NAME) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(f"""
                    INSERT INTO posts(title, content, auther)
                    VALUES('{title}', '{content}', '{auther}')
                """)
                conn.commit()
            return redirect(url_for('index'))
    return render_template('create.html', post=post)

@app.route('/<int:post_id>/edit', methods=['GET', 'POST'])
def edit(post_id): #edit post that we made
    post = get_post(post_id)
    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        auther = request.form['auther']

        if not title or not content or not auther:
            flash('Title, content and auther are required')
        else:
            with get_connection(DATABASE_NAME) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(f"""
                    UPDATE posts 
                    SET title = '{title}',
                    auther = '{auther}',
                    content = '{content}'
                    WHERE id = {post_id}
                """)
                conn.commit()
            return redirect(url_for('index'))
    return render_template('edit.html', post=post)


@app.route('/<int:post_id>/delete', methods=['POST', ])
def delete(post_id):
    with get_connection(DATABASE_NAME) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"""DELETE FROM posts WHERE id = {post_id}""")
            conn.commit()
    return redirect(url_for('index'))

app.run(debug=True)