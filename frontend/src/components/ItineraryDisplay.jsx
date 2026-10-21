import React, { useState, useEffect } from "react";
import {
  Clock,
  MapPin,
  Calendar,
  DollarSign,
  Bookmark,
  Share2,
  Printer,
  Sparkles,
  ChevronDown,
  ChevronUp,
  Tag,
  CheckCircle,
  Navigation,
  Footprints,
  RefreshCw,
  Sliders,
} from "lucide-react";
import { tripsAPI } from "../services/api";

function ItineraryDisplay({ itinerary: initialItinerary, tripDetails, onSaved }) {
  const [days, setDays] = useState(initialItinerary || []);
  const [activeDay, setActiveDay] = useState(1);
  const [saving, setSaving] = useState(false);
  const [savedSuccess, setSavedSuccess] = useState(false);
  const [saveError, setSaveError] = useState("");

  // Vibe refinement state
  const [showRefine, setShowRefine] = useState(false);
  const [refineFeedback, setRefineFeedback] = useState("");
  const [refining, setRefining] = useState(false);
  const [refineSuccess, setRefineSuccess] = useState("");

  useEffect(() => {
    if (initialItinerary) {
      setDays(initialItinerary);
    }
  }, [initialItinerary]);

  if (!days || !days.length) return null;

  const currentDayData = days.find((d) => d.day === activeDay) || days[0];

  const handleSaveTrip = async () => {
    if (!tripDetails) return;
    setSaving(true);
    setSaveError("");
    try {
      await tripsAPI.createTrip({
        ...tripDetails,
        itinerary: days,
      });
      setSavedSuccess(true);
      if (onSaved) onSaved();
      setTimeout(() => setSavedSuccess(false), 4000);
    } catch (err) {
      setSaveError(err instanceof Error ? err.message : "Failed to save trip to database");
    } finally {
      setSaving(false);
    }
  };

  const handleRefineDay = async (e) => {
    e.preventDefault();
    if (!refineFeedback.trim()) return;

    setRefining(true);
    setSaveError("");
    setRefineSuccess("");

    try {
      const updatedDay = await tripsAPI.regenerateDay({
        destination: tripDetails?.destination || "Destination",
        day_number: activeDay,
        original_title: currentDayData.title,
        travel_style: tripDetails?.travel_style || "cultural",
        interests: tripDetails?.interests || [],
        feedback: refineFeedback.trim(),
        budget_per_day: tripDetails?.budget_per_day || 5000.0,
        currency: tripDetails?.currency || "INR",
      });

      setDays((prev) =>
        prev.map((d) => (d.day === activeDay ? { ...updatedDay, day: activeDay } : d))
      );
      setRefineSuccess(`Day ${activeDay} updated with your custom vibe!`);
      setRefineFeedback("");
      setShowRefine(false);
      setTimeout(() => setRefineSuccess(""), 4000);
    } catch (err) {
      setSaveError(err instanceof Error ? err.message : "Failed to refine day");
    } finally {
      setRefining(false);
    }
  };

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="itinerary-dashboard">
      {/* Top Banner / Actions */}
      <div className="itinerary-header-card">
        <div className="itinerary-title-box">
          <h2>
            <Sparkles className="sparkle-icon" size={24} />
            {tripDetails?.destination ? `${tripDetails.destination} Itinerary` : "Your Personalized Itinerary"}
          </h2>
          <p className="itinerary-subtitle">
            {days.length}-Day curated travel plan with vibe-based personalization and route optimization.
          </p>
        </div>

        <div className="itinerary-actions">
          <button className="btn-secondary" onClick={handlePrint} title="Print or save as PDF">
            <Printer size={16} /> Print Plan
          </button>
          <button
            className={`btn-primary ${savedSuccess ? "btn-success" : ""}`}
            onClick={handleSaveTrip}
            disabled={saving || savedSuccess}
          >
            {savedSuccess ? (
              <>
                <CheckCircle size={16} /> Saved to Database!
              </>
            ) : (
              <>
                <Bookmark size={16} /> {saving ? "Saving..." : "Save Itinerary"}
              </>
            )}
          </button>
        </div>
      </div>

      {saveError && <div className="error-banner">{saveError}</div>}
      {refineSuccess && (
        <div style={{ background: "#ecfdf5", color: "#065f46", border: "1px solid #a7f3d0", padding: "0.75rem 1rem", borderRadius: "8px", marginBottom: "1.25rem", fontSize: "0.9rem" }}>
          ✓ {refineSuccess}
        </div>
      )}

      {/* Day Selector Tabs */}
      <div className="days-tab-bar">
        {days.map((day) => (
          <button
            key={day.day}
            className={`day-tab-btn ${activeDay === day.day ? "active" : ""}`}
            onClick={() => {
              setActiveDay(day.day);
              setShowRefine(false);
            }}
          >
            <span className="day-tab-num">Day {day.day}</span>
            <span className="day-tab-sub">{day.title?.substring(0, 24)}...</span>
          </button>
        ))}
      </div>

      {/* Selected Day Timeline View */}
      <div className="day-timeline-card">
        <div className="day-card-header" style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: "0.75rem" }}>
          <div>
            <h3>Day {currentDayData.day}: {currentDayData.title}</h3>
            {currentDayData.summary && <p className="day-summary-text">{currentDayData.summary}</p>}
          </div>
          <div style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap", alignItems: "center" }}>
            <span className="route-opt-badge" style={{ background: "#f0fdf4", color: "#166534", border: "1px solid #bbf7d0", padding: "0.3rem 0.75rem", borderRadius: "16px", fontSize: "0.8rem", fontWeight: 600, display: "inline-flex", alignItems: "center", gap: "0.35rem" }}>
              <Navigation size={13} /> Route Optimized
            </span>
            <button
              type="button"
              className="btn-secondary"
              style={{ fontSize: "0.82rem", padding: "0.35rem 0.75rem" }}
              onClick={() => setShowRefine(!showRefine)}
            >
              <Sliders size={13} /> {showRefine ? "Close Vibe Adjuster" : "Refine Day Vibe"}
            </button>
          </div>
        </div>

        {/* Vibe Refinement Drawer */}
        {showRefine && (
          <form onSubmit={handleRefineDay} style={{ background: "#f8fafc", border: "1px dashed var(--primary)", borderRadius: "10px", padding: "1.25rem", marginBottom: "1.5rem" }}>
            <label style={{ display: "block", fontSize: "0.9rem", fontWeight: 600, marginBottom: "0.4rem" }}>
              How would you like to refine Day {activeDay}?
            </label>
            <div style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap", marginBottom: "0.75rem" }}>
              {["More relaxed & chill", "Add rooftop dining", "Budget-friendly options", "Focus on photography", "More beach time", "Local street food safari"].map((hint) => (
                <button
                  type="button"
                  key={hint}
                  style={{ background: "white", border: "1px solid var(--border)", borderRadius: "14px", padding: "0.25rem 0.65rem", fontSize: "0.78rem", cursor: "pointer" }}
                  onClick={() => setRefineFeedback(hint)}
                >
                  + {hint}
                </button>
              ))}
            </div>
            <div style={{ display: "flex", gap: "0.5rem" }}>
              <input
                type="text"
                placeholder="e.g. Swap afternoon museum for outdoor park and sunset lounge"
                value={refineFeedback}
                onChange={(e) => setRefineFeedback(e.target.value)}
                style={{ flex: 1, padding: "0.6rem 0.85rem", border: "1px solid var(--border)", borderRadius: "6px" }}
              />
              <button type="submit" className="btn-primary" disabled={refining || !refineFeedback.trim()} style={{ padding: "0.6rem 1rem", fontSize: "0.88rem" }}>
                {refining ? <RefreshCw className="spin" size={15} /> : <Sparkles size={15} />}
                {refining ? "Adapting..." : "Regenerate Day"}
              </button>
            </div>
          </form>
        )}

        <div className="timeline-items">
          {Array.isArray(currentDayData.activities) && currentDayData.activities.length > 0 ? (
            currentDayData.activities.map((act, idx) => {
              const isString = typeof act === "string";
              const title = isString ? act : act.title;
              const desc = isString ? "" : act.description;
              const slot = isString ? `Activity ${idx + 1}` : act.time_slot;
              const location = isString ? null : act.location;
              const category = isString ? "General" : act.category;
              const cost = isString ? null : act.estimated_cost;
              const transitTime = isString ? null : act.transit_time;
              const neighborhood = isString ? null : act.neighborhood;

              return (
                <div key={idx} className="timeline-slot">
                  <div className="timeline-marker">
                    <div className="marker-dot"></div>
                    <div className="marker-line"></div>
                  </div>

                  <div className="timeline-content-card">
                    <div className="slot-meta">
                      <span className="time-badge">
                        <Clock size={14} /> {slot}
                      </span>
                      {category && (
                        <span className="category-badge">
                          <Tag size={12} /> {category}
                        </span>
                      )}
                      {neighborhood && (
                        <span className="category-badge" style={{ background: "#ede9fe", color: "#5b21b6" }}>
                          📍 {neighborhood}
                        </span>
                      )}
                      {cost !== null && cost > 0 && (
                        <span className="cost-badge">
                          ~{tripDetails?.currency || "INR"} {cost}
                        </span>
                      )}
                    </div>

                    <h4 className="activity-title">{title}</h4>
                    {desc && <p className="activity-desc">{desc}</p>}

                    <div style={{ display: "flex", gap: "1rem", flexWrap: "wrap", alignItems: "center", marginTop: "0.5rem" }}>
                      {location && (
                        <div className="activity-location">
                          <MapPin size={14} /> <span>{location}</span>
                        </div>
                      )}

                      {transitTime && (
                        <div className="transit-indicator" style={{ display: "inline-flex", alignItems: "center", gap: "0.3rem", fontSize: "0.8rem", color: "#4f46e5", background: "#eef2ff", padding: "0.2rem 0.5rem", borderRadius: "6px" }}>
                          <Footprints size={13} />
                          <span>Transit: {transitTime}</span>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              );
            })
          ) : (
            <p className="no-activities">No activities scheduled for this day.</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default ItineraryDisplay;
