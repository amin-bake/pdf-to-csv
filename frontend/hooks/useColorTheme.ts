"use client";

import { useEffect, useState } from "react";

export type ColorTheme = "earthy-forest" | "cherry-blossom" | "pastel-rainbow";

const COLOR_THEME_KEY = "color-theme";

export function useColorTheme() {
  const [colorTheme, setColorThemeState] =
    useState<ColorTheme>("earthy-forest");
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    const stored = localStorage.getItem(COLOR_THEME_KEY) as ColorTheme;
    if (
      stored &&
      (stored === "earthy-forest" ||
        stored === "cherry-blossom" ||
        stored === "pastel-rainbow")
    ) {
      setColorThemeState(stored);
      document.documentElement.setAttribute("data-color-theme", stored);
    }
  }, []);

  const setColorTheme = (theme: ColorTheme) => {
    setColorThemeState(theme);
    localStorage.setItem(COLOR_THEME_KEY, theme);
    document.documentElement.setAttribute("data-color-theme", theme);
  };

  return {
    colorTheme,
    setColorTheme,
    mounted,
  };
}
