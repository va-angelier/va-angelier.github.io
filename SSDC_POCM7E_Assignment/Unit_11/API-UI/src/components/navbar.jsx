import { Link, useNavigate } from "react-router-dom";
import {
    getCurrentUser,
    isAuthenticated,
    logoutUser,
    clearAuthSession,
} from "../services/api.jsx";

function Navbar() {
    const navigate = useNavigate();

    const sessionData = getCurrentUser();
    const authenticated = isAuthenticated();

    async function handleLogout() {
        try {
            if (sessionData.token) {
                await logoutUser();
            }
        } catch (error) {
            // Ignore logout API errors and clear client state anyway.
        } finally {
            clearAuthSession();
            navigate("/", { replace: true });
        }
    }

    return (
        <nav style={{ padding: "12px 20px", borderBottom: "1px solid #ccc" }}>
            {!authenticated ? (
                <>
                    <Link to="/">Login</Link> |{" "}
                    <Link to="/register">Register</Link>
                </>
            ) : (
                <>
                    <Link to="/dashboard">Dashboard</Link> |{" "}
                    <Link to="/records">Records</Link> |{" "}
                    {sessionData.role === "admin" && (
                        <>
                            <Link to="/admin">Admin</Link> |{" "}
                        </>
                    )}
                    <button
                        type="button"
                        onClick={handleLogout}
                        style={{
                            border: "none",
                            background: "transparent",
                            cursor: "pointer",
                            padding: 0,
                            font: "inherit",
                            textDecoration: "underline",
                        }}
                    >
                        Logout
                    </button>
                </>
            )}
        </nav>
    );
}

export default Navbar;