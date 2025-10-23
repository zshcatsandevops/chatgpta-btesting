#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# 🕊️ Pelican Rider 3D – Project M Edition
# [C] 2025 Samsoft / FlamesCo Labs
# ---------------------------------------------------------------------------
# 600×400 Tkinter render
# Smash-Ball background • Trophy spin • About page toggle (A)
# ---------------------------------------------------------------------------

import tkinter as tk
import math, time, random

W, H = 600, 400
mode = "TROPHY"

root = tk.Tk()
root.title("🕊️ Pelican Rider 3D — Project M Edition")
root.resizable(False, False)
canvas = tk.Canvas(root, width=W, height=H, bg="#0c0f1a", highlightthickness=0)
canvas.pack()

# --- 3D projection -----------------------------------------------------------
def project(x, y, z):
    scale = 200 / (z + 300)
    return W//2 + int(x * scale), H//2 - int(y * scale)

# --- Smash-Ball BG -----------------------------------------------------------
def draw_smash_ball(t):
    cx, cy = W//2, H//2
    # rotating radial burst
    for i in range(12):
        a = t*0.8 + i*math.pi/6
        x1 = cx + math.cos(a) * 200
        y1 = cy + math.sin(a) * 200
        col = f"#{int(128+127*math.sin(a)):02x}44ff"
        canvas.create_line(cx, cy, x1, y1, fill=col, width=2)
    # central pulse
    r = 80 + 10*math.sin(t*2)
    canvas.create_oval(cx-r, cy-r, cx+r, cy+r, outline="#5588ff", width=4)
    canvas.create_oval(cx-r+5, cy-r+5, cx+r-5, cy+r-5,
                       outline="#bb88ff", width=2)

# --- Trophy draw -------------------------------------------------------------
def draw_pelican_bike(t):
    z_shift = math.sin(t * 1.2) * 40
    # pedestal
    canvas.create_oval(W//2-100, H//2+100, W//2+100, H//2+140,
                       fill="#2b2b40", outline="#8888cc", width=3)
    canvas.create_oval(W//2-90, H//2+95, W//2+90, H//2+135,
                       fill="#3e3e60", outline="#aac", width=1)
    # bike wheels
    for dx in (-60, 60):
        x, y = project(dx, -30, z_shift)
        r = 30
        for i in range(8):
            a = t*8 + i*math.pi/4
            x1 = x + math.cos(a)*r
            y1 = y + math.sin(a)*r
            canvas.create_line(x, y, x1, y1, fill="#ccccff", width=2)
        canvas.create_oval(x-r, y-r, x+r, y+r, outline="#333366", width=2, fill="#1a1a33")
    # frame
    x1, y1 = project(-60, -30, z_shift)
    x2, y2 = project(60, -30, z_shift)
    x3, y3 = project(0, 10, z_shift)
    canvas.create_line(x1, y1, x3, y3, fill="#66c", width=4)
    canvas.create_line(x3, y3, x2, y2, fill="#66c", width=4)
    canvas.create_line(x1, y1, x2, y2, fill="#99f", width=2)
    # pelican
    bx, by = project(0, -100, z_shift)
    canvas.create_oval(bx-40, by-20, bx+40, by+20, fill="#fff8ee", outline="#222")
    canvas.create_polygon(bx+40, by, bx+70, by+10, bx+70, by-10,
                          fill="#ffcc33", outline="#222")
    wing_offset = int(math.sin(t*6)*20)
    canvas.create_polygon(bx-10, by-10, bx-90, by-30+wing_offset,
                          bx-20, by-20, fill="#dddddd", outline="#222")
    canvas.create_polygon(bx+10, by-10, bx+90, by-30-wing_offset,
                          bx+20, by-20, fill="#dddddd", outline="#222")
    canvas.create_oval(bx+25, by-10, bx+32, by-3, fill="#000")
    # aura fade
    aura_colors = ["#99ccff", "#7788ff", "#aa99ff", "#88bbff", "#99aaff"]
    for i, col in enumerate(aura_colors):
        r = 160 + math.sin(t*2+i)*10
        canvas.create_oval(W//2-r, H//2-r, W//2+r, H//2+r,
                           outline=col, width=2)

# --- About page --------------------------------------------------------------
def draw_about_page():
    canvas.create_rectangle(0, 0, W, H, fill="#121425", outline="")
    canvas.create_text(W//2, 50, text="PROJECT M TROPHY DATA",
                       fill="#66aaff", font=("Impact", 22))
    canvas.create_text(W//2, 100, text="🕊 Pelican Rider 3D (Assist Trophy)",
                       fill="#e0e0ff", font=("Segoe UI Semibold", 14))
    desc = (
        "A mysterious coastal courier who defies gravity.\n"
        "Summoned from the skies, it delivers a surge of wind\n"
        "that launches nearby fighters upward.\n\n"
        "• Origin : Ultra Smash Universe\n"
        "• Category : Support Spirit / Flight\n"
        "• Debut : FlamesCo OS 1.0"
    )
    canvas.create_text(W//2, H//2, text=desc, fill="#ccccff",
                       font=("Consolas", 11), justify="center")
    canvas.create_text(W//2, H-35, text="Press A to Return to Trophy",
                       fill="#66aaff", font=("Segoe UI", 10, "italic"))

# --- Main loop ---------------------------------------------------------------
start = time.time()
fade = 0.0

def update():
    global fade
    t = time.time() - start
    canvas.delete("all")

    if mode == "TROPHY":
        draw_smash_ball(t)
        draw_pelican_bike(t)
        fade = min(1.0, fade + 0.02)
        overlay = int(255 * (1 - fade))
        if overlay > 0:
            canvas.create_rectangle(0, 0, W, H,
                                    fill=f"#{overlay:02x}{overlay:02x}{overlay:02x}",
                                    outline="")
        canvas.create_text(W//2, 30, text="Pelican Rider 3D — Assist Trophy",
                           fill="#aaccff", font=("Segoe UI Bold", 14))
        canvas.create_text(W//2, H-25, text="Press A for About Page",
                           fill="#88aaff", font=("Segoe UI", 10, "italic"))
    else:
        draw_about_page()
        fade = 0.0

    root.after(33, update)

# --- Toggle ---------------------------------------------------------------
def toggle_mode(event):
    global mode
    mode = "ABOUT" if mode == "TROPHY" else "TROPHY"

root.bind("a", toggle_mode)
root.bind("A", toggle_mode)

update()
root.mainloop()
