import { useState } from "react";

function TripForm({ onSubmit, loading = false }) {
  const [destination, setDestination] = useState("");
  const [days, setDays] = useState(3);
  const [interests, setInterests] = useState("");

  function handleSubmit(event) {
    event.preventDefault();
    if (!destination.trim()) return;

    const startDate = new Date();
    const endDate = new Date(startDate);
    endDate.setDate(startDate.getDate() + Number(days) - 1);
    const formatDate = (date) => {
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, "0");
      const day = String(date.getDate()).padStart(2, "0");
      return `${year}-${month}-${day}`;
    };

    onSubmit({
      destination: destination.trim(),
      start_date: formatDate(startDate),
      end_date: formatDate(endDate),
      interests: interests.split(",").map((item) => item.trim()).filter(Boolean),
    });
  }

  return (
    <form className="quick-trip-form" onSubmit={handleSubmit}>
      <label className="quick-trip-field quick-trip-destination">
        <span>Where to?</span>
        <input value={destination} onChange={(event) => setDestination(event.target.value)} placeholder="e.g. Jaipur, India" required />
      </label>
      <label className="quick-trip-field quick-trip-days">
        <span>How many days?</span>
        <input type="number" min="1" max="30" value={days} onChange={(event) => setDays(event.target.value)} required />
      </label>
      <label className="quick-trip-field quick-trip-interests">
        <span>What do you enjoy?</span>
        <input value={interests} onChange={(event) => setInterests(event.target.value)} placeholder="History, local food, nature" />
      </label>
      <button className="btn-primary quick-trip-submit" type="submit" disabled={loading}>{loading ? "Planning your trip…" : "Create my itinerary"}</button>
    </form>
  );
}

export default TripForm;
