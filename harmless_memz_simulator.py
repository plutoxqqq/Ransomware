"""Harmless MEMZ-style visual simulator.

This script creates many bouncing windows with randomized colors/messages,
then automatically exits after five minutes.

Safety design:
- No destructive file, registry, process, network, or boot changes.
- No persistence or privilege escalation attempts.
- Fully self-terminates after 5 minutes.
"""

from __future__ import annotations

import random
import tkinter as tk
from dataclasses import dataclass
from time import monotonic

DURATION_SECONDS = 5 * 60
WINDOW_COUNT = 24
MIN_WINDOW_SIZE = 140
MAX_WINDOW_SIZE = 280
FRAME_DELAY_MS = 16

MESSAGES = [
    "Harmless visual demo",
    "Bouncing window",
    "Simulation mode",
    "No system changes",
    "Auto-exits in 5 minutes",
    "Safe prank effect",
    "Visual payload (benign)",
]

COLORS = [
    "#FF3B30",
    "#FF9500",
    "#FFCC00",
    "#34C759",
    "#32ADE6",
    "#5856D6",
    "#AF52DE",
    "#FF2D55",
    "#FFFFFF",
    "#E5E5EA",
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

    def update(self, max_w: int, max_h: int) -> None:
        self.x += self.vx
        self.y += self.vy

        if self.x <= 0:
            self.x = 0
            self.vx *= -1
        elif self.x + self.width >= max_w:
            self.x = max(0, max_w - self.width)
            self.vx *= -1

        if self.y <= 0:
            self.y = 0
            self.vy *= -1
        elif self.y + self.height >= max_h:
            self.y = max(0, max_h - self.height)
            self.vy *= -1

        self.window.geometry(f"{self.width}x{self.height}+{int(self.x)}+{int(self.y)}")


class HarmlessMemzSimulator:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.withdraw()
        self.root.title("Harmless MEMZ Simulator")
        self.root.configure(bg="black")

        self.start_time = monotonic()
        self.windows: list[FloatingWindow] = []

        self.screen_w = self.root.winfo_screenwidth()
        self.screen_h = self.root.winfo_screenheight()

        for _ in range(WINDOW_COUNT):
            self.windows.append(self._create_window())

        self.root.after(FRAME_DELAY_MS, self._tick)
        self.root.after(350, self._shuffle_styles)

    def _create_window(self) -> FloatingWindow:
        width = random.randint(MIN_WINDOW_SIZE, MAX_WINDOW_SIZE)
        height = random.randint(MIN_WINDOW_SIZE, MAX_WINDOW_SIZE)

        x = random.uniform(0, max(1, self.screen_w - width))
        y = random.uniform(0, max(1, self.screen_h - height))
        vx = random.choice([-1, 1]) * random.uniform(2.2, 7.5)
        vy = random.choice([-1, 1]) * random.uniform(2.2, 7.5)

        top = tk.Toplevel(self.root)
        top.overrideredirect(False)
        top.attributes("-topmost", True)
        top.resizable(False, False)

        background = random.choice(COLORS)
        foreground = "black" if background in {"#FFFFFF", "#E5E5EA", "#FFCC00"} else "white"

        label = tk.Label(
            top,
            text=random.choice(MESSAGES),
            bg=background,
            fg=foreground,
            font=("Segoe UI", random.randint(11, 16), "bold"),
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
        )

    def _tick(self) -> None:
        elapsed = monotonic() - self.start_time
        if elapsed >= DURATION_SECONDS:
            self._shutdown()
            return

        for fw in self.windows:
            fw.update(self.screen_w, self.screen_h)

        self.root.after(FRAME_DELAY_MS, self._tick)

    def _shuffle_styles(self) -> None:
        elapsed = monotonic() - self.start_time
        if elapsed >= DURATION_SECONDS:
            return

        for fw in self.windows:
            if random.random() < 0.45:
                bg = random.choice(COLORS)
                fg = "black" if bg in {"#FFFFFF", "#E5E5EA", "#FFCC00"} else "white"
                fw.label.configure(
                    text=random.choice(MESSAGES),
                    bg=bg,
                    fg=fg,
                    font=("Segoe UI", random.randint(10, 18), "bold"),
                )

            if random.random() < 0.25:
                fw.vx += random.uniform(-0.8, 0.8)
                fw.vy += random.uniform(-0.8, 0.8)
                fw.vx = max(-10.0, min(10.0, fw.vx))
                fw.vy = max(-10.0, min(10.0, fw.vy))

        self.root.after(350, self._shuffle_styles)

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
