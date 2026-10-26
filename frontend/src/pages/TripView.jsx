import { useCallback, useEffect, useMemo, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { motion } from "framer-motion";
import {
  ArrowLeft, CalendarDays, Check, Clipboard, Download, Edit3,
  LoaderCircle, MapPin, RefreshCw, Share2, Users,
} from "lucide-react";
import { tripsAPI } from "../services/api.js";

function normalizeDay(day, index) {
  return {
    day: day.day_number ?? day.day ?? index + 1,
    date: day.date ?? null,
    title: day.title || `Day ${index + 1}`,
    summary: day.notes ?? day.summary ?? "",
    activities: Array.isArray(day.activities) ? day.activities : [],
  };
}

function activityText(activity, index) {
  if (typeof activity === "string") return `  ${index + 1}. ${activity}`;
  const lines = [`  ${index + 1}. ${activity.title || "Activity"}`];
  if (activity.time_slot) lines.push(`     Time: ${activity.time_slot}`);
  if (activity.location) lines.push(`     Location: ${activity.location}`);
  if (activity.description) lines.push(`     ${activity.description}`);
  if (activity.estimated_cost != null) lines.push(`     Estimated cost: ${activity.estimated_cost}`);
  return lines.join("\n");
}

function TripView() {
  const { tripId } = useParams();
  const navigate = useNavigate();
  const [trip, setTrip] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [sharing, setSharing] = useState(false);
  const [regeneratingDay, setRegeneratingDay] = useState(null);

  const loadTrip = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const result = await tripsAPI.getTripById(tripId);
      setTrip({ ...result, itinerary: (result.itinerary || []).map(normalizeDay) });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not load this trip.");
    } finally {
      setLoading(false);
    }
  }, [tripId]);

  useEffect(() => { loadTrip(); }, [loadTrip]);

  const shareUrl = useMemo(() => `${window.location.origin}/trips/${tripId}`, [tripId]);
  const summary = useMemo(() => {
    if (!trip) return "";
    const preference = trip.preferences || {};
    const lines = [
      `# ${trip.destination} itinerary`,
      `**Dates:** ${trip.start_date || "Dates not set"} to ${trip.end_date || "Dates not set"}`,
      preference.num_travelers ? `**Travelers:** ${preference.num_travelers}` : "",
      "",
      ...trip.itinerary.flatMap((day) => [
        `## Day ${day.day}: ${day.title}`,
        ...(day.summary ? [day.summary] : []),
        ...day.activities.map(activityText),
        "",
      ]),
      `Open trip: ${shareUrl}`,
    ];
    return lines.filter((line) => line !== undefined).join("\n").trim();
  }, [trip, shareUrl]);

  async function copyText(text, successMessage) {
    try {
      await navigator.clipboard.writeText(text);
      setNotice(successMessage);
    } catch {
      setError("Clipboard access is unavailable here. You can still download the itinerary.");
    }
  }

  async function shareTrip() {
    setSharing(true);
    setNotice("");
    setError("");
    try {
      if (navigator.share) {
        await navigator.share({ title: `${trip.destination} itinerary`, text: summary, url: shareUrl });
        setNotice("Trip shared.");
      } else {
        await copyText(`${summary}\n\n${shareUrl}`, "Trip summary and link copied.");
      }
    } catch (err) {
      if (err?.name !== "AbortError") setError("Could not share this trip.");
    } finally {
      setSharing(false);
    }
  }

  function downloadFile() {
    const filename = `${(trip.destination || "trip").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "trip"}-itinerary.md`;
    const blobUrl = URL.createObjectURL(new Blob([summary], { type: "text/markdown;charset=utf-8" }));
    const anchor = document.createElement("a");
    anchor.href = blobUrl;
    anchor.download = filename;
    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();
    URL.revokeObjectURL(blobUrl);
    setNotice("Readable itinerary summary downloaded.");
  }

  async function regenerate(day) {
    const feedback = window.prompt(`What should change about Day ${day.day}?`, "Make this day more relaxed");
    if (!feedback?.trim()) return;
    setRegeneratingDay(day.day);
    setError("");
    setNotice("");
    try {
      const preference = trip.preferences || {};
      const updatedDay = await tripsAPI.regenerateDay({
        destination: trip.destination,
        day_number: day.day,
        original_title: day.title,
        travel_style: preference.travel_style || "cultural",
        interests: preference.interests || [],
        feedback: feedback.trim(),
        budget_per_day: preference.budget_per_day || 5000,
        currency: preference.currency || "INR",
      });
      const nextDays = trip.itinerary.map((item) => item.day === day.day
        ? normalizeDay({ ...updatedDay, day: day.day })
        : item);
      const saved = await tripsAPI.updateTrip(tripId, { itinerary: nextDays });
      setTrip({ ...saved, itinerary: (saved.itinerary || []).map(normalizeDay) });
      setNotice(`Day ${day.day} was regenerated and saved.`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not regenerate this day.");
    } finally {
      setRegeneratingDay(null);
    }
  }

  if (loading) return <div className="trip-view-state"><LoaderCircle className="spin" /> Loading trip…</div>;
  if (error && !trip) return <section className="trip-view-page"><div className="error-banner">{error}</div><button className="btn-secondary" onClick={() => navigate("/trips")}><ArrowLeft size={16} /> My Trips</button></section>;
  if (!trip) return null;

  return (
    <section className="trip-view-page">
      <Link to="/trips" className="trip-view-back"><ArrowLeft size={16} /> My Trips</Link>
      <motion.header className="trip-view-hero" initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}>
        <div>
          <p className="saved-trips-eyebrow">YOUR SAVED ITINERARY</p>
          <h1>{trip.destination}</h1>
          <div className="trip-view-meta">
            <span><CalendarDays size={16} /> {trip.start_date || "Dates not set"} – {trip.end_date || "Dates not set"}</span>
            {trip.preferences?.num_travelers && <span><Users size={16} /> {trip.preferences.num_travelers} traveler(s)</span>}
            <span><MapPin size={16} /> {trip.itinerary.length} planned day(s)</span>
          </div>
        </div>
        <div className="trip-view-actions">
          <button className="btn-secondary" onClick={() => copyText(shareUrl, "Trip link copied.")}><Clipboard size={16} /> Copy link</button>
          <button className="btn-secondary" onClick={() => copyText(summary, "Itinerary summary copied.")}><Clipboard size={16} /> Copy summary</button>
          <button className="btn-secondary" onClick={shareTrip} disabled={sharing}><Share2 size={16} /> {sharing ? "Sharing…" : "Share"}</button>
          <button className="btn-secondary" onClick={downloadFile}><Download size={16} /> Download itinerary</button>
          <button className="btn-primary" onClick={() => navigate("/trips", { state: { editTripId: trip.id } })}><Edit3 size={16} /> Edit trip</button>
        </div>
      </motion.header>

      {error && <div className="error-banner" role="alert">{error}</div>}
      {notice && <div className="saved-trip-notice" role="status"><Check size={16} /> {notice}</div>}

      {trip.itinerary.length === 0 ? <div className="saved-trips-empty"><h2>No itinerary days saved</h2><p>Generate an itinerary for this trip to see its day-by-day plan here.</p></div> : (
        <div className="trip-view-days">
          {trip.itinerary.map((day, index) => (
            <motion.article className="trip-view-day" key={day.day} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: index * 0.04 }}>
              <div className="trip-view-day-heading">
                <div><span className="trip-view-day-label">DAY {day.day}</span><h2>{day.title}</h2>{day.summary && <p>{day.summary}</p>}</div>
                <button className="icon-button" onClick={() => regenerate(day)} disabled={regeneratingDay !== null} title="Regenerate this day">
                  {regeneratingDay === day.day ? <LoaderCircle className="spin" size={17} /> : <RefreshCw size={17} />}
                </button>
              </div>
              {day.activities.length ? <ol className="trip-view-activities">{day.activities.map((activity, activityIndex) => {
                const isText = typeof activity === "string";
                return <li key={`${day.day}-${activityIndex}`}><span className="trip-view-activity-time">{isText ? `Activity ${activityIndex + 1}` : activity.time_slot || "Activity"}</span><h3>{isText ? activity : activity.title}</h3>{!isText && activity.description && <p>{activity.description}</p>}{!isText && activity.location && <span className="trip-view-location"><MapPin size={14} /> {activity.location}</span>}</li>;
              })}</ol> : <p className="trip-view-no-activities">No activities listed for this day.</p>}
            </motion.article>
          ))}
        </div>
      )}
    </section>
  );
}

export default TripView;
