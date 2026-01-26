import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

export default function Register() {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    password2: "",
    first_name: "",
    last_name: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (formData.password !== formData.password2) {
      setError("Las contrasenas no coinciden");
      return;
    }

    if (formData.password.length < 8) {
      setError("La contrasena debe tener al menos 8 caracteres");
      return;
    }

    setLoading(true);

    try {
      await register(formData);
      navigate("/");
    } catch (err: unknown) {
      if (err && typeof err === "object" && "response" in err) {
        const axiosError = err as { response?: { data?: Record<string, string[]> } };
        const errors = axiosError.response?.data;
        if (errors) {
          const firstError = Object.values(errors)[0];
          setError(Array.isArray(firstError) ? firstError[0] : String(firstError));
        } else {
          setError("Error al registrarse");
        }
      } else {
        setError("Error al registrarse");
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
        maxWidth: "480px",
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
            Crear cuenta
          </h1>
          <p style={{ color: "#6b7280" }}>Unete a Sentimind Network</p>
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
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px", marginBottom: "20px" }}>
            <div>
              <label style={{ display: "block", marginBottom: "8px", fontWeight: 600, color: "#374151" }}>Nombre</label>
              <input
                type="text"
                name="first_name"
                value={formData.first_name}
                onChange={handleChange}
                placeholder="Tu nombre"
                style={{ width: "100%", padding: "14px 16px", border: "2px solid #e5e7eb", borderRadius: "12px", outline: "none" }}
              />
            </div>
            <div>
              <label style={{ display: "block", marginBottom: "8px", fontWeight: 600, color: "#374151" }}>Apellido</label>
              <input
                type="text"
                name="last_name"
                value={formData.last_name}
                onChange={handleChange}
                placeholder="Tu apellido"
                style={{ width: "100%", padding: "14px 16px", border: "2px solid #e5e7eb", borderRadius: "12px", outline: "none" }}
              />
            </div>
          </div>

          <div style={{ marginBottom: "20px" }}>
            <label style={{ display: "block", marginBottom: "8px", fontWeight: 600, color: "#374151" }}>Usuario *</label>
            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleChange}
              placeholder="Elige un nombre de usuario"
              required
              style={{ width: "100%", padding: "14px 16px", border: "2px solid #e5e7eb", borderRadius: "12px", outline: "none" }}
            />
          </div>

          <div style={{ marginBottom: "20px" }}>
            <label style={{ display: "block", marginBottom: "8px", fontWeight: 600, color: "#374151" }}>Email *</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="tu@email.com"
              required
              style={{ width: "100%", padding: "14px 16px", border: "2px solid #e5e7eb", borderRadius: "12px", outline: "none" }}
            />
          </div>

          <div style={{ marginBottom: "20px" }}>
            <label style={{ display: "block", marginBottom: "8px", fontWeight: 600, color: "#374151" }}>Contrasena *</label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Minimo 8 caracteres"
              required
              style={{ width: "100%", padding: "14px 16px", border: "2px solid #e5e7eb", borderRadius: "12px", outline: "none" }}
            />
          </div>

          <div style={{ marginBottom: "24px" }}>
            <label style={{ display: "block", marginBottom: "8px", fontWeight: 600, color: "#374151" }}>Confirmar contrasena *</label>
            <input
              type="password"
              name="password2"
              value={formData.password2}
              onChange={handleChange}
              placeholder="Repite tu contrasena"
              required
              style={{ width: "100%", padding: "14px 16px", border: "2px solid #e5e7eb", borderRadius: "12px", outline: "none" }}
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
            {loading ? "Creando cuenta..." : "Crear cuenta"}
          </button>
        </form>

        <div style={{ marginTop: "24px", paddingTop: "16px", borderTop: "1px solid #e5e7eb", textAlign: "center" }}>
          <span style={{ color: "#6b7280" }}>¿Ya tienes cuenta? </span>
          <Link to="/login" style={{ color: "#667eea", textDecoration: "none", fontWeight: 600 }}>
            Inicia sesion
          </Link>
        </div>
      </div>
    </div>
  );
}
