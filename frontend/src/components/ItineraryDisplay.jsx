function ItineraryDisplay({ itinerary }) {
  if (!itinerary?.length) return null;

  return (
    <section aria-live="polite">
      <h2>Your itinerary</h2>
      {itinerary.map((day) => (
        <article key={day.day}>
          <h3>Day {day.day}: {day.title}</h3>
          <ul>{day.activities.map((activity, index) => <li key={`${day.day}-${index}`}>{activity}</li>)}</ul>
        </article>
      ))}
    </section>
  );
}

export default ItineraryDisplay;
