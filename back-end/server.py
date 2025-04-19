from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def init_db():
    conn = sqlite3.connect("ecommerce.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            released BOOLEAN NOT NULL
        )
    ''')
    conn.commit()

    cursor.execute("DELETE FROM products")

    produtos = [
        ("Tênis Air", "calcados", True),
        ("Camiseta X", "roupas", True),
        ("Jaqueta Storm", "roupas", False),
        ("Fone Gamer", "eletronicos", True),
        ("Notebook Pro", "eletronicos", False),
        ("Relógio Fit", "acessorios", True),
        ("Mochila Urbana", "acessorios", False),
        ("Chinelo Summer", "calcados", True),
        ("Calça Jeans", "roupas", True),
        ("Drone X10", "eletronicos", False)
    ]

    cursor.executemany("INSERT INTO products (name, category, released) VALUES (?, ?, ?)", produtos)
    conn.commit()
    conn.close()

@app.route("/products")
def get_products():
    search = request.args.get("search", "")

    # VULNERÁVEL A SQL INJECTION
    query = f"SELECT * FROM products WHERE name LIKE '%{search}%' AND released = 1"
    print("Query executada:", query)

    conn = sqlite3.connect("ecommerce.db")
    cursor = conn.cursor()
    cursor.execute(query)
    produtos = cursor.fetchall()
    conn.close()

    return jsonify([{
        "id": p[0],
        "name": p[1],
        "category": p[2],
        "released": bool(p[3])
    } for p in produtos])

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
