import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
import shutil
import json
import platform
from PIL import Image, ImageTk

class SpritePlacerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sprite Placer")

        self.active_state = tk.BooleanVar(value=True)  # Default to active

        self.sprite_images = {}
        self.sprite_paths = {}
        self.placed_sprites = []
        self.grid_size = 50

        self.max_sprite_width = 0
        self.max_sprite_height = 0

        self.selected_sprite = None  # Для хранения текущего выбранного спрайта

        self.setup_ui()

        self.canvas.bind("<Button-1>", self.place_sprite)
        if platform.system() == 'Darwin':
            self.canvas.bind("<Button-2>", self.select_sprite) # Right-click to select sprite
        else:
            self.canvas.bind("<Button-3>", self.select_sprite) # Right-click to select sprite
        self.root.bind("<Escape>", self.deselect_sprite)  # Bind Esc key to deselect sprite
        self.root.bind("<KeyPress-h>", self.show_highlight_sprites)  # Bind key press 'h'
        self.root.bind("<KeyRelease-h>", self.hide_highlight_sprites)  # Bind key release 'h'
        self.root.bind("<KeyPress>", self.key_press)  # Bind arrow keys to move sprite

        self.selected_sprite_id = None  # Track the selected sprite's ID
        self.selected_sprite_outline = None  # Track the outline rectangle ID
        self.status_outlines = []  # Track status outlines

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

        self.load_map_button = tk.Button(self.control_frame, text="Load Map", command=self.load_map)
        self.load_map_button.pack(pady=10, padx=10)

        self.save_button = tk.Button(self.control_frame, text="Save", command=self.save_sprites)
        self.save_button.pack(pady=10, padx=10)

        self.delete_button = tk.Button(self.control_frame, text="Delete", command=self.delete_selected_sprite)
        self.delete_button.pack(pady=10, padx=10)

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

        self.set_canvas_size_button = tk.Button(self.control_frame, text="Set Canvas Size", command=self.set_canvas_size)
        self.set_canvas_size_button.pack(pady=10, padx=10)

        self.grid_size_label = tk.Label(self.control_frame, text="Grid Size:")
        self.grid_size_label.pack(pady=5, padx=10)
        self.grid_size_entry = tk.Entry(self.control_frame)
        self.grid_size_entry.insert(0, "50")
        self.grid_size_entry.pack(pady=5, padx=10)

        self.set_grid_size_button = tk.Button(self.control_frame, text="Set Grid Size", command=self.set_grid_size)
        self.set_grid_size_button.pack(pady=10, padx=10)

        self.help_button = tk.Button(self.control_frame, text="Help", command=self.show_help)
        self.help_button.pack(pady=10, padx=10)

        self.sprite_image_label = tk.Label(self.info_frame, bg="lightgray")
        self.sprite_image_label.pack(pady=10, padx=10)

        self.sprite_name_label = tk.Label(self.info_frame, text="", bg="lightgray")
        self.sprite_name_label.pack(pady=5, padx=10)

        self.sprite_size_label = tk.Label(self.info_frame, text="", bg="lightgray")
        self.sprite_size_label.pack(pady=10, padx=10)

        # Divider line
        self.divider = tk.Frame(self.info_frame, height=2, bd=1, relief=tk.SUNKEN)
        self.divider.pack(fill=tk.X, padx=5, pady=10)

        # Scrollable frame for sprite thumbnails
        self.scrollable_frame = tk.Frame(self.info_frame)
        self.scrollable_frame.pack(fill=tk.BOTH, expand=True)

        self.scroll_canvas = tk.Canvas(self.scrollable_frame, bg="lightgray")
        self.scroll_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.scrollable_frame, orient="vertical", command=self.scroll_canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.scrollable_frame.bind("<Configure>", lambda e: self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all")))
        self.scroll_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.thumbnails_frame = tk.Frame(self.scroll_canvas, bg="lightgray")
        self.scroll_canvas.create_window((0, 0), window=self.thumbnails_frame, anchor="nw")

    def set_canvas_size(self):
        try:
            width = int(self.width_entry.get())
            height = int(self.height_entry.get())
            self.canvas.config(width=width, height=height)
            self.canvas_frame.config(width=width, height=height)
            self.root.geometry(f"{width + self.control_frame.winfo_width() + self.info_frame.winfo_width()}x{height + self.root.winfo_height() - self.canvas.winfo_height()}")
            self.root.resizable(False, False)
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

        self.sprite_paths = {}
        sprite_names = []
        max_width, max_height = 0, 0
        for root, dirs, files in os.walk(sprite_dir):
            for file in files:
                if file.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    sprite_path = os.path.join(root, file)
                    image = Image.open(sprite_path)
                    photo_image = ImageTk.PhotoImage(image)
                    self.sprite_images[file] = (photo_image, image.size)  # Store original size
                    self.sprite_paths[file] = sprite_path  # Сохраняем путь к изображению
                    sprite_names.append(file)
                    max_width = max(max_width, image.size[0])
                    max_height = max(max_height, image.size[1])

        self.max_sprite_width = max_width + 20
        self.max_sprite_height = max_height + 20

        self.info_frame.config(width=self.max_sprite_width)
        self.scroll_canvas.config(width=self.max_sprite_width)

        if sprite_names:
            self.selected_sprite = sprite_names[0]

        print("Sprites loaded:", sprite_names)
        self.display_thumbnails()
        self.display_sprite_info()

    def display_thumbnails(self):
        for widget in self.thumbnails_frame.winfo_children():
            widget.destroy()

        for sprite_name, (photo_image, size) in self.sprite_images.items():
            frame = tk.Frame(self.thumbnails_frame, bg="lightgray", width=self.max_sprite_width, height=size[1] + 40)
            frame.pack_propagate(False)
            label = tk.Label(frame, image=photo_image, bg="lightgray")
            label.photo_image = photo_image  # Keep a reference to avoid garbage collection
            label.pack(pady=5, padx=5)
            label.bind("<Button-1>", lambda e, sprite=sprite_name: self.select_sprite_by_thumbnail(sprite))

            size_label = tk.Label(frame, text=f"{size[0]}x{size[1]}", bg="lightgray")
            size_label.pack()

            frame.pack(pady=5, padx=5)

    def select_sprite_by_thumbnail(self, sprite_name):
        self.selected_sprite = sprite_name
        self.display_sprite_info()
        print(f"Sprite {sprite_name} selected from thumbnails.")

    def place_sprite(self, event):
        if not self.sprite_images or not self.selected_sprite:
            return

        sprite_name = self.selected_sprite
        image, original_size = self.sprite_images[sprite_name]

        # Привязка к пиксельной сетке
        grid_x = (event.x // self.grid_size) * self.grid_size
        grid_y = (event.y // self.grid_size) * self.grid_size

        sprite_id = self.canvas.create_image(grid_x, grid_y, image=image, anchor=tk.NW, tags="sprite")
        self.placed_sprites.append((sprite_id, sprite_name, grid_x, grid_y, original_size, self.active_state.get()))

        self.select_sprite_by_id(sprite_id)
        self.copy_used_sprites()

    def select_sprite(self, event):
        # Find the item under the cursor
        selected_items = self.canvas.find_withtag("current")
        if selected_items:
            self.select_sprite_by_id(selected_items[0])

    def select_sprite_by_id(self, sprite_id):
        # Deselect previous sprite
        if self.selected_sprite_outline is not None:
            self.canvas.delete(self.selected_sprite_outline)
            self.selected_sprite_outline = None

        # Select new sprite
        self.selected_sprite_id = sprite_id
        sprite_coords = self.canvas.coords(self.selected_sprite_id)
        sprite_bbox = self.canvas.bbox(self.selected_sprite_id)
        self.selected_sprite_outline = self.canvas.create_rectangle(sprite_bbox, outline="red", width=2)
        print(f"Sprite {self.selected_sprite_id} selected.")

    def deselect_sprite(self, event=None):
        if self.selected_sprite_outline is not None:
            self.canvas.delete(self.selected_sprite_outline)
            self.selected_sprite_outline = None
            self.selected_sprite_id = None
            print("Sprite deselected.")

    def move_sprite(self, event):
        if self.selected_sprite_id is None:
            return

        movement = {
            "Up": (0, -self.grid_size),
            "Down": (0, self.grid_size),
            "Left": (-self.grid_size, 0),
            "Right": (self.grid_size, 0)
        }

        if event.keysym in movement:
            dx, dy = movement[event.keysym]
            self.canvas.move(self.selected_sprite_id, dx, dy)
            self.canvas.move(self.selected_sprite_outline, dx, dy)

            # Update the position in the placed_sprites list
            for i, (sprite_id, sprite_name, x, y, original_size, active) in enumerate(self.placed_sprites):
                if sprite_id == self.selected_sprite_id:
                    new_x = x + dx
                    new_y = y + dy
                    self.placed_sprites[i] = (sprite_id, sprite_name, new_x, new_y, original_size, active)
                    break

            print(f"Sprite {self.selected_sprite_id} moved {event.keysym} to ({new_x}, {new_y}).")

    def highlight_sprites(self):
        for outline in self.status_outlines:
            self.canvas.delete(outline)
        self.status_outlines.clear()

        for sprite_id, sprite_name, x, y, original_size, active in self.placed_sprites:
            sprite_bbox = self.canvas.bbox(sprite_id)
            outline_color = "blue" if active else "green"
            outline_id = self.canvas.create_rectangle(sprite_bbox, outline=outline_color, width=2)
            self.status_outlines.append(outline_id)

    def show_highlight_sprites(self, event):
        self.highlight_sprites()

    def hide_highlight_sprites(self, event):
        for outline in self.status_outlines:
            self.canvas.delete(outline)
        self.status_outlines.clear()

    def key_press(self, event):
        if event.keysym in ("Up", "Down", "Left", "Right"):
            self.move_sprite(event)

    def show_help(self):
        help_text = (
            "Keyboard Controls:\n"
            " - Arrow Keys: Move selected sprite\n"
            " - h: Highlight sprites by status (hold)\n"
            " - Esc: Deselect sprite\n"
        )
        messagebox.showinfo("Help", help_text)

    def delete_selected_sprite(self):
        if self.selected_sprite_id is not None:
            self.canvas.delete(self.selected_sprite_id)
            # Remove the selected sprite from the list
            self.placed_sprites = [sprite for sprite in self.placed_sprites if sprite[0] != self.selected_sprite_id]
            print(f"Sprite {self.selected_sprite_id} deleted.")
            self.selected_sprite_id = None

            # Remove outline
            if self.selected_sprite_outline is not None:
                self.canvas.delete(self.selected_sprite_outline)
                self.selected_sprite_outline = None
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

    def copy_used_sprites(self):
        used_sprites_dir = os.path.join(os.getcwd(), 'img', 'used_sprites')
        os.makedirs(used_sprites_dir, exist_ok=True)
        used_sprite_names = set(sprite[1] for sprite in self.placed_sprites)  # Собираем все уникальные используемые спрайты

        for sprite_name in used_sprite_names:
            if sprite_name in self.sprite_paths:
                src_path = self.sprite_paths[sprite_name]
                dst_path = os.path.join(used_sprites_dir, sprite_name)
                shutil.copy2(src_path, dst_path)
                print(f"Copied {sprite_name} to {dst_path}")

    def load_map(self):
        file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if not file_path:
            return

        with open(file_path, 'r') as f:
            data = json.load(f)

        # Очистка текущего холста и списка спрайтов
        self.canvas.delete("all")
        self.placed_sprites.clear()

        # Восстановление спрайтов на холсте
        placed_sprites = data["placed_sprites"]
        for item in placed_sprites:
            sprite_name = item['sprite']
            x, y = item['x'], item['y']
            original_size = item['original_size']
            active = item.get('active', True)  # Default to True if 'active' key is not present

            if sprite_name in self.sprite_images:
                image, _ = self.sprite_images[sprite_name]
                sprite_id = self.canvas.create_image(x, y, image=image, anchor=tk.NW, tags="sprite")
                self.placed_sprites.append((sprite_id, sprite_name, x, y, original_size, active))
            else:
                # Если спрайт не найден в текущих изображениях, загружаем его из /img/used_sprites
                sprite_path = os.path.join('img', 'used_sprites', sprite_name)
                if os.path.exists(sprite_path):
                    image = Image.open(sprite_path)
                    photo_image = ImageTk.PhotoImage(image)
                    self.sprite_images[sprite_name] = (photo_image, original_size)
                    sprite_id = self.canvas.create_image(x, y, image=photo_image, anchor=tk.NW, tags="sprite")
                    self.placed_sprites.append((sprite_id, sprite_name, x, y, original_size, active))

        # Установка размера холста из загруженного файла
        if "canvas_size" in data:
            canvas_size = data["canvas_size"]
            self.canvas.config(width=canvas_size["width"], height=canvas_size["height"])

        self.copy_used_sprites()

    def display_sprite_info(self):
        sprite_name = self.selected_sprite
        if sprite_name in self.sprite_images:
            image, original_size = self.sprite_images[sprite_name]
            self.sprite_image_label.config(image=image)
            self.sprite_image_label.image = image  # Keep a reference to avoid garbage collection
            self.sprite_name_label.config(text=sprite_name)
            self.sprite_size_label.config(text=f"Size: {original_size[0]} x {original_size[1]}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SpritePlacerApp(root)
    root.mainloop()
