// src/utils/localData.js
// Helper to read JSON data from localStorage with fallback defaults
export const getLocalJSON = (key, defaultValue) => {
  try {
    const raw = localStorage.getItem(key);
    if (!raw) return defaultValue;
    return JSON.parse(raw);
  } catch (e) {
    console.warn(`Failed to parse localStorage key ${key}:`, e);
    return defaultValue;
  }
};
