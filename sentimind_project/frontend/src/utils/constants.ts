// Categorías disponibles para los botones de filtro
export const CATEGORIES = [
  "Todas",
  "Tóxico",
  "Gracioso",
  "Inspirador",
  "Triste",
  "Romántico",
  "Polémico",
  "Asqueroso",
  "Filosófico",
  "Confesión",
  "Queja",
  "Curiosidad",
  "Terror",
];

// Configuración de colores y emojis para cada categoría
export interface CategoryConfig {
  emoji: string;
  bgColor: string;
  textColor: string;
  borderColor: string;
  lightBg: string;
}

export const CATEGORY_CONFIG: Record<string, CategoryConfig> = {
  Tóxico: {
    emoji: "🔴",
    bgColor: "#fee2e2",
    textColor: "#991b1b",
    borderColor: "#f87171",
    lightBg: "#fef2f2",
  },
  Gracioso: {
    emoji: "😂",
    bgColor: "#fef3c7",
    textColor: "#92400e",
    borderColor: "#fbbf24",
    lightBg: "#fffbeb",
  },
  Inspirador: {
    emoji: "✨",
    bgColor: "#d1fae5",
    textColor: "#065f46",
    borderColor: "#34d399",
    lightBg: "#ecfdf5",
  },
  Triste: {
    emoji: "💔",
    bgColor: "#dbeafe",
    textColor: "#1e40af",
    borderColor: "#60a5fa",
    lightBg: "#eff6ff",
  },
  Romántico: {
    emoji: "💕",
    bgColor: "#fce7f3",
    textColor: "#9d174d",
    borderColor: "#f472b6",
    lightBg: "#fdf2f8",
  },
  Polémico: {
    emoji: "🔥",
    bgColor: "#ffedd5",
    textColor: "#9a3412",
    borderColor: "#fb923c",
    lightBg: "#fff7ed",
  },
  Asqueroso: {
    emoji: "🤢",
    bgColor: "#ecfccb",
    textColor: "#3f6212",
    borderColor: "#a3e635",
    lightBg: "#f7fee7",
  },
  Filosófico: {
    emoji: "🤔",
    bgColor: "#ede9fe",
    textColor: "#5b21b6",
    borderColor: "#a78bfa",
    lightBg: "#f5f3ff",
  },
  Confesión: {
    emoji: "🤫",
    bgColor: "#e0e7ff",
    textColor: "#3730a3",
    borderColor: "#818cf8",
    lightBg: "#eef2ff",
  },
  Queja: {
    emoji: "😤",
    bgColor: "#f1f5f9",
    textColor: "#334155",
    borderColor: "#94a3b8",
    lightBg: "#f8fafc",
  },
  Curiosidad: {
    emoji: "🧐",
    bgColor: "#cffafe",
    textColor: "#0e7490",
    borderColor: "#22d3ee",
    lightBg: "#ecfeff",
  },
  Terror: {
    emoji: "👻",
    bgColor: "#e2e8f0",
    textColor: "#1e293b",
    borderColor: "#64748b",
    lightBg: "#f1f5f9",
  },
};

export const getCategoryConfig = (category: string): CategoryConfig => {
  return (
    CATEGORY_CONFIG[category] || {
      emoji: "📝",
      bgColor: "#e0e7ff",
      textColor: "#3730a3",
      borderColor: "#818cf8",
      lightBg: "#eef2ff",
    }
  );
};

// Mantener compatibilidad con código anterior
export const CATEGORY_COLORS: Record<string, string> = {
  Tóxico: "bg-red-100 text-red-800 border-red-400",
  Gracioso: "bg-yellow-100 text-yellow-800 border-yellow-400",
  Inspirador: "bg-green-100 text-green-800 border-green-400",
  Triste: "bg-blue-100 text-blue-800 border-blue-400",
  Romántico: "bg-pink-100 text-pink-800 border-pink-400",
  Polémico: "bg-orange-100 text-orange-800 border-orange-400",
  Asqueroso: "bg-lime-100 text-lime-800 border-lime-400",
  Filosófico: "bg-purple-100 text-purple-800 border-purple-400",
  Confesión: "bg-indigo-100 text-indigo-800 border-indigo-400",
  Queja: "bg-gray-100 text-gray-800 border-gray-400",
  Curiosidad: "bg-cyan-100 text-cyan-800 border-cyan-400",
  Terror: "bg-slate-100 text-slate-800 border-slate-400",
};

export const getCategoryColor = (category: string): string => {
  return (
    CATEGORY_COLORS[category] ||
    "bg-indigo-100 text-indigo-800 border-indigo-400"
  );
};
