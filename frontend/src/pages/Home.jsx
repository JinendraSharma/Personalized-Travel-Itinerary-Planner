import React from "react";
import { Link } from "react-router-dom";
import { Compass, Sparkles } from "lucide-react";
import ItineraryDisplay from "../components/ItineraryDisplay.jsx";
import TripForm from "../components/TripForm.jsx";

function Home({ onPlanTrip, itinerary, currentTrip, loading, error }) {
  return (
    <div className="home-container">
      <div className="home-hero">
        <div className="hero-copy">
          <span className="eyebrow"><Compass size={15} /> YOUR NEXT GOOD STORY</span>
          <h1>Go somewhere.<br /><em>Feel everything.</em></h1>
          <p>Thoughtful travel plans, shaped around your pace, your people, and the places you want to know.</p>
          <Link to="/create" className="btn-primary hero-cta"><Sparkles size={17} /> Plan a trip</Link>
        </div>
        <div className="hero-art" aria-label="Illustration of a mountain landscape">
          <span className="hero-sun" /><span className="mountain mountain-back" /><span className="mountain mountain-front" />
          <span className="hero-caption">TAKE THE SCENIC ROUTE</span>
        </div>
      </div>

      <div className="quick-plan-card">
        <div className="quick-plan-heading"><span className="eyebrow">START WITH A DESTINATION</span><h2>A little getaway?</h2><p>Build a quick plan in just a few details.</p></div>
        <TripForm onSubmit={onPlanTrip} loading={loading} />
      </div>

      {error && <div className="error-banner" style={{ marginTop: "1.5rem" }}>{error}</div>}

      {itinerary?.length > 0 && <ItineraryDisplay itinerary={itinerary} tripDetails={currentTrip} />}
    </div>
  );
}

export default Home;
