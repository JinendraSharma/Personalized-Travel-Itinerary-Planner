const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

function getAuthHeaders() {
  const token = localStorage.getItem("access_token");
  const headers = { "Content-Type": "application/json" };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  return headers;
}

export const tripsAPI = {
  async planTrip(tripData) {
    const response = await fetch(`${API_BASE_URL}/trips/plan`, {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify(tripData),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `Failed to plan trip (${response.status})`);
    }
    return response.json();
  },

  async createTrip(tripData) {
    const response = await fetch(`${API_BASE_URL}/trips/create`, {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify(tripData),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `Failed to create trip (${response.status})`);
    }
    return response.json();
  },

  async getTrips() {
    const response = await fetch(`${API_BASE_URL}/trips`, {
      headers: getAuthHeaders(),
    });
    if (!response.ok) {
      throw new Error("Failed to fetch trips");
    }
    return response.json();
  },

  async getTripById(id) {
    const response = await fetch(`${API_BASE_URL}/trips/${id}`, {
      headers: getAuthHeaders(),
    });
    if (!response.ok) {
      throw new Error("Trip not found");
    }
    return response.json();
  },

  async regenerateDay(data) {
    const response = await fetch(`${API_BASE_URL}/trips/regenerate-day`, {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || "Failed to regenerate day");
    }
    return response.json();
  },
};

export const authAPI = {
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
    return response.json();
  },
};

// Backwards compatibility
export async function planTrip(trip) {
  return tripsAPI.planTrip(trip);
}
