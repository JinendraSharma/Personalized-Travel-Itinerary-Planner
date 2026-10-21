import ItineraryDisplay from "../components/ItineraryDisplay.jsx";
import TripForm from "../components/TripForm.jsx";

function Home({ onPlanTrip, itinerary, loading, error }) {
  return (
    <main>
      <h1>Personalized Travel Itinerary Planner</h1>
      <p>Build a simple trip plan around your destination, duration, and interests.</p>
      <TripForm onSubmit={onPlanTrip} loading={loading} />
      {error && <p role="alert">{error}</p>}
      <ItineraryDisplay itinerary={itinerary} />
    </main>
  );
}

export default Home;
