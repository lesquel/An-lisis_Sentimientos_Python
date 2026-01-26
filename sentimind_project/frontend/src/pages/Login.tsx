import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      await login(username, password);
      navigate("/");
    } catch (err: unknown) {
      if (err && typeof err === "object" && "response" in err) {
        const axiosError = err as { response?: { data?: { detail?: string } } };
        setError(axiosError.response?.data?.detail || "Error al iniciar sesion");
      } else {
        setError("Error al iniciar sesion");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      minHeight: "100vh",
      background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      padding: "20px",
    }}>
      <div style={{
        background: "rgba(255, 255, 255, 0.95)",
        borderRadius: "24px",
        boxShadow: "0 25px 80px rgba(0, 0, 0, 0.25)",
        width: "100%",
        maxWidth: "420px",
        padding: "40px",
      }}>
        <div style={{ textAlign: "center", marginBottom: "32px" }}>
          <div style={{
            width: "80px",
            height: "80px",
            margin: "0 auto 16px",
            background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            borderRadius: "20px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: "40px",
          }}>
            🧠
          </div>
          <h1 style={{ fontSize: "1.75rem", fontWeight: 700, color: "#1f2937", marginBottom: "8px" }}>
            Bienvenido de vuelta
          </h1>
          <p style={{ color: "#6b7280" }}>Inicia sesion en Sentimind Network</p>
        </div>

        {error && (
          <div style={{
            background: "#fef2f2",
            border: "1px solid #fecaca",
            borderRadius: "12px",
            padding: "12px 16px",
            marginBottom: "24px",
            color: "#dc2626",
          }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: "20px" }}>
            <label style={{ display: "block", marginBottom: "8px", fontWeight: 600, color: "#374151" }}>
              Usuario
            </label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Tu nombre de usuario"
              required
              style={{
                width: "100%",
                padding: "14px 16px",
                fontSize: "1rem",
                border: "2px solid #e5e7eb",
                borderRadius: "12px",
                outline: "none",
              }}
            />
          </div>

          <div style={{ marginBottom: "24px" }}>
            <label style={{ display: "block", marginBottom: "8px", fontWeight: 600, color: "#374151" }}>
              Contrasena
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Tu contrasena"
              required
              style={{
                width: "100%",
                padding: "14px 16px",
                fontSize: "1rem",
                border: "2px solid #e5e7eb",
                borderRadius: "12px",
                outline: "none",
              }}
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            style={{
              width: "100%",
              padding: "14px",
              fontSize: "1rem",
              fontWeight: 700,
              color: "white",
              background: loading ? "#9ca3af" : "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
              border: "none",
              borderRadius: "12px",
              cursor: loading ? "not-allowed" : "pointer",
            }}
          >
            {loading ? "Iniciando sesion..." : "Iniciar Sesion"}
          </button>
        </form>

        <div style={{ marginTop: "24px", textAlign: "center" }}>
          <Link to="/forgot-password" style={{ color: "#667eea", textDecoration: "none" }}>
            ¿Olvidaste tu contrasena?
          </Link>
        </div>

        <div style={{ marginTop: "16px", paddingTop: "16px", borderTop: "1px solid #e5e7eb", textAlign: "center" }}>
          <span style={{ color: "#6b7280" }}>¿No tienes cuenta? </span>
          <Link to="/register" style={{ color: "#667eea", textDecoration: "none", fontWeight: 600 }}>
            Registrate
          </Link>
        </div>
      </div>
    </div>
  );
}
