import { Navigate } from "react-router-dom";
import { getCurrentUser, isAuthenticated } from "../services/api.jsx";

function ProtectedRoute({ children, requireAdmin = false }) {
    const sessionData = getCurrentUser();
    const authenticated = isAuthenticated();

    if (!authenticated || !sessionData.token) {
        return <Navigate to="/" replace />;
    }

    if (requireAdmin && sessionData.role !== "admin") {
        return <Navigate to="/dashboard" replace />;
    }

    return children;
}

export default ProtectedRoute;