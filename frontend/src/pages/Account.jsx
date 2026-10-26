import { useCallback, useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { ArrowRight, CalendarDays, CircleUserRound, Compass, LogIn, LogOut, MapPin, ShieldCheck, UserPlus } from "lucide-react";
import { authAPI, tripsAPI } from "../services/api.js";

function Account({ forceLogin = false }) {
  const navigate = useNavigate();
  const [authenticated, setAuthenticated] = useState(() => !forceLogin && Boolean(localStorage.getItem("access_token")));
  const [profile, setProfile] = useState(() => {
    const name = localStorage.getItem("user_name");
    const email = localStorage.getItem("user_email");
    return name || email ? { name, email } : null;
  });
  const [trips, setTrips] = useState(() => tripsAPI.getCachedTrips());
  const [registering, setRegistering] = useState(false);
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [loading, setLoading] = useState(false);
  const [profileLoading, setProfileLoading] = useState(false);
  const [error, setError] = useState("");

  const loadAccount = useCallback(async () => {
    if (!localStorage.getItem("access_token")) return;
    const cachedProfile = { name: localStorage.getItem("user_name"), email: localStorage.getItem("user_email") };
    setProfile((current) => current || cachedProfile);
    setProfileLoading(!cachedProfile.name && !cachedProfile.email);
    setError("");
    try {
      const [profileResult, tripsResult] = await Promise.allSettled([authAPI.getProfile(), tripsAPI.getTrips()]);
      if (profileResult.status === "fulfilled") {
        setProfile(profileResult.value);
        localStorage.setItem("user_email", profileResult.value.email);
        localStorage.setItem("user_name", profileResult.value.name);
      } else {
        if (!cachedProfile.name && !cachedProfile.email) setError("Your account details are unavailable. Please sign in again.");
      }
      if (tripsResult.status === "fulfilled") setTrips(tripsResult.value);
      else setError("We couldn’t load your saved trips. Please try again.");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not load account details.");
    } finally {
      setProfileLoading(false);
    }
  }, []);

  useEffect(() => { if (authenticated) loadAccount(); }, [authenticated, loadAccount]);

  useEffect(() => {
    const syncTrips = (event) => setTrips(event.detail || []);
    window.addEventListener("travel-planner:trips-updated", syncTrips);
    return () => window.removeEventListener("travel-planner:trips-updated", syncTrips);
  }, []);

  async function submit(event) {
    event.preventDefault();
    setLoading(true);
    setError("");
    try {
      if (registering) await authAPI.register(form);
      else await authAPI.login({ email: form.email, password: form.password });
      setAuthenticated(true);
      navigate("/");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not sign in.");
    } finally {
      setLoading(false);
    }
  }

  function logout() {
    authAPI.logout();
    localStorage.removeItem("user_email");
    localStorage.removeItem("user_name");
    setAuthenticated(false);
    setProfile(null);
    setTrips([]);
    navigate("/");
  }

  const memberSince = profile?.created_at
    ? new Date(profile.created_at).toLocaleDateString(undefined, { month: "long", year: "numeric" })
    : null;

  return (
    <section className={`account-page ${authenticated ? "account-page-signed-in" : ""}`}>
      {authenticated ? (
        <>
          <header className="account-heading">
            <div>
              <p className="saved-trips-eyebrow">YOUR TRAVEL PROFILE</p>
              <h1>Account</h1>
              <p>Manage your profile and pick up where your next journey begins.</p>
            </div>
            <button className="btn-secondary" onClick={logout}><LogOut size={16} /> Sign out</button>
          </header>

          {error && <div className="error-banner" role="alert">{error}</div>}

          <div className="account-dashboard">
            <article className="account-profile-card">
              <div className="account-avatar"><CircleUserRound size={34} strokeWidth={1.5} /></div>
              <div className="account-profile-copy">
                <p className="account-section-kicker">PROFILE DETAILS</p>
                {profileLoading && !profile ? <p>Loading your profile…</p> : (
                  <>
                    <h2>{profile?.name || "Traveler"}</h2>
                    <p className="account-email">{profile?.email || localStorage.getItem("user_email") || "Email unavailable"}</p>
                  </>
                )}
                {memberSince && <p className="account-member-since">Traveling with us since {memberSince}</p>}
              </div>
              <span className="account-secure-label"><ShieldCheck size={15} /> Private account</span>
            </article>

            <article className="account-trips-card">
              <div className="account-trips-heading">
                <div>
                  <p className="account-section-kicker">YOUR TRAVEL LIBRARY</p>
                  <h2>Saved trips <span>{profileLoading ? "…" : trips.length}</span></h2>
                </div>
                <Link to="/trips" className="account-view-all">View all <ArrowRight size={15} /></Link>
              </div>
              {profileLoading && trips.length === 0 ? <p className="account-trips-empty">Loading your saved trips…</p> : trips.length ? (
                <div className="account-recent-trips">
                  {trips.slice(0, 3).map((trip) => (
                    <Link className="account-trip-row" key={trip.id} to={`/trips/${trip.id}`}>
                      <span className="account-trip-icon"><MapPin size={17} /></span>
                      <span className="account-trip-copy"><strong>{trip.destination}</strong><small><CalendarDays size={13} /> {trip.start_date} – {trip.end_date}</small></span>
                      <ArrowRight className="account-trip-arrow" size={17} />
                    </Link>
                  ))}
                </div>
              ) : (
                <div className="account-trips-empty"><Compass size={22} /><p>Your saved itineraries will show up here.</p><Link to="/create">Plan your first trip <ArrowRight size={14} /></Link></div>
              )}
              <Link to="/create" className="btn-primary account-new-trip"><Compass size={16} /> Plan a new trip</Link>
            </article>
          </div>
        </>
      ) : (
        <div className="account-card">
          <form onSubmit={submit}>
            <p className="saved-trips-eyebrow">TRAVEL PLANNER ACCOUNT</p>
            <h1>{registering ? "Create your account" : "Welcome back"}</h1>
            <p>Sign in to save and manage your itineraries across sessions.</p>
            {registering && <label>Name<input required minLength="2" autoComplete="name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} /></label>}
            <label>Email<input required type="email" autoComplete="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} /></label>
            <label>Password<input required minLength="8" type="password" autoComplete={registering ? "new-password" : "current-password"} value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} /></label>
            {error && <div className="error-banner" role="alert">{error}</div>}
            <button className="btn-primary account-submit" type="submit" disabled={loading}>
              {registering ? <UserPlus size={16} /> : <LogIn size={16} />}{loading ? "Please wait…" : registering ? "Create account" : "Sign in"}
            </button>
            <button className="account-mode-toggle" type="button" onClick={() => { setRegistering(!registering); setError(""); }}>
              {registering ? "Already have an account? Sign in" : "New here? Create an account"}
            </button>
          </form>
        </div>
      )}
    </section>
  );
}

export default Account;
