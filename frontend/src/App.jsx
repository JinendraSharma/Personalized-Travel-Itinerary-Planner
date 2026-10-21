import { useState } from "react";
import Home from "./pages/Home.jsx";
import { planTrip } from "./services/api.js";

function App() {
  const [itinerary, setItinerary] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handlePlanTrip(trip) {
    setLoading(true);
    setError("");
    try {
      const result = await planTrip(trip);
      setItinerary(result.itinerary ?? []);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to generate itinerary.");
    } finally {
      setLoading(false);
    }
  }

  return <Home onPlanTrip={handlePlanTrip} itinerary={itinerary} loading={loading} error={error} />;
}

export default App;
