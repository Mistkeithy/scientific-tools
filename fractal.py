#!/usr/bin/python

import tkinter as tk

def draw_H_mm(canvas, x_mm, y_mm, size_mm, width_mm, level, s, cx, cy):
    if level == 0:
        return
    x1 = cx + (x_mm - size_mm/2) * s
    x2 = cx + (x_mm + size_mm/2) * s
    y1 = cy + (y_mm - size_mm/2) * s
    y2 = cy + (y_mm + size_mm/2) * s
    ym = cy + y_mm * s
    width_pixels = width_mm * s
    canvas.create_line(x1, y1, x1, y2, width=width_pixels, tags="fractal")
    canvas.create_line(x2, y1, x2, y2, width=width_pixels, tags="fractal")
    canvas.create_line(x1, ym, x2, ym, width=width_pixels, tags="fractal")
    draw_H_mm(canvas, x_mm - size_mm/2, y_mm - size_mm/2, size_mm / 2, width_mm / 2, level - 1, s, cx, cy)
    draw_H_mm(canvas, x_mm - size_mm/2, y_mm + size_mm/2, size_mm / 2, width_mm / 2, level - 1, s, cx, cy)
    draw_H_mm(canvas, x_mm + size_mm/2, y_mm - size_mm/2, size_mm / 2, width_mm / 2, level - 1, s, cx, cy)
    draw_H_mm(canvas, x_mm + size_mm/2, y_mm + size_mm/2, size_mm / 2, width_mm / 2, level - 1, s, cx, cy)

def draw_all():
    canvas.delete("all")
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    width_mm = size_mm * (2 - 2**(1 - level))
    s = z * min(canvas_width / width_mm, canvas_height / width_mm)
    cx = canvas_width / 2
    cy = canvas_height / 2
    initial_width_mm = size_mm / 20
    draw_H_mm(canvas, 0, 0, size_mm, initial_width_mm, level, s, cx, cy)
    scale_length_mm = 10
    scale_length_pixels = scale_length_mm * s
    scale_x1 = 50
    scale_y = canvas_height - 20
    canvas.create_line(scale_x1, scale_y, scale_x1 + scale_length_pixels, scale_y, width=2)
    canvas.create_text(scale_x1 + scale_length_pixels / 2, scale_y + 10, text="1 см")

def zoom_in():
    global z
    z *= 1.2
    draw_all()

def zoom_out():
    global z
    z /= 1.2
    draw_all()

def export_svg():
    width_mm = size_mm * (2 - 2**(1 - level))
    svg = f'<svg width="{width_mm}mm" height="{width_mm}mm" viewBox="-{width_mm/2} -{width_mm/2} {width_mm} {width_mm}" xmlns="http://www.w3.org/2000/svg">\n'
    initial_width_mm = size_mm / 20
    svg += draw_H_svg(0, 0, size_mm, initial_width_mm, level)
    # Добавляем линейку масштаба (1 см)
    scale_length_mm = 10  # 1 см = 10 мм
    svg += f'<line x1="-{width_mm/2 + 5}" y1="{width_mm/2 - 5}" x2="-{width_mm/2 + 5 + scale_length_mm}" y2="{width_mm/2 - 5}" stroke="black" stroke-width="0.5" />\n'
    svg += f'<text x="-{width_mm/2 + 5 + scale_length_mm / 2}" y="{width_mm/2 - 7}" font-size="3" text-anchor="middle">1 см</text>\n'
    svg += '</svg>'
    with open("fractal_antenna.svg", "w") as f:
        f.write(svg)

def draw_H_svg(x_mm, y_mm, size_mm, width_mm, level):
    if level == 0:
        return ""
    svg = ""
    svg += f'<line x1="{x_mm - size_mm/2}" y1="{y_mm - size_mm/2}" x2="{x_mm - size_mm/2}" y2="{y_mm + size_mm/2}" stroke="black" stroke-width="{width_mm}" />\n'
    svg += f'<line x1="{x_mm + size_mm/2}" y1="{y_mm - size_mm/2}" x2="{x_mm + size_mm/2}" y2="{y_mm + size_mm/2}" stroke="black" stroke-width="{width_mm}" />\n'
    svg += f'<line x1="{x_mm - size_mm/2}" y1="{y_mm}" x2="{x_mm + size_mm/2}" y2="{y_mm}" stroke="black" stroke-width="{width_mm}" />\n'
    svg += draw_H_svg(x_mm - size_mm/2, y_mm - size_mm/2, size_mm / 2, width_mm / 2, level - 1)
    svg += draw_H_svg(x_mm - size_mm/2, y_mm + size_mm/2, size_mm / 2, width_mm / 2, level - 1)
    svg += draw_H_svg(x_mm + size_mm/2, y_mm - size_mm/2, size_mm / 2, width_mm / 2, level - 1)
    svg += draw_H_svg(x_mm + size_mm/2, y_mm + size_mm/2, size_mm / 2, width_mm / 2, level - 1)
    return svg

def update_frequency():
    global frequency, size_mm
    try:
        new_frequency = float(entry_frequency.get()) * 1e9  # Переводим ГГц в Гц
        if new_frequency > 0:
            frequency = new_frequency
            wavelength = c / frequency
            size_mm = (wavelength / 4) * 1000  # Размер в мм
            draw_all()
    except ValueError:
        pass

root = tk.Tk()
root.title("H-образная фрактальная антенна")
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack(fill="both", expand=True)
canvas.bind("<Configure>", lambda event: draw_all())

frame = tk.Frame(root)
frame.pack()
btn_in = tk.Button(frame, text="Увеличить", command=zoom_in)
btn_in.pack(side="left")
btn_out = tk.Button(frame, text="Уменьшить", command=zoom_out)
btn_out.pack(side="left")
btn_export = tk.Button(frame, text="Экспорт в SVG", command=export_svg)
btn_export.pack(side="left")

# Поле ввода частоты
tk.Label(frame, text="Частота (ГГц):").pack(side="left")
entry_frequency = tk.Entry(frame, width=10)
entry_frequency.insert(0, "2.4")
entry_frequency.pack(side="left")
btn_update = tk.Button(frame, text="Обновить", command=update_frequency)
btn_update.pack(side="left")

z = 1.0
frequency = 2.4e9  # Частота по умолчанию 2.4 ГГц
c = 3e8  # Скорость света в м/с
wavelength = c / frequency
size_mm = (wavelength / 4) * 1000  # Начальный размер в мм
level = 3

draw_all()
root.mainloop()
