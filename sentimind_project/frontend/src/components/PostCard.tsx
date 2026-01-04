import type { Post } from "../adapters/postAdapter";
import { getCategoryConfig } from "../utils/constants";

interface PostCardProps {
  post: Post;
}

export default function PostCard({ post }: PostCardProps) {
  const config = getCategoryConfig(post.category);
  const confidencePercent = Math.round(post.confidence * 100);

  return (
    <div
      style={{
        background: "white",
        borderRadius: "20px",
        overflow: "hidden",
        boxShadow: "0 10px 40px rgba(0, 0, 0, 0.12)",
        transition: "all 0.3s ease",
        cursor: "default",
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.transform = "translateY(-8px)";
        e.currentTarget.style.boxShadow = "0 25px 60px rgba(0, 0, 0, 0.2)";
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.transform = "translateY(0)";
        e.currentTarget.style.boxShadow = "0 10px 40px rgba(0, 0, 0, 0.12)";
      }}
    >
      {/* Barra superior de color */}
      <div
        style={{
          height: "6px",
          background: `linear-gradient(90deg, ${config.borderColor} 0%, ${config.textColor} 100%)`,
        }}
      />

      <div style={{ padding: "24px" }}>
        {/* Header con categoría y confianza */}
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "flex-start",
            marginBottom: "16px",
          }}
        >
          {/* Badge de categoría */}
          <div
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: "8px",
              padding: "8px 16px",
              borderRadius: "30px",
              backgroundColor: config.bgColor,
              color: config.textColor,
              fontWeight: 700,
              fontSize: "0.75rem",
              textTransform: "uppercase",
              letterSpacing: "0.5px",
            }}
          >
            <span style={{ fontSize: "1rem" }}>{config.emoji}</span>
            <span>{post.category}</span>
          </div>

          {/* Indicador de confianza */}
          <div style={{ textAlign: "right" }}>
            <div
              style={{
                fontSize: "1.25rem",
                fontWeight: 800,
                color: config.textColor,
              }}
            >
              {confidencePercent}%
            </div>
            <div
              style={{
                fontSize: "0.65rem",
                color: "#9ca3af",
                textTransform: "uppercase",
                letterSpacing: "1px",
              }}
            >
              Certeza IA
            </div>
          </div>
        </div>

        {/* Contenido del post */}
        <div
          style={{
            position: "relative",
            padding: "16px 0",
          }}
        >
          <span
            style={{
              position: "absolute",
              top: "0",
              left: "-5px",
              fontSize: "3rem",
              color: config.bgColor,
              fontFamily: "Georgia, serif",
              lineHeight: 1,
            }}
          >
            "
          </span>
          <p
            style={{
              fontSize: "1.1rem",
              lineHeight: 1.7,
              color: "#374151",
              paddingLeft: "20px",
              paddingRight: "10px",
            }}
          >
            {post.content}
          </p>
        </div>

        {/* Footer */}
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            paddingTop: "16px",
            borderTop: "1px solid #f3f4f6",
            marginTop: "8px",
          }}
        >
          {/* Fecha */}
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "6px",
              color: "#9ca3af",
              fontSize: "0.8rem",
            }}
          >
            <span>🕐</span>
            <span>
              {new Date(post.created_at).toLocaleString("es-EC", {
                day: "2-digit",
                month: "short",
                hour: "2-digit",
                minute: "2-digit",
              })}
            </span>
          </div>

          {/* Barra de progreso de confianza */}
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "8px",
            }}
          >
            <div
              style={{
                width: "80px",
                height: "8px",
                backgroundColor: "#f3f4f6",
                borderRadius: "4px",
                overflow: "hidden",
              }}
            >
              <div
                style={{
                  width: `${confidencePercent}%`,
                  height: "100%",
                  background: `linear-gradient(90deg, ${config.borderColor} 0%, ${config.textColor} 100%)`,
                  borderRadius: "4px",
                  transition: "width 0.5s ease",
                }}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
