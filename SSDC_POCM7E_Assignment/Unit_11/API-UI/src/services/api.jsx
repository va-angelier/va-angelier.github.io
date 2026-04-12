const API_BASE_URL = "/api";

function getSession() {
    try {
        const rawSession = sessionStorage.getItem("session");
        return rawSession ? JSON.parse(rawSession) : null;
    } catch {
        sessionStorage.removeItem("session");
        return null;
    }
}

function getSessionToken() {
    const session = getSession();
    return typeof session?.token === "string" ? session.token : "";
}

function getRole() {
    const session = getSession();
    return typeof session?.role === "string" ? session.role : "";
}

function buildHeaders(includeJson = true) {
    const headers = {
        Accept: "application/json",
    };

    if (includeJson) {
        headers["Content-Type"] = "application/json";
    }

    const token = getSessionToken();

    if (token) {
        headers["X-Session-Token"] = token;
    }

    return headers;
}

function buildProtectedHeaders(includeJson = true) {
    return {
        ...buildHeaders(includeJson),
        "X-API-Key": "my-secret-api-access-token",
    };
}

async function handleResponse(response) {
    let data = null;

    try {
        data = await response.json();
    } catch {
        data = null;
    }

    if (!response.ok) {
        const message =
            data?.error ||
            data?.message ||
            `Request failed with status ${response.status}`;
        throw new Error(message);
    }

    return data;
}

export function saveAuthSession(data) {
    const sessionData = {
        authenticated: true,
        username: typeof data.username === "string" ? data.username : "",
        role: typeof data.role === "string" ? data.role : "user",
        secure_mode: Boolean(data.secure_mode),
        token: typeof data.session_token === "string" ? data.session_token : "",
    };

    sessionStorage.setItem("session", JSON.stringify(sessionData));
}

export function clearAuthSession() {
    sessionStorage.removeItem("session");
}

export function isAuthenticated() {
    const session = getSession();

    return Boolean(
        session &&
        session.authenticated === true &&
        typeof session.token === "string" &&
        session.token.length > 0
    );
}

export function isAdmin() {
    return getRole() === "admin";
}

export function getCurrentUser() {
    const session = getSession();

    return {
        username: typeof session?.username === "string" ? session.username : "",
        role: typeof session?.role === "string" ? session.role : "",
        token: typeof session?.token === "string" ? session.token : "",
        secureMode: Boolean(session?.secure_mode),
        authenticated: Boolean(session?.authenticated),
    };
}

export async function getSecurityMode() {
    const response = await fetch(`${API_BASE_URL}/security/mode`, {
        method: "GET",
        headers: {
            Accept: "application/json",
        },
    });

    return handleResponse(response);
}

export async function registerUser(payload) {
    const response = await fetch(`${API_BASE_URL}/register`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
        },
        body: JSON.stringify(payload),
    });

    return handleResponse(response);
}

export async function loginUser(payload) {
    const response = await fetch(`${API_BASE_URL}/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
        },
        body: JSON.stringify(payload),
    });

    return handleResponse(response);
}

export async function logoutUser() {
    const response = await fetch(`${API_BASE_URL}/logout`, {
        method: "POST",
        headers: buildHeaders(false),
    });

    return handleResponse(response);
}

export async function getMe() {
    const response = await fetch(`${API_BASE_URL}/me`, {
        method: "GET",
        headers: buildHeaders(false),
    });

    return handleResponse(response);
}

export async function getProfile(username) {
    const response = await fetch(`${API_BASE_URL}/profile/${username}`, {
        method: "GET",
        headers: buildHeaders(false),
    });

    return handleResponse(response);
}

export async function getRecords() {
    const response = await fetch(`${API_BASE_URL}/records`, {
        method: "GET",
        headers: buildHeaders(false),
    });

    return handleResponse(response);
}

export async function getRecord(recordId) {
    const response = await fetch(`${API_BASE_URL}/records/${recordId}`, {
        method: "GET",
        headers: buildHeaders(false),
    });

    return handleResponse(response);
}

export async function createRecord(payload) {
    const response = await fetch(`${API_BASE_URL}/records`, {
        method: "POST",
        headers: buildProtectedHeaders(true),
        body: JSON.stringify(payload),
    });

    return handleResponse(response);
}

export async function updateRecord(recordId, payload) {
    const response = await fetch(`${API_BASE_URL}/records/${recordId}`, {
        method: "PUT",
        headers: buildProtectedHeaders(true),
        body: JSON.stringify(payload),
    });

    return handleResponse(response);
}

export async function deleteRecord(recordId) {
    const response = await fetch(`${API_BASE_URL}/records/${recordId}`, {
        method: "DELETE",
        headers: buildProtectedHeaders(false),
    });

    return handleResponse(response);
}

export async function getSecurityEvents() {
    const response = await fetch(`${API_BASE_URL}/security/events`, {
        method: "GET",
        headers: buildProtectedHeaders(false),
    });

    return handleResponse(response);
}

export async function setSecurityMode(enabled) {
    const response = await fetch(`${API_BASE_URL}/security/mode`, {
        method: "POST",
        headers: buildProtectedHeaders(true),
        body: JSON.stringify({ enabled }),
    });

    return handleResponse(response);
}

export async function deleteUser(username) {
    const response = await fetch(`${API_BASE_URL}/users/${username}`, {
        method: "DELETE",
        headers: buildProtectedHeaders(false),
    });

    return handleResponse(response);
}