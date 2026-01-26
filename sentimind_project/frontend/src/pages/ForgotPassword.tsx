import { useState } from "react";
import { Link } from "react-router-dom";
import { authService } from "../adapters/authAdapter";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      await authService.requestPasswordReset(email);
      setSuccess(true);
    } catch (err: unknown) {
      if (err && typeof err === "object" && "response" in err) {
        const axiosError = err as { response?: { data?: { email?: string[] } } };
        setError(axiosError.response?.data?.email?.[0] || "Error al enviar el correo");
      } else {
        setError("Error al enviar el correo");
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
            🔐
          </div>
          <h1 style={{ fontSize: "1.75rem", fontWeight: 700, color: "#1f2937", marginBottom: "8px" }}>
            Recuperar contrasena
          </h1>
          <p style={{ color: "#6b7280" }}>Te enviaremos un enlace para restablecer tu contrasena</p>
        </div>

        {success ? (
          <div style={{
            background: "#ecfdf5",
            border: "1px solid #a7f3d0",
            borderRadius: "12px",
            padding: "20px",
            textAlign: "center",
          }}>
            <div style={{ fontSize: "48px", marginBottom: "16px" }}>✉️</div>
            <h3 style={{ color: "#065f46", fontWeight: 600, marginBottom: "8px" }}>Correo enviado</h3>
            <p style={{ color: "#047857" }}>
              Si existe una cuenta con el email <strong>{email}</strong>, recibiras instrucciones.
            </p>
            <Link to="/login" style={{ display: "inline-block", marginTop: "20px", color: "#667eea", textDecoration: "none", fontWeight: 600 }}>
              Volver al login
            </Link>
          </div>
        ) : (
          <>
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
              <div style={{ marginBottom: "24px" }}>
                <label style={{ display: "block", marginBottom: "8px", fontWeight: 600, color: "#374151" }}>
                  Email
                </label>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="tu@email.com"
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
                {loading ? "Enviando..." : "Enviar enlace de recuperacion"}
              </button>
            </form>

            <div style={{ marginTop: "24px", textAlign: "center" }}>
              <Link to="/login" style={{ color: "#667eea", textDecoration: "none" }}>
                ← Volver al login
              </Link>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
