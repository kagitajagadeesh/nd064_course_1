import sqlite3, sys

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
import logging

# Function to get a database connection.
# This function connects to database with the name `database.db`
connectionsCount = 0
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    global connectionsCount
    connectionsCount += 1
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

@app.route('/healthz')
def healthCheck():
    response = app.response_class(
        response = json.dumps({"result": "OK-healthy"}),
        status = 200,
        mimetype = 'application/json'
    )
    return response

@app.route('/metrics')
def metrics():
    connection = get_db_connection()
    posts = connection.execute('SELECT count(*) FROM posts').fetchone()
    connection.close()

    response = app.response_class(
        response = json.dumps({
            "db_connection_count": connectionsCount,
            "post_count": posts[0]
        }),
        status = 200,
        mimetype = 'application/json'
    )
    app.logger.info('Metrics request successfull')
    return response

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      app.logger.info('A non-existing article is accessed')
      return render_template('404.html'), 404
    else:
      app.logger.info('Article "' + post['title'] + '" retrieved!')
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    app.logger.info('The "About Us" page is retrieved')
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()

            app.logger.info('A new article titled "' + title + '" is created' )
            return redirect(url_for('index'))

    return render_template('create.html')

# start the application on port 3111
if __name__ == "__main__":

#    logging.basicConfig(
#        #filename='app.log',
#        level=logging.DEBUG,
#        format='%(levelname)s:%(module)s:%(asctime)s %(message)s',
#        datefmt='%d/%m/%Y %H:%M:%S'
#     )
    class StdErrFilter(logging.Filter):
        def filter(self, rec):
            return rec.levelno in (logging.ERROR, logging.WARNING)

    class StdOutFilter(logging.Filter):
        def filter(self, rec):
            return rec.levelno in (logging.DEBUG, logging.INFO)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(process)s - %(asctime)s - %(name)s - %(levelname)s - %(message)s')

    h1 = logging.StreamHandler(sys.stdout)
    h1.setLevel(logging.DEBUG)
    h1.setFormatter(formatter)
    h1.addFilter(StdOutFilter())
    logger.addHandler(h1)

    h2 = logging.StreamHandler(sys.stderr)
    h2.setLevel(logging.WARNING)
    h2.setFormatter(formatter)
    h2.addFilter(StdErrFilter())
    logger.addHandler(h2)
   app.run(host='0.0.0.0', port='3111', debug=True)
