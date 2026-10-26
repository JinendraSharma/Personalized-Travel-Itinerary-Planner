import { useEffect, useState } from "react";
import { Routes, Route, Link, Navigate, useLocation, useNavigate } from "react-router-dom";
import { Sparkles, Compass, MapPin } from "lucide-react";
import Home from "./pages/Home.jsx";
import CreateTrip from "./pages/CreateTrip.jsx";
import SavedTrips from "./pages/SavedTrips.jsx";
import TripView from "./pages/TripView.jsx";
import Account from "./pages/Account.jsx";
import ItineraryDisplay from "./components/ItineraryDisplay.jsx";
import { planTrip } from "./services/api.js";

function RequireAuth({ authenticated, children }) {
  return authenticated ? children : <Navigate to="/" replace />;
}

function App() {
  const [itinerary, setItinerary] = useState([]);
  const [currentTrip, setCurrentTrip] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const location = useLocation();
  const navigate = useNavigate();
  // Keep authenticated users signed in across reloads while sending new visitors to login.
  const [authenticated, setAuthenticated] = useState(() => Boolean(localStorage.getItem("access_token")));

  useEffect(() => {
    const syncAuthentication = () => setAuthenticated(Boolean(localStorage.getItem("access_token")));
    window.addEventListener("auth-change", syncAuthentication);
    window.addEventListener("storage", syncAuthentication);
    return () => {
      window.removeEventListener("auth-change", syncAuthentication);
      window.removeEventListener("storage", syncAuthentication);
    };
  }, []);

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
          {authenticated ? (
            <>
              <Link to="/" className={location.pathname === "/" ? "active" : ""}>Home</Link>
              <Link to="/create" className={location.pathname === "/create" ? "active" : ""}>Smart Trip Builder</Link>
              <Link to="/trips" className={location.pathname.startsWith("/trips") ? "active" : ""}>My Trips</Link>
              <Link to="/account" className={location.pathname === "/account" ? "active" : ""}>Account</Link>
              {itinerary.length > 0 && (
                <Link to="/itinerary" className={location.pathname === "/itinerary" ? "active" : ""}>View Itinerary</Link>
              )}
            </>
          ) : (
            <Link to="/account" className={location.pathname === "/account" ? "active" : ""}>
              Sign in
            </Link>
          )}
        </nav>
      </header>

      {/* Main Routes */}
      <main>
        <Routes>
          <Route
            path="/"
            element={authenticated ? (
              <Home
                onPlanTrip={handlePlanTrip}
                itinerary={itinerary}
                currentTrip={currentTrip}
                loading={loading}
                error={error}
              />
            ) : <Account forceLogin />}
          />
          <Route
            path="/create"
            element={<RequireAuth authenticated={authenticated}>
              <CreateTrip
                onTripGenerated={handleTripGenerated}
              />
            </RequireAuth>}
          />
          <Route path="/trips" element={<RequireAuth authenticated={authenticated}><SavedTrips /></RequireAuth>} />
          <Route path="/trips/:tripId" element={<RequireAuth authenticated={authenticated}><TripView /></RequireAuth>} />
          <Route path="/account" element={<Account forceLogin={!authenticated} />} />
          <Route
            path="/itinerary"
            element={<RequireAuth authenticated={authenticated}>
              <div style={{ maxWidth: "900px", margin: "2rem auto", padding: "0 1.5rem" }}>
                <ItineraryDisplay itinerary={itinerary} tripDetails={currentTrip} />
              </div>
            </RequireAuth>}
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
