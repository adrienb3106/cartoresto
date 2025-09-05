import { useEffect, useState } from "react";
import { getRestaurants } from "./api/api";

function App() {
  const [restaurants, setRestaurants] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
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
  }, []);

  if (loading) return <p>Chargement...</p>;
  if (error) return <p style={{ color: "red" }}>Erreur : {error}</p>;

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>CartoResto 🍽️</h1>
      <ul>
        {restaurants.map((r) => (
          <li key={r.id}>
            {r.nom} — {r.adresse}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
