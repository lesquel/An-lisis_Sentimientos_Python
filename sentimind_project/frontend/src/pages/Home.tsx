import { usePosts } from "../hooks/usePosts";
import PostCard from "../components/PostCard";
import PostInput from "../components/PostInput";
import FilterBar from "../components/FilterBar";

export default function Home() {
  const { posts, loading, error, filter, setFilter, addPost } = usePosts();

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        padding: "20px",
      }}
    >
      {/* Contenedor principal */}
      <div
        style={{
          maxWidth: "1200px",
          margin: "0 auto",
        }}
      >
        {/* ========== HEADER ========== */}
        <header
          style={{
            textAlign: "center",
            marginBottom: "40px",
            paddingTop: "20px",
          }}
        >
          {/* Logo animado */}
          <div
            className="animate-float"
            style={{
              width: "100px",
              height: "100px",
              margin: "0 auto 20px",
              background: "white",
              borderRadius: "30px",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: "50px",
              boxShadow: "0 20px 60px rgba(0, 0, 0, 0.3)",
            }}
          >
            🧠
          </div>

          {/* Título */}
          <h1
            style={{
              fontSize: "clamp(2rem, 5vw, 3.5rem)",
              fontWeight: 800,
              color: "white",
              marginBottom: "10px",
              textShadow: "0 4px 20px rgba(0, 0, 0, 0.3)",
            }}
          >
            Sentimind Network
          </h1>

          {/* Subtítulo */}
          <p
            style={{
              fontSize: "1.1rem",
              color: "rgba(255, 255, 255, 0.9)",
              marginBottom: "20px",
            }}
          >
            Red social con clasificación automática por Inteligencia Artificial
          </p>

          {/* Badges de tecnología */}
          <div
            style={{
              display: "flex",
              justifyContent: "center",
              gap: "10px",
              flexWrap: "wrap",
            }}
          >
            {[
              { icon: "🔬", text: "Minería de Datos" },
              { icon: "🎯", text: "Zero-Shot AI" },
              { icon: "🤖", text: "Transformers" },
            ].map((badge, i) => (
              <span
                key={i}
                style={{
                  background: "rgba(255, 255, 255, 0.2)",
                  backdropFilter: "blur(10px)",
                  color: "white",
                  padding: "8px 16px",
                  borderRadius: "30px",
                  fontSize: "0.85rem",
                  fontWeight: 500,
                  display: "flex",
                  alignItems: "center",
                  gap: "6px",
                }}
              >
                <span>{badge.icon}</span>
                {badge.text}
              </span>
            ))}
          </div>
        </header>

        {/* ========== ÁREA DE INPUT ========== */}
        <PostInput onSubmit={addPost} loading={loading} />

        {/* ========== MENSAJE DE ERROR ========== */}
        {error && (
          <div
            className="animate-fade-in"
            style={{
              background: "#fef2f2",
              border: "2px solid #fecaca",
              borderRadius: "16px",
              padding: "16px 20px",
              marginBottom: "24px",
              display: "flex",
              alignItems: "center",
              gap: "12px",
              color: "#dc2626",
            }}
          >
            <span style={{ fontSize: "24px" }}>⚠️</span>
            <span style={{ fontWeight: 500 }}>{error}</span>
          </div>
        )}

        {/* ========== BARRA DE FILTROS ========== */}
        <FilterBar currentFilter={filter} onFilterChange={setFilter} />

        {/* ========== ESTADÍSTICAS ========== */}
        <div
          style={{
            textAlign: "center",
            marginBottom: "24px",
          }}
        >
          <div
            style={{
              display: "inline-block",
              background: "rgba(255, 255, 255, 0.2)",
              backdropFilter: "blur(10px)",
              padding: "12px 24px",
              borderRadius: "30px",
              color: "white",
              fontSize: "0.9rem",
            }}
          >
            {filter ? (
              <>
                📊 Mostrando <strong>{posts.length}</strong> posts de{" "}
                <strong>{filter}</strong>
              </>
            ) : (
              <>
                📊 Mostrando <strong>{posts.length}</strong> posts totales
              </>
            )}
          </div>
        </div>

        {/* ========== GRID DE POSTS ========== */}
        {loading && posts.length === 0 ? (
          <div
            style={{
              background: "rgba(255, 255, 255, 0.95)",
              borderRadius: "24px",
              padding: "60px 20px",
              textAlign: "center",
              boxShadow: "0 20px 60px rgba(0, 0, 0, 0.2)",
            }}
          >
            <div
              className="animate-spin"
              style={{
                width: "60px",
                height: "60px",
                margin: "0 auto 20px",
                border: "4px solid #e5e7eb",
                borderTop: "4px solid #667eea",
                borderRadius: "50%",
              }}
            />
            <p
              style={{
                fontSize: "1.2rem",
                fontWeight: 600,
                color: "#374151",
                marginBottom: "8px",
              }}
            >
              Cargando posts...
            </p>
            <p style={{ color: "#9ca3af" }}>Conectando con la IA</p>
          </div>
        ) : posts.length === 0 ? (
          <div
            style={{
              background: "rgba(255, 255, 255, 0.95)",
              borderRadius: "24px",
              padding: "60px 20px",
              textAlign: "center",
              boxShadow: "0 20px 60px rgba(0, 0, 0, 0.2)",
            }}
          >
            <div style={{ fontSize: "80px", marginBottom: "20px" }}>📝</div>
            <p
              style={{
                fontSize: "1.5rem",
                fontWeight: 600,
                color: "#374151",
                marginBottom: "8px",
              }}
            >
              No hay posts aún
            </p>
            <p style={{ color: "#9ca3af", fontSize: "1rem" }}>
              ¡Sé el primero en publicar algo y ver la magia de la IA!
            </p>
          </div>
        ) : (
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fill, minmax(350px, 1fr))",
              gap: "24px",
            }}
          >
            {posts.map((post, index) => (
              <div
                key={post.id}
                className="animate-fade-in-up"
                style={{ animationDelay: `${index * 0.05}s` }}
              >
                <PostCard post={post} />
              </div>
            ))}
          </div>
        )}

        {/* ========== FOOTER ========== */}
        <footer
          style={{
            textAlign: "center",
            marginTop: "60px",
            paddingBottom: "40px",
          }}
        >
          <div
            style={{
              display: "inline-block",
              background: "rgba(255, 255, 255, 0.15)",
              backdropFilter: "blur(10px)",
              padding: "24px 40px",
              borderRadius: "20px",
            }}
          >
            <p
              style={{
                color: "rgba(255, 255, 255, 0.9)",
                marginBottom: "12px",
                fontWeight: 500,
              }}
            >
              Desarrollado con ❤️ para ULEAM
            </p>
            <div
              style={{
                display: "flex",
                justifyContent: "center",
                gap: "10px",
                flexWrap: "wrap",
              }}
            >
              {["Django", "React", "🤗 Hugging Face", "uv"].map((tech, i) => (
                <span
                  key={i}
                  style={{
                    background: "rgba(255, 255, 255, 0.2)",
                    color: "white",
                    padding: "6px 14px",
                    borderRadius: "20px",
                    fontSize: "0.8rem",
                    fontWeight: 500,
                  }}
                >
                  {tech}
                </span>
              ))}
            </div>
            <p
              style={{
                color: "rgba(255, 255, 255, 0.6)",
                fontSize: "0.75rem",
                marginTop: "12px",
              }}
            >
              Modelo: facebook/bart-large-mnli | Arquitectura Hexagonal
            </p>
          </div>
        </footer>
      </div>
    </div>
  );
}
