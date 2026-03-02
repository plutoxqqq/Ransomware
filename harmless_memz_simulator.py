"""High-intensity, harmless visual stress simulator.

This script opens many animated windows with rapid movement and flashing colors,
then exits automatically after five minutes.

Safety design:
- No destructive file, registry, process, network, or boot changes.
- No persistence or privilege escalation attempts.
- No cursor hijacking or input interception.
- Fully self-terminates after five minutes.
"""

from __future__ import annotations

import math
import random
import tkinter as tk
from dataclasses import dataclass
from time import monotonic

DURATION_SECONDS = 5 * 60
WINDOW_COUNT = 30
MIN_WINDOW_SIZE = 140
MAX_WINDOW_SIZE = 280
FRAME_DELAY_MS = 8  # ~125 FPS target for smoother animation.
STYLE_DELAY_MS = 85
MAX_SPEED = 16.0

MESSAGES = [
    "SYSTEM ALERT",
    "VISUAL OVERLOAD",
    "PROCESSING",
    "SIGNAL NOISE",
    "RAPID WINDOW EVENT",
    "BENIGN STRESS TEST",
    "AUTO-SHUTDOWN ENABLED",
]

COLORS = [
    "#FF0033",
    "#FF6A00",
    "#FFD400",
    "#00E676",
    "#00B0FF",
    "#5E35B1",
    "#D500F9",
    "#F50057",
    "#FFFFFF",
    "#000000",
]


@dataclass
class FloatingWindow:
    window: tk.Toplevel
    label: tk.Label
    x: float
    y: float
    vx: float
    vy: float
    width: int
    height: int
    phase: float

    def update(self, max_w: int, max_h: int, pulse: float) -> None:
        """Move the window with bounce physics and mild sinusoidal perturbation."""
        self.x += self.vx + math.sin(self.phase + pulse) * 0.9
        self.y += self.vy + math.cos(self.phase + pulse * 1.2) * 0.9

        if self.x <= 0:
            self.x = 0
            self.vx = abs(self.vx)
        elif self.x + self.width >= max_w:
            self.x = max(0, max_w - self.width)
            self.vx = -abs(self.vx)

        if self.y <= 0:
            self.y = 0
            self.vy = abs(self.vy)
        elif self.y + self.height >= max_h:
            self.y = max(0, max_h - self.height)
            self.vy = -abs(self.vy)

        self.window.geometry(f"{self.width}x{self.height}+{int(self.x)}+{int(self.y)}")


class HarmlessMemzSimulator:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.withdraw()
        self.root.title("Visual Stress Simulator")
        self.root.configure(bg="black")

        self.start_time = monotonic()
        self.windows: list[FloatingWindow] = []
        self.tick_count = 0

        self.screen_w = self.root.winfo_screenwidth()
        self.screen_h = self.root.winfo_screenheight()

        for _ in range(WINDOW_COUNT):
            self.windows.append(self._create_window())

        self.root.after(FRAME_DELAY_MS, self._tick)
        self.root.after(STYLE_DELAY_MS, self._shuffle_styles)

    def _create_window(self) -> FloatingWindow:
        width = random.randint(MIN_WINDOW_SIZE, MAX_WINDOW_SIZE)
        height = random.randint(MIN_WINDOW_SIZE, MAX_WINDOW_SIZE)

        x = random.uniform(0, max(1, self.screen_w - width))
        y = random.uniform(0, max(1, self.screen_h - height))
        vx = random.choice([-1, 1]) * random.uniform(7.5, 12.5)
        vy = random.choice([-1, 1]) * random.uniform(7.5, 12.5)

        top = tk.Toplevel(self.root)
        top.overrideredirect(False)
        top.attributes("-topmost", True)
        top.resizable(False, False)

        background = random.choice(COLORS)
        foreground = "black" if background in {"#FFFFFF", "#FFD400"} else "white"

        label = tk.Label(
            top,
            text=random.choice(MESSAGES),
            bg=background,
            fg=foreground,
            font=("Segoe UI", random.randint(11, 20), "bold"),
            justify="center",
            wraplength=width - 20,
        )
        label.pack(fill="both", expand=True)

        top.geometry(f"{width}x{height}+{int(x)}+{int(y)}")

        return FloatingWindow(
            window=top,
            label=label,
            x=x,
            y=y,
            vx=vx,
            vy=vy,
            width=width,
            height=height,
            phase=random.uniform(0.0, math.tau),
        )

    def _tick(self) -> None:
        elapsed = monotonic() - self.start_time
        if elapsed >= DURATION_SECONDS:
            self._shutdown()
            return

        self.tick_count += 1
        pulse = self.tick_count * 0.11

        for fw in self.windows:
            fw.update(self.screen_w, self.screen_h, pulse)

        self.root.after(FRAME_DELAY_MS, self._tick)

    def _shuffle_styles(self) -> None:
        elapsed = monotonic() - self.start_time
        if elapsed >= DURATION_SECONDS:
            return

        invert = random.random() < 0.4

        for fw in self.windows:
            # Flashing effect by frequent color inversions or random recolors.
            if invert:
                current_bg = str(fw.label.cget("bg"))
                current_fg = str(fw.label.cget("fg"))
                fw.label.configure(bg=current_fg, fg=current_bg)
            else:
                bg = random.choice(COLORS)
                fg = "black" if bg in {"#FFFFFF", "#FFD400"} else "white"
                fw.label.configure(bg=bg, fg=fg)

            if random.random() < 0.55:
                fw.label.configure(
                    text=random.choice(MESSAGES),
                    font=("Segoe UI", random.randint(10, 22), "bold"),
                )

            # Controlled jitter and acceleration to keep movement chaotic but stable.
            fw.vx += random.uniform(-1.2, 1.2)
            fw.vy += random.uniform(-1.2, 1.2)
            fw.vx = max(-MAX_SPEED, min(MAX_SPEED, fw.vx))
            fw.vy = max(-MAX_SPEED, min(MAX_SPEED, fw.vy))

        self.root.after(STYLE_DELAY_MS, self._shuffle_styles)

    def _shutdown(self) -> None:
        for fw in self.windows:
            try:
                fw.window.destroy()
            except tk.TclError:
                pass

        self.windows.clear()
        self.root.quit()
        self.root.destroy()


def main() -> None:
    root = tk.Tk()
    HarmlessMemzSimulator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
