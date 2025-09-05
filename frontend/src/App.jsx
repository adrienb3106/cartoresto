import { useEffect, useState } from "react";
import { getRestaurants } from "./api/api";

function App() {
  const [page, setPage] = useState("home");
  const [restaurants, setRestaurants] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (page === "restaurants") {
      async function fetchData() {
        try {
          const data = await getRestaurants();
          setRestaurants(data);
        } catch (err) {
          setError(err.message);
        } finally {
          setLoading(false);
        }
      }
      fetchData();
    }
  }, [page]);

  if (page === "home") {
  return (
    <div style={{ textAlign: "center" }}>
      <h1 style={{ fontSize: "3rem", marginBottom: "20px" }}>CartoResto 🍽️</h1>
      <button
        onClick={() => setPage("restaurants")}
        style={{
          padding: "12px 24px",
          fontSize: "1.2rem",
          cursor: "pointer",
          borderRadius: "8px",
          border: "none",
          backgroundColor: "#4CAF50",
          color: "white",
        }}
      >
        Liste des restaurants
      </button>
    </div>
  );
}

  // --- PAGE LISTE ---
  if (page === "restaurants") {
    if (loading) return <p style={{ textAlign: "center" }}>Chargement...</p>;
    if (error) return <p style={{ textAlign: "center", color: "red" }}>Erreur : {error}</p>;

    return (
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          minHeight: "100vh",
          backgroundColor: "#f0f0f0",
        }}
      >
        <h1 style={{ marginBottom: "20px" }}>Liste des restaurants 🍴</h1>
        <ul style={{ listStyle: "none", padding: 0, marginBottom: "20px" }}>
          {restaurants.map((r) => (
            <li
              key={r.id}
              style={{
                margin: "6px 0",
                padding: "10px 15px",
                border: "1px solid #ccc",
                borderRadius: "6px",
                backgroundColor: "#fff",
                textAlign: "center",
                width: "300px",
              }}
            >
              {r.nom} — {r.adresse}
            </li>
          ))}
        </ul>
        <button
          onClick={() => setPage("home")}
          style={{
            padding: "10px 20px",
            fontSize: "1rem",
            cursor: "pointer",
            borderRadius: "8px",
            border: "1px solid #ccc",
            backgroundColor: "#eee",
          }}
        >
          Retour à l'accueil
        </button>
      </div>
    );
  }
}

export default App;
