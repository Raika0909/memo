from flask import Flask, request, render_template, redirect
import sqlite3

app = Flask(__name__, static_folder='.', static_url_path='')

tasks = []

# データベースを繋ぐ関数
def get_db():
    db = sqlite3.connect('memo.db')
    db.row_factory = sqlite3.Row
    return db

# データベースの初期化
def init_db():
    with app.app_context():
        try:
            db = get_db()
        finally:
            db.close()

init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        db = get_db()

        with db:
            tasks = db.execute('SELECT * FROM task').fetchall()
            categories = db.execute('SELECT * FROM category').fetchall()

        if request.method == 'POST':
            task = request.form['task']
            category_id = request.form['category_id']
            with db:
                db.execute('INSERT INTO task (task_name, category_id) VALUES (?, ?)', (task, category_id,))
            return redirect('/')

        return render_template('index.html', tasks=tasks, categories=categories)
    finally:
        db.close()

@app.route('/finish', methods=['POST'])
def finish():
    try:
        db = get_db()
        task_id = int(request.form['task_id'])
        with db:
            db.execute('DELETE FROM task WHERE id = ?', (task_id,))
        return redirect('/')
    finally:
        db.close()

@app.route('/edit', methods=['POST'])
def edit():
    try:
        db = get_db()
        task_id = int(request.form['task_id'])
        task = request.form['task']
        category_id = int(request.form['category_id'])
        with db:
            db.execute('UPDATE task SET task_name = ?, category_id = ? WHERE id = ?', (task, category_id, task_id,))
        return redirect('/')
    finally:
        db.close()

@app.route('/addition', methods=['POST'])
def addition():
    try:
        db = get_db()
        task_id = int(request.form['task_id'])
        addition = request.form['addition']
        with db:
            db.execute('UPDATE task SET addition = ? WHERE id = ?', (addition, task_id,))
        return redirect('/')
    finally:
        db.close()

@app.route('/edit_addition', methods=['POST'])
def edit_addition():
    try:
        db = get_db()
        task_id = int(request.form['task_id'])
        with db:
            db.execute('UPDATE task SET editing = 1 WHERE id = ?', (task_id,))
        return redirect('/')
    finally:
        db.close()

@app.route('/category/<category_id>', methods=['GET'])
def show_category(category_id):
    try:
        db = get_db()
        
        with db:
            if category_id == '6':  # カテゴリー「すべて」を表示する
                tasks = db.execute('SELECT * FROM task').fetchall()
            else:
                tasks = db.execute('SELECT * FROM task WHERE category_id = ?', (category_id,)).fetchall()
            categories = db.execute('SELECT * FROM category').fetchall()
        
        return render_template('index.html', tasks=tasks, categories=categories)
    finally:
        db.close()

@app.route('/save_addition', methods=['POST'])
def save_addition():
    try:
        db = get_db()
        task_id = int(request.form['task_id'])
        addition = request.form['addition']
        with db:
            db.execute('UPDATE task SET addition = ?, editing = 0 WHERE id = ?', (addition, task_id,))
        return redirect('/')
    finally:
        db.close()

if __name__ == '__main__':
    app.run()
