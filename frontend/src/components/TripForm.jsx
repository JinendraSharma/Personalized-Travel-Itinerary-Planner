import { useState } from "react";

function TripForm({ onSubmit, loading = false }) {
  const [destination, setDestination] = useState("");
  const [days, setDays] = useState(3);
  const [interests, setInterests] = useState("");

  function handleSubmit(event) {
    event.preventDefault();
    if (!destination.trim()) return;
    onSubmit({
      destination: destination.trim(),
      days: Number(days),
      interests: interests.split(",").map((item) => item.trim()).filter(Boolean),
    });
  }

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Destination
        <input value={destination} onChange={(event) => setDestination(event.target.value)} placeholder="e.g. Jaipur" required />
      </label>
      <label>
        Number of days
        <input type="number" min="1" max="30" value={days} onChange={(event) => setDays(event.target.value)} required />
      </label>
      <label>
        Interests (comma-separated)
        <input value={interests} onChange={(event) => setInterests(event.target.value)} placeholder="history, food, nature" />
      </label>
      <button type="submit" disabled={loading}>{loading ? "Planning…" : "Generate itinerary"}</button>
    </form>
  );
}

export default TripForm;
