import { useState } from "react";
import { CATEGORIES, getCategoryConfig } from "../utils/constants";

interface FilterBarProps {
  currentFilter: string | null;
  onFilterChange: (filter: string | null) => void;
}

export default function FilterBar({
  currentFilter,
  onFilterChange,
}: FilterBarProps) {
  const [hoveredCat, setHoveredCat] = useState<string | null>(null);

  return (
    <div
      style={{
        background: "rgba(255, 255, 255, 0.95)",
        borderRadius: "20px",
        padding: "24px",
        marginBottom: "24px",
        boxShadow: "0 10px 40px rgba(0, 0, 0, 0.12)",
      }}
    >
      {/* Título */}
      <div
        style={{
          textAlign: "center",
          marginBottom: "16px",
        }}
      >
        <span
          style={{
            fontSize: "0.75rem",
            fontWeight: 700,
            color: "#6b7280",
            textTransform: "uppercase",
            letterSpacing: "2px",
          }}
        >
          🎯 Filtrar por categoría
        </span>
      </div>

      {/* Botones de filtro */}
      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "center",
          gap: "10px",
        }}
      >
        {CATEGORIES.map((cat) => {
          const isActive =
            currentFilter === cat || (cat === "Todas" && !currentFilter);
          const isHovered = hoveredCat === cat;
          const config = getCategoryConfig(cat);

          return (
            <button
              key={cat}
              onClick={() => onFilterChange(cat === "Todas" ? null : cat)}
              onMouseEnter={() => setHoveredCat(cat)}
              onMouseLeave={() => setHoveredCat(null)}
              style={{
                display: "flex",
                alignItems: "center",
                gap: "6px",
                padding: "10px 18px",
                fontSize: "0.875rem",
                fontWeight: 600,
                border: "none",
                borderRadius: "30px",
                cursor: "pointer",
                transition: "all 0.2s ease",
                background: isActive
                  ? cat === "Todas"
                    ? "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
                    : config.borderColor
                  : isHovered
                  ? "#f3f4f6"
                  : "white",
                color: isActive ? "white" : "#4b5563",
                boxShadow: isActive
                  ? "0 6px 20px rgba(0, 0, 0, 0.2)"
                  : "0 2px 8px rgba(0, 0, 0, 0.08)",
                transform: isActive
                  ? "scale(1.05)"
                  : isHovered
                  ? "scale(1.02)"
                  : "scale(1)",
              }}
            >
              {cat !== "Todas" && (
                <span style={{ fontSize: "1rem" }}>{config.emoji}</span>
              )}
              {cat === "Todas" && <span style={{ fontSize: "1rem" }}>🌐</span>}
              <span>{cat}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
