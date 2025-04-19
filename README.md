Código backend com falha de injeção SQL

```py
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
```

Código front-end

```jsx
import React, { useState, useEffect } from "react";


function App() {
  const [search, setSearch] = useState("");
  const [products, setProducts] = useState([]);


  const fetchProducts = async () => {
    const res = await fetch(`http://localhost:5000/products?search=${encodeURIComponent(search)}`);
    const data = await res.json();
    setProducts(data);
  };


  useEffect(() => {
    fetchProducts();
  }, [search]);


  return (
    <div className="container mt-5">
      <h2 className="mb-4">Produtos</h2>
      <div className="mb-3">
        <input
          type="text"
          className="form-control"
          placeholder="Buscar pelo nome do produto"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>


      {products.length === 0 ? (
        <p className="text-muted">Nenhum produto encontrado.</p>
      ) : (
        <div className="list-group">
          {products.map((p) => (
            <div key={p.id} className="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
              <div>
                <h5 className="mb-1">{p.name}</h5>
                <small className="text-muted">Categoria: {p.category}</small>
              </div>
              <span className={`badge ${p.released ? "bg-success" : "bg-warning text-dark"}`}>
                {p.released ? "Lançado" : "Não lançado"}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}


export default App;
```

Demonstração da pesquisa antes da correção

![image](https://github.com/user-attachments/assets/beadd483-7100-4f7e-a535-6242dfcf06a1)

![image](https://github.com/user-attachments/assets/bba3b0fd-c7ca-48d0-ad7d-f8e7e02e9cef)

Correção do erro

```py
@app.route("/products")
def get_products():
    search = request.args.get("search", "")
   
    # SEGURO COM PARÂMETROS
    query = "SELECT * FROM products WHERE name LIKE ? AND released = 1"
    search_term = f"%{search}%"


    conn = sqlite3.connect("ecommerce.db")
    cursor = conn.cursor()
    cursor.execute(query, (search_term,))
    produtos = cursor.fetchall()
    conn.close()


    return jsonify([{
        "id": p[0],
        "name": p[1],
        "category": p[2],
        "released": bool(p[3])
    } for p in produtos])
```

Demonstração da pesquisa após a correção

![image](https://github.com/user-attachments/assets/638a08ed-62af-48d7-8133-925813e71343)

