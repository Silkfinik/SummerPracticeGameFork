import tkinter as tk
from tkinter import filedialog, ttk
import os
import json
from PIL import Image, ImageTk


class SpritePlacerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sprite Placer")

        self.setup_ui()

        self.sprite_images = {}
        self.placed_sprites = []
        self.grid_size = 50

        self.canvas.bind("<Button-1>", self.place_sprite)

    def setup_ui(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.control_frame = tk.Frame(self.main_frame, width=200, bg="lightgray")
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.canvas_frame = tk.Frame(self.main_frame)
        self.canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.load_sprites_button = tk.Button(self.control_frame, text="Load Sprites", command=self.load_sprites)
        self.load_sprites_button.pack(pady=10, padx=10)

        self.save_button = tk.Button(self.control_frame, text="Save", command=self.save_sprites)
        self.save_button.pack(pady=10, padx=10)

        self.sprite_var = tk.StringVar()
        self.sprite_menu = ttk.Combobox(self.control_frame, textvariable=self.sprite_var)
        self.sprite_menu.pack(pady=10, padx=10)

    def load_sprites(self):
        sprite_dir = filedialog.askdirectory(title="Select Sprite Directory")
        if not sprite_dir:
            return

        self.sprite_images.clear()
        sprite_names = []
        for root, dirs, files in os.walk(sprite_dir):
            for file in files:
                if file.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    sprite_path = os.path.join(root, file)
                    image = Image.open(sprite_path)
                    image.thumbnail((self.grid_size, self.grid_size))  # Adjust size to grid size
                    photo_image = ImageTk.PhotoImage(image)
                    self.sprite_images[file] = (photo_image, image.size)  # Store original size
                    sprite_names.append(file)

        self.sprite_menu['values'] = sprite_names
        if sprite_names:
            self.sprite_var.set(sprite_names[0])

        print("Sprites loaded:", sprite_names)

    def place_sprite(self, event):
        if not self.sprite_images or not self.sprite_var.get():
            return

        sprite_name = self.sprite_var.get()
        image, original_size = self.sprite_images[sprite_name]

        # Привязка к пиксельной сетке
        grid_x = (event.x // self.grid_size) * self.grid_size
        grid_y = (event.y // self.grid_size) * self.grid_size

        sprite_id = self.canvas.create_image(grid_x, grid_y, image=image, anchor=tk.NW)
        self.placed_sprites.append((sprite_name, grid_x, grid_y, original_size))

    def save_sprites(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if not file_path:
            return

        data = {"placed_sprites": [{"sprite": sprite, "x": x, "y": y, "original_size": original_size} for
                                   sprite, x, y, original_size in self.placed_sprites],
                "canvas_size": {"width": self.canvas.winfo_width(), "height": self.canvas.winfo_height()}}
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

        print(f"Saved to {file_path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SpritePlacerApp(root)
    root.mainloop()
