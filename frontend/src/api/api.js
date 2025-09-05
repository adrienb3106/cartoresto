const API_URL = import.meta.env.VITE_API_URL;

export async function getRestaurants() {
  const response = await fetch(`${API_URL}/restaurants/`);
  if (!response.ok) {
    throw new Error("Erreur lors du chargement des restaurants");
  }
  return await response.json();
}