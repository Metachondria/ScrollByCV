import tkinter as tk
from tkinter import Canvas
import threading
import pyautogui

class Overlay:
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
        self.root = tk.Tk()
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", "white")
        self.root.overrideredirect(True)  # Убираем рамку окна
        self.canvas = Canvas(self.root, width=self.screen_width, height=self.screen_height, bg="white", highlightthickness=0)
        self.canvas.pack()
        self.dot_radius = 10
        self.current_x = self.screen_width // 2
        self.current_y = self.screen_height // 2
        self.draw_dot(self.current_x, self.current_y)

    def draw_dot(self, x, y):
        self.canvas.delete("all")
        # self.canvas.create_oval(
        #     x - self.dot_radius,
        #     y - self.dot_radius,
        #     x + self.dot_radius,
        #     y + self.dot_radius,
        #     fill="red",
        #     outline=""
        # )
        self.root.update()

    def update_position(self, x, y):
        # Ограничиваем координаты внутри экрана
        x = max(0, min(self.screen_width, int(x)))
        y = max(0, min(self.screen_height, int(y)))
        self.current_x = x
        self.current_y = y
        self.draw_dot(self.current_x, self.current_y)

    def run(self):
        self.root.mainloop()

    def start(self):
        threading.Thread(target=self.run, daemon=True).start()
