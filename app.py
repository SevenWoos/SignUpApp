from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

# SQLite DB
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
      CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        first_name TEXT NOT NULL, 
        last_name TEXT NOT NULL, 
        email TEXT NOT NULL UNIQUE
      )
    '''    
    )

    conn.commit()
    conn.close()

  
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    first = request.form['first_name']
    last = request.form['last_name']
    email = request.form['email']


    # Save to database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (first_name, last_name, email) VALUES(?, ?, ?)', (first, last, email))

        conn.commit()
      
    except sqlite3.IntegrityError:
      # return 'User already signed up. Email already exists'
      return render_template('already_exists.html')
    finally:
        conn.close()
    
    # return "Thanks for signing up!"
    return render_template('success.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)