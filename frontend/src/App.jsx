import { useState } from "react";
import { Routes, Route, Link, useLocation, useNavigate } from "react-router-dom";
import { Sparkles, Compass, MapPin } from "lucide-react";
import Home from "./pages/Home.jsx";
import CreateTrip from "./pages/CreateTrip.jsx";
import ItineraryDisplay from "./components/ItineraryDisplay.jsx";
import { planTrip } from "./services/api.js";

function App() {
  const [itinerary, setItinerary] = useState([]);
  const [currentTrip, setCurrentTrip] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const location = useLocation();
  const navigate = useNavigate();

  async function handlePlanTrip(trip) {
    setLoading(true);
    setError("");
    try {
      const result = await planTrip(trip);
      setCurrentTrip(result);
      setItinerary(result.itinerary ?? []);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to generate itinerary.");
    } finally {
      setLoading(false);
    }
  }

  function handleTripGenerated(tripResult) {
    setCurrentTrip(tripResult);
    setItinerary(tripResult.itinerary ?? []);
    navigate("/itinerary");
  }

  return (
    <div className="app-root">
      {/* Navigation Header */}
      <header className="app-header">
        <Link to="/" className="brand-logo">
          <Sparkles size={24} />
          <span>TravelAI Planner</span>
        </Link>
        <nav className="nav-links">
          <Link to="/" className={location.pathname === "/" ? "active" : ""}>
            Home
          </Link>
          <Link to="/create" className={location.pathname === "/create" ? "active" : ""}>
            Smart Trip Builder
          </Link>
          {itinerary.length > 0 && (
            <Link to="/itinerary" className={location.pathname === "/itinerary" ? "active" : ""}>
              View Itinerary
            </Link>
          )}
        </nav>
      </header>

      {/* Main Routes */}
      <main>
        <Routes>
          <Route
            path="/"
            element={
              <Home
                onPlanTrip={handlePlanTrip}
                itinerary={itinerary}
                currentTrip={currentTrip}
                loading={loading}
                error={error}
              />
            }
          />
          <Route
            path="/create"
            element={
              <CreateTrip
                onTripGenerated={handleTripGenerated}
              />
            }
          />
          <Route
            path="/itinerary"
            element={
              <div style={{ maxWidth: "900px", margin: "2rem auto", padding: "0 1.5rem" }}>
                <ItineraryDisplay itinerary={itinerary} tripDetails={currentTrip} />
              </div>
            }
          />
        </Routes>
      </main>
    </div>
  );
}

export default App;
