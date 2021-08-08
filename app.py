from flask import Flask,redirect,request,render_template
import sqlite3
import os


app = Flask(__name__)

BASS_DIR = os.path.dirname(__file__)

@app.route('/')
def index():
    conn = sqlite3.connect(os.path.join(BASS_DIR, 'tyblog.db'))
    cursor = conn.cursor()
    sql = "select id,title from blog"
    rows = cursor.execute(sql)
    blogs = []
    for row in rows:
        blog = {}
        id = row[0]
        title = row[1]
        blog['id'] = id
        blog['title'] = title
        blogs.append(blog)

    return render_template('index.html',blogs=blogs)

@app.route('/add_blog/',methods=['GET','POST'])
def add_blog():
    if request.method == 'GET':
        return render_template('add_blog.html')
    else:
        conn = sqlite3.connect(os.path.join(BASS_DIR,'tyblog.db'))
        cursor = conn.cursor()
        title = request.form.get('title')
        content = request.form.get('content')
        sql = "insert into blog(id,title,content) values(null,'%s','%s')"%(title,content)
        cursor.execute(sql)
        conn.commit()
        conn.close()
        print(title)
        print(content)
        return redirect('/')



@app.route('/blog_detail/')
def blog_detail():
    blog_id = request.args.get('id')
    conn = sqlite3.connect(os.path.join(BASS_DIR, 'tyblog.db'))
    cursor = conn.cursor()
    sql = 'select id,title,content from blog where id =%s'%blog_id
    rows = cursor.execute(sql)
    blog = {}
    for row in rows:
        blog['id'] = row[0]
        blog['title'] = row[1]
        blog['content']= row[2]
    return render_template('blog_datail.html',blog=blog)


if __name__ == '__main__':
    app.run()
