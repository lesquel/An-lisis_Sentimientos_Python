// Categorías disponibles para los botones de filtro (25 categorías + Todas)
export const CATEGORIES = [
  "Todas",
  // Emociones básicas
  "Alegría",
  "Tristeza",
  "Enojo",
  "Miedo",
  "Sorpresa",
  "Asco",
  // Emociones sociales
  "Amor",
  "Odio",
  "Vergüenza",
  "Orgullo",
  "Envidia",
  "Celos",
  // Tipos de contenido
  "Humor",
  "Inspiración",
  "Confesión",
  "Queja",
  "Consejo",
  "Pregunta",
  "Reflexión",
  "Nostalgia",
  "Ansiedad",
  "Frustración",
  // Contenido especial
  "Sarcasmo",
  "Polémica",
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
  // Emociones básicas
  Alegría: {
    emoji: "😊",
    bgColor: "#fef3c7",
    textColor: "#92400e",
    borderColor: "#fbbf24",
    lightBg: "#fffbeb",
  },
  Tristeza: {
    emoji: "😢",
    bgColor: "#dbeafe",
    textColor: "#1e40af",
    borderColor: "#60a5fa",
    lightBg: "#eff6ff",
  },
  Enojo: {
    emoji: "😠",
    bgColor: "#fee2e2",
    textColor: "#991b1b",
    borderColor: "#f87171",
    lightBg: "#fef2f2",
  },
  Miedo: {
    emoji: "😨",
    bgColor: "#e2e8f0",
    textColor: "#1e293b",
    borderColor: "#64748b",
    lightBg: "#f1f5f9",
  },
  Sorpresa: {
    emoji: "😲",
    bgColor: "#cffafe",
    textColor: "#0e7490",
    borderColor: "#22d3ee",
    lightBg: "#ecfeff",
  },
  Asco: {
    emoji: "🤢",
    bgColor: "#ecfccb",
    textColor: "#3f6212",
    borderColor: "#a3e635",
    lightBg: "#f7fee7",
  },
  // Emociones sociales
  Amor: {
    emoji: "❤️",
    bgColor: "#fce7f3",
    textColor: "#9d174d",
    borderColor: "#f472b6",
    lightBg: "#fdf2f8",
  },
  Odio: {
    emoji: "🔴",
    bgColor: "#fee2e2",
    textColor: "#7f1d1d",
    borderColor: "#ef4444",
    lightBg: "#fef2f2",
  },
  Vergüenza: {
    emoji: "😳",
    bgColor: "#fce7f3",
    textColor: "#831843",
    borderColor: "#ec4899",
    lightBg: "#fdf2f8",
  },
  Orgullo: {
    emoji: "🦁",
    bgColor: "#fef3c7",
    textColor: "#78350f",
    borderColor: "#f59e0b",
    lightBg: "#fffbeb",
  },
  Envidia: {
    emoji: "👀",
    bgColor: "#d1fae5",
    textColor: "#064e3b",
    borderColor: "#10b981",
    lightBg: "#ecfdf5",
  },
  Celos: {
    emoji: "💚",
    bgColor: "#dcfce7",
    textColor: "#166534",
    borderColor: "#22c55e",
    lightBg: "#f0fdf4",
  },
  // Tipos de contenido
  Humor: {
    emoji: "😂",
    bgColor: "#fef9c3",
    textColor: "#854d0e",
    borderColor: "#facc15",
    lightBg: "#fefce8",
  },
  Inspiración: {
    emoji: "✨",
    bgColor: "#d1fae5",
    textColor: "#065f46",
    borderColor: "#34d399",
    lightBg: "#ecfdf5",
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
  Consejo: {
    emoji: "💡",
    bgColor: "#fef3c7",
    textColor: "#92400e",
    borderColor: "#fbbf24",
    lightBg: "#fffbeb",
  },
  Pregunta: {
    emoji: "❓",
    bgColor: "#cffafe",
    textColor: "#0e7490",
    borderColor: "#22d3ee",
    lightBg: "#ecfeff",
  },
  Reflexión: {
    emoji: "🤔",
    bgColor: "#ede9fe",
    textColor: "#5b21b6",
    borderColor: "#a78bfa",
    lightBg: "#f5f3ff",
  },
  Nostalgia: {
    emoji: "🌅",
    bgColor: "#ffedd5",
    textColor: "#9a3412",
    borderColor: "#fb923c",
    lightBg: "#fff7ed",
  },
  Ansiedad: {
    emoji: "😰",
    bgColor: "#e0e7ff",
    textColor: "#3730a3",
    borderColor: "#818cf8",
    lightBg: "#eef2ff",
  },
  Frustración: {
    emoji: "😩",
    bgColor: "#fee2e2",
    textColor: "#b91c1c",
    borderColor: "#f87171",
    lightBg: "#fef2f2",
  },
  Sarcasmo: {
    emoji: "😏",
    bgColor: "#fef3c7",
    textColor: "#78350f",
    borderColor: "#f59e0b",
    lightBg: "#fffbeb",
  },
  Polémica: {
    emoji: "🔥",
    bgColor: "#ffedd5",
    textColor: "#9a3412",
    borderColor: "#fb923c",
    lightBg: "#fff7ed",
  },
  Terror: {
    emoji: "👻",
    bgColor: "#e2e8f0",
    textColor: "#1e293b",
    borderColor: "#64748b",
    lightBg: "#f1f5f9",
  },
  // Mantener compatibilidad con categorías antiguas
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
  Curiosidad: {
    emoji: "🧐",
    bgColor: "#cffafe",
    textColor: "#0e7490",
    borderColor: "#22d3ee",
    lightBg: "#ecfeff",
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
  // Nuevas categorías
  Alegría: "bg-yellow-100 text-yellow-800 border-yellow-400",
  Tristeza: "bg-blue-100 text-blue-800 border-blue-400",
  Enojo: "bg-red-100 text-red-800 border-red-400",
  Miedo: "bg-slate-100 text-slate-800 border-slate-400",
  Sorpresa: "bg-cyan-100 text-cyan-800 border-cyan-400",
  Asco: "bg-lime-100 text-lime-800 border-lime-400",
  Amor: "bg-pink-100 text-pink-800 border-pink-400",
  Odio: "bg-red-200 text-red-900 border-red-500",
  Vergüenza: "bg-pink-100 text-pink-800 border-pink-400",
  Orgullo: "bg-amber-100 text-amber-800 border-amber-400",
  Envidia: "bg-emerald-100 text-emerald-800 border-emerald-400",
  Celos: "bg-green-100 text-green-800 border-green-400",
  Humor: "bg-yellow-100 text-yellow-800 border-yellow-400",
  Inspiración: "bg-green-100 text-green-800 border-green-400",
  Confesión: "bg-indigo-100 text-indigo-800 border-indigo-400",
  Queja: "bg-gray-100 text-gray-800 border-gray-400",
  Consejo: "bg-amber-100 text-amber-800 border-amber-400",
  Pregunta: "bg-cyan-100 text-cyan-800 border-cyan-400",
  Reflexión: "bg-purple-100 text-purple-800 border-purple-400",
  Nostalgia: "bg-orange-100 text-orange-800 border-orange-400",
  Ansiedad: "bg-indigo-100 text-indigo-800 border-indigo-400",
  Frustración: "bg-red-100 text-red-800 border-red-400",
  Sarcasmo: "bg-amber-100 text-amber-800 border-amber-400",
  Polémica: "bg-orange-100 text-orange-800 border-orange-400",
  Terror: "bg-slate-100 text-slate-800 border-slate-400",
  // Categorías antiguas para compatibilidad
  Tóxico: "bg-red-100 text-red-800 border-red-400",
  Gracioso: "bg-yellow-100 text-yellow-800 border-yellow-400",
  Inspirador: "bg-green-100 text-green-800 border-green-400",
  Triste: "bg-blue-100 text-blue-800 border-blue-400",
  Romántico: "bg-pink-100 text-pink-800 border-pink-400",
  Asqueroso: "bg-lime-100 text-lime-800 border-lime-400",
  Filosófico: "bg-purple-100 text-purple-800 border-purple-400",
  Curiosidad: "bg-cyan-100 text-cyan-800 border-cyan-400",
};

export const getCategoryColor = (category: string): string => {
  return (
    CATEGORY_COLORS[category] ||
    "bg-indigo-100 text-indigo-800 border-indigo-400"
  );
};
