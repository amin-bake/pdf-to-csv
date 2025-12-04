"use client";

import * as React from "react";
import { Check, Palette } from "lucide-react";
import { useColorTheme, type ColorTheme } from "@/hooks/useColorTheme";

import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger
} from "@/components/ui/dropdown-menu";

const COLOR_THEMES: {
  value: ColorTheme;
  label: string;
  description: string;
}[] = [
  {
    value: "earthy-forest",
    label: "Earthy Forest",
    description: "Calm greens and earth tones",
  },
  {
    value: "cherry-blossom",
    label: "Cherry Blossom Bloom",
    description: "Vibrant reds and soft pinks",
  },
  {
    value: "pastel-rainbow",
    label: "Pastel Rainbow Fantasy",
    description: "Dreamy pastels and rainbow hues",
  },
];

export function ColorThemeSelector() {
  const { colorTheme, setColorTheme, mounted } = useColorTheme();

  if (!mounted) {
    return (
      <Button variant="outline" size="icon" disabled>
        <Palette className="h-[1.2rem] w-[1.2rem]" />
        <span className="sr-only">Select color theme</span>
      </Button>
    );
  }

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button
          variant="outline"
          size="icon"
          className="relative overflow-hidden cursor-pointer group"
        >
          <Palette className="h-[1.2rem] w-[1.2rem] text-primary group-hover:text-white transition-colors" />
          <span className="sr-only">Select color theme</span>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-56">
        {COLOR_THEMES.map((theme) => (
          <DropdownMenuItem
            key={theme.value}
            onClick={() => setColorTheme(theme.value)}
            className="cursor-pointer flex flex-col items-start gap-1 py-2"
          >
            <div className="flex items-center justify-between w-full">
              <span className="font-medium">{theme.label}</span>
              {colorTheme === theme.value && (
                <Check className="h-4 w-4 text-primary" />
              )}
            </div>
            <span className="text-xs text-muted-foreground">
              {theme.description}
            </span>
          </DropdownMenuItem>
        ))}
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
