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

@app.route('/')
def main():
    db = get_db()
    threads = db.execute('SELECT * FROM threads').fetchall()
    return render_template('main.html', threads=threads)

@app.route('/thread/<int:thread_id>')
def view_thread(thread_id):
    db = get_db()
    # スレッドのタイトルを取得
    thread = db.execute('SELECT * FROM threads WHERE id = ?', (thread_id,)).fetchone()
    # スレッドのコメント一覧を取得
    comments = db.execute('SELECT * FROM comments WHERE thread_id = ?', (thread_id,)).fetchall()
    return render_template('thread.html', thread=thread, comments=comments)

@app.route('/create_thread', methods=['GET', 'POST'])
def create_thread():
    db = get_db()
    if request.method == 'POST':
        thread_name = request.form['thread_name']
        db.execute("INSERT INTO threads (name) VALUES (?)", (thread_name,))
        db.commit()
        return redirect(url_for('main'))
    return render_template('create_thread.html')

if __name__ == '__main__':
    with app.app_context():
        # スキーマの作成
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

    app.run(debug=True)
