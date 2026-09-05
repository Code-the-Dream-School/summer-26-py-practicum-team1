export async function getLocations() {
  const response = await fetch("/api/locations");

  if (!response.ok) {
    throw new Error("Failed to load locations");
  }

  const data = await response.json();

  return data.locations;
}
