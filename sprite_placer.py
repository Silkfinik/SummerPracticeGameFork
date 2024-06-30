import tkinter as tk
from tkinter import filedialog, ttk
import os
import json
from PIL import Image, ImageTk


class SpritePlacerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sprite Placer")

        self.active_state = tk.BooleanVar(value=True)  # Default to active

        self.setup_ui()

        self.sprite_images = {}
        self.placed_sprites = []
        self.grid_size = 50

        self.canvas.bind("<Button-1>", self.place_sprite)
        self.canvas.bind("<Button-3>", self.select_sprite)  # Right-click to select sprite
        self.sprite_menu.bind("<<ComboboxSelected>>", self.display_sprite_info)

        self.selected_sprite_id = None  # Track the selected sprite's ID

    def setup_ui(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.control_frame = tk.Frame(self.main_frame, width=200, bg="lightgray")
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.canvas_frame = tk.Frame(self.main_frame)
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.info_frame = tk.Frame(self.main_frame, width=200, bg="lightgray")
        self.info_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.load_sprites_button = tk.Button(self.control_frame, text="Load Sprites", command=self.load_sprites)
        self.load_sprites_button.pack(pady=10, padx=10)

        self.save_button = tk.Button(self.control_frame, text="Save", command=self.save_sprites)
        self.save_button.pack(pady=10, padx=10)

        self.delete_button = tk.Button(self.control_frame, text="Delete", command=self.delete_selected_sprite)
        self.delete_button.pack(pady=10, padx=10)

        self.sprite_var = tk.StringVar()
        self.sprite_menu = ttk.Combobox(self.control_frame, textvariable=self.sprite_var)
        self.sprite_menu.pack(pady=10, padx=10)

        self.active_checkbox = tk.Checkbutton(self.control_frame, text="status", variable=self.active_state)
        self.active_checkbox.pack(pady=10, padx=10)

        self.width_label = tk.Label(self.control_frame, text="Canvas Width:")
        self.width_label.pack(pady=5, padx=10)
        self.width_entry = tk.Entry(self.control_frame)
        self.width_entry.pack(pady=5, padx=10)

        self.height_label = tk.Label(self.control_frame, text="Canvas Height:")
        self.height_label.pack(pady=5, padx=10)
        self.height_entry = tk.Entry(self.control_frame)
        self.height_entry.pack(pady=5, padx=10)

        self.set_canvas_size_button = tk.Button(self.control_frame, text="Set Canvas Size",
                                                command=self.set_canvas_size)
        self.set_canvas_size_button.pack(pady=10, padx=10)

        self.grid_size_label = tk.Label(self.control_frame, text="Grid Size:")
        self.grid_size_label.pack(pady=5, padx=10)
        self.grid_size_entry = tk.Entry(self.control_frame)
        self.grid_size_entry.insert(0, "50")
        self.grid_size_entry.pack(pady=5, padx=10)

        self.set_grid_size_button = tk.Button(self.control_frame, text="Set Grid Size", command=self.set_grid_size)
        self.set_grid_size_button.pack(pady=10, padx=10)

        self.sprite_image_label = tk.Label(self.info_frame, bg="lightgray")
        self.sprite_image_label.pack(pady=10, padx=10)

        self.sprite_size_label = tk.Label(self.info_frame, text="", bg="lightgray")
        self.sprite_size_label.pack(pady=10, padx=10)

    def set_canvas_size(self):
        try:
            width = int(self.width_entry.get())
            height = int(self.height_entry.get())
            self.canvas.config(width=width, height=height)
            self.canvas_frame.config(width=width, height=height)
        except ValueError:
            print("Please enter valid width and height.")

    def set_grid_size(self):
        try:
            self.grid_size = int(self.grid_size_entry.get())
        except ValueError:
            print("Please enter a valid grid size.")

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

        sprite_id = self.canvas.create_image(grid_x, grid_y, image=image, anchor=tk.NW, tags="sprite")
        self.placed_sprites.append((sprite_id, sprite_name, grid_x, grid_y, original_size, self.active_state.get()))

    def select_sprite(self, event):
        # Find the item under the cursor
        selected_items = self.canvas.find_withtag("current")
        if selected_items:
            # Deselect previous sprite
            if self.selected_sprite_id is not None:
                self.canvas.itemconfig(self.selected_sprite_id, outline="")

            # Select new sprite
            self.selected_sprite_id = selected_items[0]
            self.canvas.itemconfig(self.selected_sprite_id, outline="red")
            print(f"Sprite {self.selected_sprite_id} selected.")

    def delete_selected_sprite(self):
        if self.selected_sprite_id is not None:
            self.canvas.delete(self.selected_sprite_id)
            # Remove the selected sprite from the list
            self.placed_sprites = [sprite for sprite in self.placed_sprites if sprite[0] != self.selected_sprite_id]
            print(f"Sprite {self.selected_sprite_id} deleted.")
            self.selected_sprite_id = None
        else:
            print("No sprite selected.")

    def save_sprites(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if not file_path:
            return

        data = {"placed_sprites": [{"sprite": sprite, "x": x, "y": y, "original_size": original_size, "active": active} for
                                   _, sprite, x, y, original_size, active in self.placed_sprites],
                "canvas_size": {"width": self.canvas.winfo_width(), "height": self.canvas.winfo_height()}}
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

        print(f"Saved to {file_path}")

    def display_sprite_info(self, event):
        sprite_name = self.sprite_var.get()
        if sprite_name in self.sprite_images:
            image, original_size = self.sprite_images[sprite_name]
            self.sprite_image_label.config(image=image)
            self.sprite_image_label.image = image  # Keep a reference to avoid garbage collection
            self.sprite_size_label.config(text=f"Size: {original_size[0]} x {original_size[1]}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SpritePlacerApp(root)
    root.mainloop()
