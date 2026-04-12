import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { loginUser, saveAuthSession } from "../services/api.jsx";

function LoginPage() {
    const navigate = useNavigate();

    const [formData, setFormData] = useState({
        username: "",
        password: "",
    });

    const [errorMessage, setErrorMessage] = useState("");
    const [isSubmitting, setIsSubmitting] = useState(false);

    function handleChange(event) {
        const { name, value } = event.target;

        setFormData((previous) => ({
            ...previous,
            [name]: value,
        }));
    }

    async function handleSubmit(event) {
        event.preventDefault();
        setErrorMessage("");

        const username = formData.username.trim();
        const password = formData.password;

        if (!username || !password) {
            setErrorMessage("Username and password are required.");
            return;
        }

        setIsSubmitting(true);

        try {
            const data = await loginUser({
                username,
                password,
            });

            saveAuthSession(data);
            navigate("/dashboard", { replace: true });
        } catch (error) {
            setErrorMessage(
                error instanceof Error ? error.message : "Login failed."
            );
        } finally {
            setIsSubmitting(false);
        }
    }

    return (
        <div style={{ padding: "20px", maxWidth: "420px" }}>
            <h1>Login</h1>

            <form onSubmit={handleSubmit} noValidate>
                <div style={{ marginBottom: "12px" }}>
                    <label htmlFor="username">Username</label>
                    <br />
                    <input
                        id="username"
                        name="username"
                        type="text"
                        value={formData.username}
                        onChange={handleChange}
                        autoComplete="username"
                        maxLength={64}
                        required
                        style={{ width: "100%", padding: "8px" }}
                    />
                </div>

                <div style={{ marginBottom: "12px" }}>
                    <label htmlFor="password">Password</label>
                    <br />
                    <input
                        id="password"
                        name="password"
                        type="password"
                        value={formData.password}
                        onChange={handleChange}
                        autoComplete="current-password"
                        maxLength={128}
                        required
                        style={{ width: "100%", padding: "8px" }}
                    />
                </div>

                {errorMessage && (
                    <p style={{ color: "red" }}>{errorMessage}</p>
                )}

                <button type="submit" disabled={isSubmitting}>
                    {isSubmitting ? "Signing in..." : "Login"}
                </button>
            </form>

            <p style={{ marginTop: "16px" }}>
                No account yet? <Link to="/register">Register here</Link>
            </p>
        </div>
    );
}

export default LoginPage;