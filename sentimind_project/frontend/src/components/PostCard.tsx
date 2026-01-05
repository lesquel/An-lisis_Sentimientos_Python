import type { Post } from "../adapters/postAdapter";
import { getCategoryConfig } from "../utils/constants";

interface PostCardProps {
  post: Post;
}

export default function PostCard({ post }: PostCardProps) {
  const config = getCategoryConfig(post.category);
  const confidencePercent = Math.round(post.confidence * 100);

  // Obtener categorías detectadas (usar el array o crear uno con la principal)
  const categories =
    post.categories?.length > 0
      ? post.categories
      : [{ name: post.category, confidence: post.confidence }];

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
        {/* Header con categorías detectadas */}
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "flex-start",
            marginBottom: "16px",
            flexWrap: "wrap",
            gap: "8px",
          }}
        >
          {/* Badges de categorías (múltiples) */}
          <div
            style={{ display: "flex", flexWrap: "wrap", gap: "8px", flex: 1 }}
          >
            {categories.map((cat, index) => {
              const catConfig = getCategoryConfig(cat.name);
              const isSecondary = index > 0;
              return (
                <div
                  key={cat.name}
                  style={{
                    display: "inline-flex",
                    alignItems: "center",
                    gap: "6px",
                    padding: isSecondary ? "5px 10px" : "8px 16px",
                    borderRadius: "30px",
                    backgroundColor: catConfig.bgColor,
                    color: catConfig.textColor,
                    fontWeight: isSecondary ? 600 : 700,
                    fontSize: isSecondary ? "0.65rem" : "0.75rem",
                    textTransform: "uppercase",
                    letterSpacing: "0.5px",
                    opacity: isSecondary ? 0.85 : 1,
                  }}
                >
                  <span style={{ fontSize: isSecondary ? "0.8rem" : "1rem" }}>
                    {catConfig.emoji}
                  </span>
                  <span>{cat.name}</span>
                  <span
                    style={{
                      fontSize: "0.6rem",
                      opacity: 0.7,
                      marginLeft: "2px",
                    }}
                  >
                    {Math.round(cat.confidence * 100)}%
                  </span>
                </div>
              );
            })}
          </div>

          {/* Indicador de confianza principal */}
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
