import { useEffect, useState } from "react";
import { Link, Navigate } from "react-router-dom";
import {
    getCurrentUser,
    isAuthenticated,
    getMe,
    saveAuthSession,
} from "../services/api.jsx";

function DashboardPage() {
    const [sessionInfo, setSessionInfo] = useState({
        authenticated: false,
        username: "",
        role: "",
        secure_mode: false,
        token: "",
    });
    const [loading, setLoading] = useState(true);
    const [errorMessage, setErrorMessage] = useState("");

    const storedSession = getCurrentUser();
    const authenticated = isAuthenticated();

    useEffect(() => {
        async function loadCurrentUser() {
            try {
                setLoading(true);
                setErrorMessage("");

                if (!storedSession.token) {
                    throw new Error("No session token found.");
                }

                const data = await getMe();

                const nextSession = {
                    authenticated: true,
                    username: typeof data.username === "string" ? data.username : "",
                    role: typeof data.role === "string" ? data.role : "",
                    secure_mode: Boolean(data.secure_mode),
                    session_token: storedSession.token,
                };

                saveAuthSession(nextSession);

                setSessionInfo({
                    authenticated: true,
                    username: nextSession.username,
                    role: nextSession.role,
                    secure_mode: nextSession.secure_mode,
                    token: storedSession.token,
                });
            } catch (error) {
                setErrorMessage(
                    error instanceof Error ? error.message : "Failed to load dashboard."
                );
            } finally {
                setLoading(false);
            }
        }

        if (authenticated && storedSession.token) {
            loadCurrentUser();
        } else {
            setLoading(false);
        }
    }, [authenticated, storedSession.token]);

    if (!authenticated || !storedSession.token) {
        return <Navigate to="/" replace />;
    }

    if (loading) {
        return (
            <div style={{ padding: "20px" }}>
                <h1>Dashboard</h1>
                <p>Loading dashboard...</p>
            </div>
        );
    }

    if (errorMessage) {
        return (
            <div style={{ padding: "20px" }}>
                <h1>Dashboard</h1>
                <p style={{ color: "red" }}>{errorMessage}</p>
            </div>
        );
    }

    return (
        <div style={{ padding: "20px" }}>
            <h1>Dashboard</h1>

            <p>
                Logged in as <strong>{sessionInfo.username || "unknown"}</strong> | role:{" "}
                <strong>{sessionInfo.role || "unknown"}</strong> | secure_mode:{" "}
                <strong>{String(sessionInfo.secure_mode)}</strong>
            </p>

            <hr />

            <h2>Session details</h2>
            <ul>
                <li>Authenticated: {String(sessionInfo.authenticated)}</li>
                <li>Username: {sessionInfo.username || "unknown"}</li>
                <li>Role: {sessionInfo.role || "unknown"}</li>
                <li>Secure mode: {String(sessionInfo.secure_mode)}</li>
            </ul>
        </div>
    );
}

export default DashboardPage;