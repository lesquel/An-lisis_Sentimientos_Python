import { useAuth } from "../contexts/AuthContext";
import { useNavigate } from "react-router-dom";

export default function Navbar() {
  const { user, logout, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate("/login");
  };

  if (!isAuthenticated) return null;

  return (
    <nav
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        right: 0,
        background: "rgba(255, 255, 255, 0.95)",
        backdropFilter: "blur(10px)",
        boxShadow: "0 2px 20px rgba(0, 0, 0, 0.1)",
        zIndex: 1000,
        padding: "12px 20px",
      }}
    >
      <div
        style={{
          maxWidth: "1200px",
          margin: "0 auto",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
        }}
      >
        {/* Logo */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "12px",
            cursor: "pointer",
          }}
          onClick={() => navigate("/")}
        >
          <div
            style={{
              width: "40px",
              height: "40px",
              background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
              borderRadius: "12px",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: "24px",
            }}
          >
            🧠
          </div>
          <span
            style={{
              fontSize: "1.25rem",
              fontWeight: 700,
              background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
            }}
          >
            Sentimind
          </span>
        </div>

        {/* User Info */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "16px",
          }}
        >
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "10px",
              padding: "8px 16px",
              background: "#f3f4f6",
              borderRadius: "30px",
            }}
          >
            <div
              style={{
                width: "32px",
                height: "32px",
                background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                borderRadius: "50%",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                color: "white",
                fontWeight: 700,
                fontSize: "0.9rem",
              }}
            >
              {user?.username?.charAt(0).toUpperCase() || "U"}
            </div>
            <span
              style={{
                fontWeight: 600,
                color: "#374151",
                fontSize: "0.9rem",
              }}
            >
              {user?.username || "Usuario"}
            </span>
          </div>

          <button
            onClick={handleLogout}
            style={{
              padding: "10px 20px",
              fontSize: "0.9rem",
              fontWeight: 600,
              color: "#dc2626",
              background: "#fef2f2",
              border: "none",
              borderRadius: "10px",
              cursor: "pointer",
              transition: "all 0.2s ease",
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = "#fee2e2";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = "#fef2f2";
            }}
          >
            Cerrar sesión
          </button>
        </div>
      </div>
    </nav>
  );
}
