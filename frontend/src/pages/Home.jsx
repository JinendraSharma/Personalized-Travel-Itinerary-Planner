import React from "react";
import { Link } from "react-router-dom";
import { Compass, Sparkles } from "lucide-react";
import ItineraryDisplay from "../components/ItineraryDisplay.jsx";
import TripForm from "../components/TripForm.jsx";

function Home({ onPlanTrip, itinerary, currentTrip, loading, error }) {
  return (
    <div className="home-container" style={{ maxWidth: "860px", margin: "2rem auto", padding: "0 1.5rem" }}>
      <div className="home-hero" style={{ textAlign: "center", marginBottom: "2rem" }}>
        <h1 style={{ fontSize: "2.2rem", fontWeight: 800, color: "var(--text-main)", marginBottom: "0.5rem" }}>
          AI-Powered Travel Itinerary Planner
        </h1>
        <p style={{ color: "var(--text-muted)", fontSize: "1.05rem", maxWidth: "600px", margin: "0 auto" }}>
          Generate customized day-by-day itineraries tailored to your travel style, budget, and favorite activities.
        </p>

        <div style={{ marginTop: "1rem" }}>
          <Link to="/create" className="btn-primary" style={{ textDecoration: "none", display: "inline-flex" }}>
            <Sparkles size={18} /> Launch Multi-Step Smart Builder
          </Link>
        </div>
      </div>

      <div style={{ background: "white", padding: "1.75rem", borderRadius: "var(--radius)", border: "1px solid var(--border)", boxShadow: "var(--shadow)" }}>
        <h3 style={{ marginBottom: "1rem", fontSize: "1.2rem" }}>Quick Trip Planner</h3>
        <TripForm onSubmit={onPlanTrip} loading={loading} />
      </div>

      {error && <div className="error-banner" style={{ marginTop: "1.5rem" }}>{error}</div>}

      <ItineraryDisplay itinerary={itinerary} tripDetails={currentTrip} />
    </div>
  );
}

export default Home;
