import { useState, useEffect } from "react";
import { getProducts, addProduct, deleteProduct } from "../api/chatApi";

function ShopDashboard() {
  const [products, setProducts] = useState([]);
  const [form, setForm] = useState({ name: "", price: "", stock: "", category: "" });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProducts();
  }, []);

  async function fetchProducts() {
    setLoading(true);
    try {
      const data = await getProducts();
      setProducts(data);
    } catch (err) {
      console.error("Failed to load products", err);
    } finally {
      setLoading(false);
    }
  }

  async function handleAdd() {
    if (!form.name || !form.price) return;
    try {
      await addProduct({
        name: form.name,
        price: parseFloat(form.price),
        stock: parseInt(form.stock || "0", 10),
        category: form.category,
      });
      setForm({ name: "", price: "", stock: "", category: "" });
      fetchProducts();
    } catch (err) {
      console.error("Failed to add product", err);
    }
  }

  async function handleDelete(id) {
    try {
      await deleteProduct(id);
      fetchProducts();
    } catch (err) {
      console.error("Failed to delete product", err);
    }
  }

  return (
    <div className="dashboard">
      <h2 className="dashboard__title">Shop Dashboard</h2>

      <div className="dashboard__form">
        <input
          placeholder="Product name"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
        />
        <input
          placeholder="Price"
          type="number"
          value={form.price}
          onChange={(e) => setForm({ ...form, price: e.target.value })}
        />
        <input
          placeholder="Stock"
          type="number"
          value={form.stock}
          onChange={(e) => setForm({ ...form, stock: e.target.value })}
        />
        <input
          placeholder="Category"
          value={form.category}
          onChange={(e) => setForm({ ...form, category: e.target.value })}
        />
        <button onClick={handleAdd}>Add Product</button>
      </div>

      {loading ? (
        <p>Loading products...</p>
      ) : (
        <table className="dashboard__table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Price</th>
              <th>Stock</th>
              <th>Category</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {products.map((p) => (
              <tr key={p.id}>
                <td>{p.name}</td>
                <td>₹{p.price}</td>
                <td>{p.stock}</td>
                <td>{p.category}</td>
                <td>
                  <button onClick={() => handleDelete(p.id)} className="dashboard__delete-btn">
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <style>{`
        .dashboard {
          padding: 24px;
          max-width: 800px;
          margin: 0 auto;
        }
        .dashboard__title {
          font-size: 20px;
          margin-bottom: 16px;
          color: #1f2230;
        }
        .dashboard__form {
          display: flex;
          gap: 8px;
          margin-bottom: 20px;
          flex-wrap: wrap;
        }
        .dashboard__form input {
          padding: 8px 10px;
          border: 1px solid #ddd;
          border-radius: 8px;
          font-size: 13px;
        }
        .dashboard__form button {
          padding: 8px 16px;
          background: #4f46e5;
          color: #fff;
          border: none;
          border-radius: 8px;
          cursor: pointer;
        }
        .dashboard__table {
          width: 100%;
          border-collapse: collapse;
        }
        .dashboard__table th, .dashboard__table td {
          padding: 8px 10px;
          border-bottom: 1px solid #eee;
          text-align: left;
          font-size: 13.5px;
        }
        .dashboard__delete-btn {
          background: #ef4444;
          color: #fff;
          border: none;
          padding: 4px 10px;
          border-radius: 6px;
          font-size: 12px;
          cursor: pointer;
        }
      `}</style>
    </div>
  );
}

export default ShopDashboard;