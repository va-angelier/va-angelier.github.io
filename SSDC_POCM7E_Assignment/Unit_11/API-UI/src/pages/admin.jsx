import { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";
import {
    getCurrentUser,
    isAuthenticated,
    getSecurityEvents,
} from "../services/api.jsx";

function AdminPage() {
    const [events, setEvents] = useState([]);
    const [loading, setLoading] = useState(true);
    const [errorMessage, setErrorMessage] = useState("");

    const sessionData = getCurrentUser();
    const authenticated = isAuthenticated();

    useEffect(() => {
        async function loadSecurityEvents() {
            try {
                setLoading(true);
                setErrorMessage("");

                const data = await getSecurityEvents();

                if (!Array.isArray(data)) {
                    throw new Error("Invalid response format.");
                }

                setEvents(data);
            } catch (error) {
                setErrorMessage(
                    error instanceof Error
                        ? error.message
                        : "Failed to load admin data."
                );
            } finally {
                setLoading(false);
            }
        }

        if (authenticated && sessionData.token) {
            loadSecurityEvents();
        }
    }, [authenticated, sessionData.token]);

    if (!authenticated || !sessionData.token) {
        return <Navigate to="/" replace />;
    }

    if (sessionData.role !== "admin") {
        return <Navigate to="/dashboard" replace />;
    }

    if (loading) {
        return (
            <div style={{ padding: "20px" }}>
                <h1>Admin Panel</h1>
                <p>Loading security events...</p>
            </div>
        );
    }

    if (errorMessage) {
        return (
            <div style={{ padding: "20px" }}>
                <h1>Admin Panel</h1>
                <p style={{ color: "red" }}>{errorMessage}</p>
            </div>
        );
    }

    return (
        <div style={{ padding: "20px" }}>
            <h1>Admin Panel</h1>

            {events.length === 0 ? (
                <p>No security events found.</p>
            ) : (
                <ul>
                    {events.map((event, index) => (
                        <li key={index}>
                            <strong>{event.timestamp}</strong> —{" "}
                            {event.event_type} —{" "}
                            {event.outcome} —{" "}
                            {event.identifier}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}

export default AdminPage;