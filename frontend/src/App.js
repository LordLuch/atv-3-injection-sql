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
