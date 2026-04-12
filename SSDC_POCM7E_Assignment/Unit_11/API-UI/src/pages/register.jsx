import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";

function RegisterPage() {
    const navigate = useNavigate();

    const [formData, setFormData] = useState({
        username: "",
        password: "",
        role: "user"
    });

    const [errorMessage, setErrorMessage] = useState("");
    const [successMessage, setSuccessMessage] = useState("");
    const [isSubmitting, setIsSubmitting] = useState(false);

    function handleChange(event) {
        const { name, value } = event.target;

        setFormData((previous) => ({
            ...previous,
            [name]: value
        }));
    }

    async function handleSubmit(event) {
        event.preventDefault();
        setErrorMessage("");
        setSuccessMessage("");

        const username = formData.username.trim();
        const password = formData.password;
        const role = formData.role;

        if (!username || !password) {
            setErrorMessage("Username and password are required.");
            return;
        }

        if (password.length < 8) {
            setErrorMessage("Password must be at least 8 characters long.");
            return;
        }

        if (role !== "user" && role !== "admin") {
            setErrorMessage("Role must be either user or admin.");
            return;
        }

        setIsSubmitting(true);

        try {
            const response = await fetch("/api/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                body: JSON.stringify({
                    username,
                    password,
                    role
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    typeof data.error === "string"
                        ? data.error
                        : "Registration failed."
                );
            }

            setSuccessMessage(
                typeof data.message === "string"
                    ? data.message
                    : "User registered successfully."
            );

            setFormData({
                username: "",
                password: "",
                role: "user"
            });

            setTimeout(() => {
                navigate("/", { replace: true });
            }, 1000);
        } catch (error) {
            setErrorMessage(
                error instanceof Error ? error.message : "Registration failed."
            );
        } finally {
            setIsSubmitting(false);
        }
    }

    return (
        <div style={{ padding: "20px", maxWidth: "420px" }}>
            <h1>Register</h1>

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
                        autoComplete="new-password"
                        maxLength={128}
                        required
                        style={{ width: "100%", padding: "8px" }}
                    />
                </div>

                <div style={{ marginBottom: "12px" }}>
                    <label htmlFor="role">Role</label>
                    <br />
                    <select
                        id="role"
                        name="role"
                        value={formData.role}
                        onChange={handleChange}
                        style={{ width: "100%", padding: "8px" }}
                    >
                        <option value="user">user</option>
                        <option value="admin">admin</option>
                    </select>
                </div>

                {errorMessage && (
                    <p style={{ color: "red" }}>{errorMessage}</p>
                )}

                {successMessage && (
                    <p style={{ color: "green" }}>{successMessage}</p>
                )}

                <button type="submit" disabled={isSubmitting}>
                    {isSubmitting ? "Registering..." : "Register"}
                </button>
            </form>

            <p style={{ marginTop: "16px" }}>
                Already have an account? <Link to="/">Go to login</Link>
            </p>
        </div>
    );
}

export default RegisterPage;