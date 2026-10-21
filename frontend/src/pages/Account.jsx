import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { LogIn, LogOut, UserPlus } from "lucide-react";
import { authAPI } from "../services/api.js";

function Account() {
  const navigate = useNavigate();
  const [authenticated, setAuthenticated] = useState(Boolean(localStorage.getItem("access_token")));
  const [registering, setRegistering] = useState(false);
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function submit(event) {
    event.preventDefault();
    setLoading(true);
    setError("");
    try {
      if (registering) {
        await authAPI.register(form);
      }
      await authAPI.login({ email: form.email, password: form.password });
      setAuthenticated(true);
      navigate("/trips");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not sign in.");
    } finally {
      setLoading(false);
    }
  }

  function logout() {
    authAPI.logout();
    setAuthenticated(false);
    navigate("/");
  }

  return (
    <section className="account-page">
      <div className="account-card">
        {authenticated ? (
          <>
            <p className="saved-trips-eyebrow">ACCOUNT</p>
            <h1>You’re signed in</h1>
            <p>Your saved trips are linked to this account.</p>
            <div className="account-actions">
              <button className="btn-primary" onClick={() => navigate("/trips")}>View My Trips</button>
              <button className="btn-secondary" onClick={logout}><LogOut size={16} /> Sign out</button>
            </div>
          </>
        ) : (
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
        )}
      </div>
    </section>
  );
}

export default Account;
