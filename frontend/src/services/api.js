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
    const response = await fetch(`${API_BASE_URL}/trips/create`, {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify(tripData),
    });

    if (!response.ok) {
      throw new Error(await getApiError(response, `Failed to create trip (${response.status})`));
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

  async updateTrip(id, tripData) {
    const response = await fetch(`${API_BASE_URL}/trips/${id}`, {
      method: "PATCH",
      headers: getAuthHeaders(),
      body: JSON.stringify(tripData),
    });
    if (!response.ok) {
      throw new Error(await getApiError(response, "Failed to update trip"));
    }
    return response.json();
  },

  async deleteTrip(id) {
    const response = await fetch(`${API_BASE_URL}/trips/${id}`, {
      method: "DELETE",
      headers: getAuthHeaders(),
    });
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || "Failed to delete trip");
    }
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
    return session;
  },

  logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_id");
  },
};

// Backwards compatibility
export async function planTrip(trip) {
  return tripsAPI.planTrip(trip);
}
