const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || (import.meta.env.DEV ? "http://127.0.0.1:8000" : "");

async function getApiError(response, fallback) {
  const errorData = await response.json().catch(() => ({}));
  const detail = errorData.detail;
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) {
    return detail.map((issue) => {
      const message = issue?.msg || JSON.stringify(issue);
      const field = Array.isArray(issue?.loc) ? issue.loc.slice(1).join(".") : "";
      return field ? `${field}: ${message}` : message;
    }).join("; ");
  }
  return fallback;
}

function getAuthHeaders() {
  const token = localStorage.getItem("access_token");
  const headers = { "Content-Type": "application/json" };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  return headers;
}

function tripCacheKey() {
  const userId = localStorage.getItem("user_id");
  return userId ? `travel-planner.saved-trips.${userId}` : null;
}

function readCachedTrips() {
  const key = tripCacheKey();
  if (!key) return [];
  try {
    const cached = JSON.parse(localStorage.getItem(key) || "[]");
    return Array.isArray(cached) ? cached : [];
  } catch {
    return [];
  }
}

function writeCachedTrips(trips) {
  const key = tripCacheKey();
  if (!key) return;
  try {
    localStorage.setItem(key, JSON.stringify(trips));
  } catch {
    // The server remains the source of truth when browser storage is unavailable.
  }
}

function rememberTrip(trip) {
  if (!trip?.id || !tripCacheKey()) return trip;
  const cached = readCachedTrips();
  const previous = cached.find((item) => item.id === trip.id);
  const merged = {
    ...previous,
    ...trip,
    itinerary: trip.itinerary ?? previous?.itinerary ?? [],
    preferences: { ...(previous?.preferences || {}), ...(trip.preferences || {}) },
  };
  writeCachedTrips([merged, ...cached.filter((item) => item.id !== trip.id)]);
  return merged;
}

function makeLocalTrip(tripData) {
  const userId = localStorage.getItem("user_id");
  if (!userId) throw new Error("Sign in before saving a trip on this device.");
  const trip = {
    ...tripData,
    id: globalThis.crypto?.randomUUID?.() || `local-${Date.now()}`,
    user_id: userId,
    days: tripData.itinerary?.length || 0,
    preferences: {
      travel_style: tripData.travel_style,
      interests: tripData.interests || [],
      budget_per_day: tripData.budget_per_day,
      currency: tripData.currency || "INR",
      pace: tripData.pace || "moderate",
      num_travelers: tripData.num_travelers || 1,
      dietary_needs: tripData.dietary_needs || "",
    },
    created_at: new Date().toISOString(),
  };
  return rememberTrip(trip);
}

function removeCachedTrip(id) {
  writeCachedTrips(readCachedTrips().filter((trip) => trip.id !== id));
}

export const tripsAPI = {
  async planTrip(tripData) {
    const response = await fetch(`${API_BASE_URL}/trips/plan`, {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify(tripData),
    });

    if (!response.ok) {
      throw new Error(await getApiError(response, `Failed to plan trip (${response.status})`));
    }
    return response.json();
  },

  async createTrip(tripData) {
    let response;
    try {
      response = await fetch(`${API_BASE_URL}/trips/create`, {
        method: "POST",
        headers: getAuthHeaders(),
        body: JSON.stringify(tripData),
      });
    } catch {
      return makeLocalTrip(tripData);
    }

    if (!response.ok) {
      throw new Error(await getApiError(response, `Failed to create trip (${response.status})`));
    }
    return rememberTrip(await response.json());
  },

  async getTrips() {
    try {
      const response = await fetch(`${API_BASE_URL}/trips`, { headers: getAuthHeaders() });
      if (!response.ok) throw new Error("Failed to fetch trips");
      const trips = await response.json();
      const cached = readCachedTrips();
      const merged = new Map(cached.map((trip) => [trip.id, trip]));
      for (const trip of trips) {
        const previous = merged.get(trip.id);
        merged.set(trip.id, {
          ...previous,
          ...trip,
          itinerary: trip.itinerary ?? previous?.itinerary ?? [],
          preferences: { ...(previous?.preferences || {}), ...(trip.preferences || {}) },
        });
      }
      const result = [...merged.values()].sort((a, b) => (b.created_at || "").localeCompare(a.created_at || ""));
      writeCachedTrips(result);
      return result;
    } catch (error) {
      const cached = readCachedTrips();
      if (cached.length) return cached;
      throw error instanceof Error ? error : new Error("Failed to fetch trips");
    }
  },

  async getTripById(id) {
    try {
      const response = await fetch(`${API_BASE_URL}/trips/${id}`, { headers: getAuthHeaders() });
      if (!response.ok) throw new Error("Trip not found");
      return rememberTrip(await response.json());
    } catch (error) {
      const cached = readCachedTrips().find((trip) => trip.id === id);
      if (cached) return cached;
      throw error instanceof Error ? error : new Error("Trip not found");
    }
  },

  async updateTrip(id, tripData) {
    let response;
    try {
      response = await fetch(`${API_BASE_URL}/trips/${id}`, {
        method: "PATCH",
        headers: getAuthHeaders(),
        body: JSON.stringify(tripData),
      });
    } catch {
      const cached = readCachedTrips().find((trip) => trip.id === id);
      if (!cached) throw new Error("This trip is not cached on this device.");
      const preferenceFields = [
        "travel_style", "interests", "budget_per_day", "currency", "pace",
        "num_travelers", "dietary_needs",
      ];
      const preferenceUpdates = Object.fromEntries(
        preferenceFields.filter((field) => field in tripData).map((field) => [field, tripData[field]]),
      );
      return rememberTrip({
        ...cached,
        ...tripData,
        preferences: { ...(cached.preferences || {}), ...preferenceUpdates },
        itinerary: tripData.itinerary ?? cached.itinerary,
        updated_at: new Date().toISOString(),
      });
    }
    if (!response.ok) {
      throw new Error(await getApiError(response, "Failed to update trip"));
    }
    return rememberTrip(await response.json());
  },

  async deleteTrip(id) {
    try {
      const response = await fetch(`${API_BASE_URL}/trips/${id}`, {
        method: "DELETE",
        headers: getAuthHeaders(),
      });
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || "Failed to delete trip");
      }
    } catch (error) {
      if (!readCachedTrips().some((trip) => trip.id === id)) throw error;
    }
    removeCachedTrip(id);
  },

  async regenerateDay(data) {
    const response = await fetch(`${API_BASE_URL}/trips/regenerate-day`, {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      throw new Error(await getApiError(response, "Failed to regenerate day"));
    }
    return response.json();
  },
};

export const authAPI = {
  async getProfile() {
    const response = await fetch(`${API_BASE_URL}/auth/me`, {
      headers: getAuthHeaders(),
    });
    if (!response.ok) {
      throw new Error(await getApiError(response, "Could not load account details."));
    }
    return response.json();
  },

  async register(data) {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || "Registration failed");
    }
    return response.json();
  },

  async login(data) {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || "Login failed");
    }
    const session = await response.json();
    localStorage.setItem("access_token", session.access_token);
    localStorage.setItem("user_id", session.user_id);
    localStorage.setItem("user_email", session.email || data.email);
    if (session.name) localStorage.setItem("user_name", session.name);
    window.dispatchEvent(new Event("auth-change"));
    return session;
  },

  logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_id");
    window.dispatchEvent(new Event("auth-change"));
  },
};

// Backwards compatibility
export async function planTrip(trip) {
  return tripsAPI.planTrip(trip);
}
