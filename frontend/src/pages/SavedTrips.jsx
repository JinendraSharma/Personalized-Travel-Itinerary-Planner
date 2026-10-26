import { useCallback, useEffect, useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { CalendarDays, MapPin, Pencil, Trash2 } from "lucide-react";
import { tripsAPI } from "../services/api.js";

function SavedTrips() {
  const [trips, setTrips] = useState([]);
  const [selected, setSelected] = useState(null);
  const [form, setForm] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const location = useLocation();

  const loadTrips = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      setTrips(await tripsAPI.getTrips());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not load saved trips.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { loadTrips(); }, [loadTrips]);

  const openTrip = useCallback(async (id) => {
    setError("");
    setNotice("");
    try {
      const trip = await tripsAPI.getTripById(id);
      setSelected(trip);
      setForm({
        destination: trip.destination || "",
        start_date: trip.start_date || "",
        end_date: trip.end_date || "",
        budget_per_day: trip.preferences?.budget_per_day ?? "",
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not open this trip.");
    }
  }, []);

  useEffect(() => {
    if (location.state?.editTripId) openTrip(location.state.editTripId);
  }, [location.state?.editTripId, openTrip]);

  async function saveTrip(event) {
    event.preventDefault();
    setSaving(true);
    setError("");
    setNotice("");
    try {
      const updated = await tripsAPI.updateTrip(selected.id, {
        ...form,
        budget_per_day: form.budget_per_day === "" ? null : Number(form.budget_per_day),
      });
      setSelected(updated);
      await loadTrips();
      setNotice("Trip saved successfully.");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not save this trip.");
    } finally {
      setSaving(false);
    }
  }

  async function removeTrip(id) {
    if (!window.confirm("Delete this trip and its itinerary? This cannot be undone.")) return;
    setError("");
    setNotice("");
    try {
      await tripsAPI.deleteTrip(id);
      if (selected?.id === id) { setSelected(null); setForm(null); }
      await loadTrips();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not delete this trip.");
    }
  }

  return (
    <section className="saved-trips-page">
      <header className="saved-trips-heading">
        <div>
          <p className="saved-trips-eyebrow">YOUR TRAVEL LIBRARY</p>
          <h1>Saved trips</h1>
          <p>Pick up where you left off, update your plan, or remove trips you no longer need.</p>
        </div>
        <Link to="/create" className="btn-primary">Plan a new trip</Link>
      </header>

      {error && <div className="error-banner" role="status">{error}</div>}
      {notice && <div className="saved-trip-notice" role="status">{notice}</div>}
      {loading ? <p>Loading your trips…</p> : trips.length === 0 ? (
        <div className="saved-trips-empty"><MapPin size={28} /><h2>No saved trips yet</h2><p>Generate and save an itinerary to see it here.</p></div>
      ) : (
        <div className="saved-trips-layout">
          <div className="saved-trip-list">
            {trips.map((trip) => (
              <article className={`saved-trip-card ${selected?.id === trip.id ? "selected" : ""}`} key={trip.id}>
                <button className="saved-trip-open" onClick={() => openTrip(trip.id)}>
                  <span className="saved-trip-icon"><MapPin size={18} /></span>
                  <span className="saved-trip-copy"><strong>{trip.destination}</strong><span><CalendarDays size={14} /> {trip.start_date} – {trip.end_date}</span></span>
                </button>
                <div className="saved-trip-card-actions">
                  <button className="icon-button" aria-label={`Edit ${trip.destination}`} onClick={() => openTrip(trip.id)}><Pencil size={16} /></button>
                  <button className="icon-button danger" aria-label={`Delete ${trip.destination}`} onClick={() => removeTrip(trip.id)}><Trash2 size={16} /></button>
                </div>
              </article>
            ))}
          </div>

          {selected && form && (
            <form className="saved-trip-editor" onSubmit={saveTrip}>
              <h2>Edit trip</h2>
              <Link className="saved-trip-detail-link" to={`/trips/${selected.id}`}>View full itinerary</Link>
              <label>Destination<input required value={form.destination} onChange={(e) => setForm({ ...form, destination: e.target.value })} /></label>
              <div className="saved-trip-date-fields">
                <label>Start date<input type="date" value={form.start_date} onChange={(e) => setForm({ ...form, start_date: e.target.value })} /></label>
                <label>End date<input type="date" value={form.end_date} onChange={(e) => setForm({ ...form, end_date: e.target.value })} /></label>
              </div>
              <label>Daily budget<input type="number" min="0" value={form.budget_per_day} onChange={(e) => setForm({ ...form, budget_per_day: e.target.value })} /></label>
              <p className="saved-trip-editor-hint">Your day-by-day itinerary stays saved while you update these trip details.</p>
              <button className="btn-primary" type="submit" disabled={saving}>{saving ? "Saving…" : "Save changes"}</button>
            </form>
          )}
        </div>
      )}
    </section>
  );
}

export default SavedTrips;
