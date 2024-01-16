from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('forum.db')
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def get_parent_comment(parent_id):
    db = get_db()
    parent_comment = db.execute('SELECT body FROM comments WHERE id = ?', (parent_id,)).fetchone()
    return parent_comment['body'] if parent_comment else None

@app.route('/')
def main():
    db = get_db()
    # テーブルが存在しない場合は作成
    db.execute('''
            CREATE TABLE IF NOT EXISTS threads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
            ''')
    db.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                thread_id INTEGER,
                parent_id INTEGER,
                body TEXT NOT NULL,
                FOREIGN KEY (thread_id) REFERENCES threads (id)
            )
            ''')
    db.commit()

    threads = db.execute('SELECT * FROM threads').fetchall()
    return render_template('main.html', threads=threads)

@app.route('/thread/<int:thread_id>')
def view_thread(thread_id):
    db = get_db()
    # スレッドのタイトルを取得
    thread = db.execute('SELECT * FROM threads WHERE id = ?', (thread_id,)).fetchone()
    # スレッドのコメント一覧を取得
    comments = db.execute('SELECT * FROM comments WHERE thread_id = ?', (thread_id,)).fetchall()
    return render_template('thread.html', thread=thread, comments=comments, get_parent_comment=get_parent_comment)

@app.route('/create_thread', methods=['GET', 'POST'])
def create_thread():
    db = get_db()
    if request.method == 'POST':
        thread_name = request.form['thread_name']
        db.execute("INSERT INTO threads (name) VALUES (?)", (thread_name,))
        db.commit()
        return redirect(url_for('main'))
    return render_template('create_thread.html')

@app.route('/create_comment', methods=['POST'])
def create_comment():
    db = get_db()
    thread_id = request.form.get('thread_id')
    parent_id = request.form.get('parent_id', None)  # 親コメントがない場合に備えてデフォルト値を設定
    body = request.form['body']  # 'body' パラメータを取得
    db.execute("INSERT INTO comments (thread_id, parent_id, body) VALUES (?, ?, ?)", (thread_id, parent_id, body))
    db.commit()
    return redirect(url_for('view_thread', thread_id=thread_id))

if __name__ == '__main__':
    with app.app_context():
        # スキーマの作成
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

    app.run(debug=True)
