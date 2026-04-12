import { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";
import {
    getCurrentUser,
    isAuthenticated,
    getRecords,
    createRecord,
    updateRecord,
    deleteRecord,
} from "../services/api.jsx";

function RecordsOverviewPage() {
    const [records, setRecords] = useState([]);
    const [formData, setFormData] = useState({
        name: "",
        description: "",
    });
    const [editingRecordId, setEditingRecordId] = useState(null);
    const [loading, setLoading] = useState(true);
    const [submitting, setSubmitting] = useState(false);
    const [errorMessage, setErrorMessage] = useState("");
    const [successMessage, setSuccessMessage] = useState("");

    const sessionData = getCurrentUser();
    const authenticated = isAuthenticated();

    async function loadRecordsData() {
        try {
            setLoading(true);
            setErrorMessage("");

            const data = await getRecords();

            if (!Array.isArray(data)) {
                throw new Error("Invalid records response.");
            }

            setRecords(data);
        } catch (error) {
            setErrorMessage(
                error instanceof Error ? error.message : "Failed to load records."
            );
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        if (authenticated && sessionData.token) {
            loadRecordsData();
        } else {
            setLoading(false);
        }
    }, [authenticated, sessionData.token]);

    function handleChange(event) {
        const { name, value } = event.target;

        setFormData((previous) => ({
            ...previous,
            [name]: value,
        }));
    }

    function resetForm() {
        setFormData({
            name: "",
            description: "",
        });
        setEditingRecordId(null);
    }

    function startEdit(record) {
        setFormData({
            name: typeof record.name === "string" ? record.name : "",
            description:
                typeof record.description === "string" ? record.description : "",
        });
        setEditingRecordId(record.id);
        setErrorMessage("");
        setSuccessMessage("");
    }

    function cancelEdit() {
        resetForm();
        setErrorMessage("");
        setSuccessMessage("");
    }

    async function handleSubmit(event) {
        event.preventDefault();
        setErrorMessage("");
        setSuccessMessage("");

        const trimmedName = formData.name.trim();
        const trimmedDescription = formData.description.trim();

        if (!trimmedName) {
            setErrorMessage("Name is required.");
            return;
        }

        setSubmitting(true);

        try {
            const payload = {
                name: trimmedName,
                description: trimmedDescription,
            };

            let data;

            if (editingRecordId !== null) {
                data = await updateRecord(editingRecordId, payload);
                setSuccessMessage(`Record ${data.id} updated successfully.`);
            } else {
                data = await createRecord(payload);
                setSuccessMessage(`Record ${data.id} created successfully.`);
            }

            resetForm();
            await loadRecordsData();
        } catch (error) {
            setErrorMessage(
                error instanceof Error ? error.message : "Record operation failed."
            );
        } finally {
            setSubmitting(false);
        }
    }

    async function handleDelete(recordId) {
        setErrorMessage("");
        setSuccessMessage("");

        const confirmed = window.confirm(
            `Are you sure you want to delete record ${recordId}?`
        );

        if (!confirmed) {
            return;
        }

        try {
            const data = await deleteRecord(recordId);

            setSuccessMessage(
                typeof data.message === "string"
                    ? data.message
                    : `Record ${recordId} deleted successfully.`
            );

            if (editingRecordId === recordId) {
                resetForm();
            }

            await loadRecordsData();
        } catch (error) {
            setErrorMessage(
                error instanceof Error ? error.message : "Failed to delete record."
            );
        }
    }

    if (!authenticated || !sessionData.token) {
        return <Navigate to="/" replace />;
    }

    return (
        <div style={{ padding: "20px" }}>
            <h1>Records</h1>

            <form
                onSubmit={handleSubmit}
                noValidate
                style={{ marginBottom: "24px" }}
            >
                <h2>{editingRecordId !== null ? "Edit record" : "Create record"}</h2>

                <div style={{ marginBottom: "12px", maxWidth: "420px" }}>
                    <label htmlFor="name">Name</label>
                    <br />
                    <input
                        id="name"
                        name="name"
                        type="text"
                        value={formData.name}
                        onChange={handleChange}
                        maxLength={100}
                        required
                        style={{ width: "100%", padding: "8px" }}
                    />
                </div>

                <div style={{ marginBottom: "12px", maxWidth: "420px" }}>
                    <label htmlFor="description">Description</label>
                    <br />
                    <textarea
                        id="description"
                        name="description"
                        value={formData.description}
                        onChange={handleChange}
                        maxLength={500}
                        rows={4}
                        style={{ width: "100%", padding: "8px" }}
                    />
                </div>

                {errorMessage && <p style={{ color: "red" }}>{errorMessage}</p>}

                {successMessage && (
                    <p style={{ color: "green" }}>{successMessage}</p>
                )}

                <button type="submit" disabled={submitting}>
                    {submitting
                        ? "Saving..."
                        : editingRecordId !== null
                          ? "Update Record"
                          : "Create Record"}
                </button>

                {editingRecordId !== null && (
                    <button
                        type="button"
                        onClick={cancelEdit}
                        style={{ marginLeft: "10px" }}
                    >
                        Cancel
                    </button>
                )}
            </form>

            <hr />

            <h2>Current records</h2>

            {loading ? (
                <p>Loading records...</p>
            ) : records.length === 0 ? (
                <p>No records found.</p>
            ) : (
                <table
                    style={{
                        width: "100%",
                        borderCollapse: "collapse",
                        marginTop: "12px",
                    }}
                >
                    <thead>
                        <tr>
                            <th
                                style={{
                                    textAlign: "left",
                                    borderBottom: "1px solid #ccc",
                                    padding: "8px",
                                }}
                            >
                                ID
                            </th>
                            <th
                                style={{
                                    textAlign: "left",
                                    borderBottom: "1px solid #ccc",
                                    padding: "8px",
                                }}
                            >
                                Name
                            </th>
                            <th
                                style={{
                                    textAlign: "left",
                                    borderBottom: "1px solid #ccc",
                                    padding: "8px",
                                }}
                            >
                                Description
                            </th>
                            <th
                                style={{
                                    textAlign: "left",
                                    borderBottom: "1px solid #ccc",
                                    padding: "8px",
                                }}
                            >
                                Actions
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        {records.map((record) => (
                            <tr key={record.id}>
                                <td
                                    style={{
                                        padding: "8px",
                                        borderBottom: "1px solid #eee",
                                    }}
                                >
                                    {record.id}
                                </td>
                                <td
                                    style={{
                                        padding: "8px",
                                        borderBottom: "1px solid #eee",
                                    }}
                                >
                                    {record.name}
                                </td>
                                <td
                                    style={{
                                        padding: "8px",
                                        borderBottom: "1px solid #eee",
                                    }}
                                >
                                    {record.description || "-"}
                                </td>
                                <td
                                    style={{
                                        padding: "8px",
                                        borderBottom: "1px solid #eee",
                                    }}
                                >
                                    <button
                                        type="button"
                                        onClick={() => startEdit(record)}
                                    >
                                        Edit
                                    </button>

                                    {sessionData.role === "admin" && (
                                        <button
                                            type="button"
                                            onClick={() => handleDelete(record.id)}
                                            style={{ marginLeft: "8px" }}
                                        >
                                            Delete
                                        </button>
                                    )}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}

export default RecordsOverviewPage;