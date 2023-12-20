from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("html/main.html")

@app.route("/build")
def build():
    return render_template("html/build.html")

@app.route("/threads")
def threads():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    # 最新のスレッドタイトルを取得
    c.execute("SELECT title FROM threads ORDER BY rowid DESC LIMIT 1")
    thread_title = c.fetchone()

    conn.close()

    # テンプレートにタイトルを渡す
    return render_template("html/threads.html", thread_title=thread_title[0] if thread_title else "")


#/submitはGPTに吐かせてるのであまり信用しないでください
@app.route('/submit', methods=['POST'])
def submit():
    text = request.form['thread_title']

    # データベースに接続
    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    # # テーブルが存在しない場合は作成
    # c.execute('''CREATE TABLE IF NOT EXISTS threads (title TEXT)''')

    # データをテーブルに挿入
    c.execute("INSERT INTO threads (title) VALUES (?)", (text,))
    c.execute("INSERT INTO threads (title) VALUES (?)", (text,))

    # 変更をコミットし、接続を閉じる
    conn.commit()
    conn.close()
    return redirect(url_for('thread'))


if __name__ == '__main__':
    app.run(debug=True)
