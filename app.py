from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('library.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return render_template('index.html', books=books)

@app.route('/add', methods=('GET', 'POST'))
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        quantity = request.form['quantity']
        room = request.form['room']
        shelf = request.form['shelf']
        section = request.form['section']
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO books (title, author, isbn, quantity, room, shelf, section) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (title, author, isbn, quantity, room, shelf, section))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit_book(id):
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (id,)).fetchone()
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        quantity = request.form['quantity']
        room = request.form['room']
        shelf = request.form['shelf']
        section = request.form['section']
        conn.execute('''
            UPDATE books SET title=?, author=?, isbn=?, quantity=?, room=?, shelf=?, section=? 
            WHERE id=?
        ''', (title, author, isbn, quantity, room, shelf, section, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    conn.close()
    return render_template('edit.html', book=book)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_book(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM books WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# --- Route untuk carian segera (live search) ---
@app.route('/search')
def search():
    query = request.args.get('q', '')
    conn = get_db_connection()
    books = conn.execute("""
        SELECT * FROM books 
        WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ?
    """, (f'%{query}%', f'%{query}%', f'%{query}%')).fetchall()
    conn.close()
    results = [dict(book) for book in books]
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
