import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
import shutil
import json
import platform
from PIL import Image, ImageTk


def extract_text(filepath):
    """Извлечение имени файла без расширения."""
    filename = os.path.basename(filepath)
    return filename.replace('.json', '')


class SpritePlacerApp:
    def __init__(self, root):
        """Инициализация приложения."""
        self.root = root
        self.root.title("Sprite Placer")

        self.active_state = tk.BooleanVar(value=True)  # По умолчанию активен

        self.sprite_images = {}
        self.sprite_images_for_nail = {}
        self.sprite_paths = {}
        self.sprite_paths_for_nail = {}
        self.placed_sprites = []
        self.grid_size = 50

        self.max_sprite_width = 0
        self.max_sprite_height = 0

        self.selected_sprite = None  # Текущий выбранный спрайт
        self.scale_factor = 1.0  # Начальный масштаб

        self.grid_lines = []  # Хранение ID линий сетки
        self.grid_opacity = 100  # Начальная непрозрачность

        self.canvas_border = None  # Граница холста

        self.death_height = 0  # Начальная высота линии смерти
        self.player_spawn_x = 0  # Начальная координата X для спауна игрока
        self.player_spawn_y = 0  # Начальная координата Y для спауна игрока

        self.path_to_img = ""

        self.setup_ui()

        self.canvas.bind("<Button-1>", self.place_sprite)
        if platform.system() == 'Darwin':
            self.canvas.bind("<Button-2>", self.select_sprite)  # Правая кнопка для выбора спрайта
        else:
            self.canvas.bind("<Button-3>", self.select_sprite)  # Правая кнопка для выбора спрайта
        self.root.bind("<Escape>", self.deselect_sprite)  # Клавиша Esc для снятия выбора спрайта
        self.root.bind("<KeyPress-h>", self.show_highlight_sprites)  # Клавиша h для выделения спрайтов
        self.root.bind("<KeyRelease-h>", self.hide_highlight_sprites)  # Отпускание клавиши h
        self.root.bind("<KeyPress>", self.key_press)  # Клавиши стрелок для перемещения спрайта
        self.root.bind("<y  >", self.delete_selected_sprite)  # Клавиша Delete для удаления спрайта

        self.root.bind("<Control-s>", self.save_sprites)  # Ctrl+S для сохранения спрайтов
        self.root.bind("<Control-o>", lambda event: self.load_sprites())  # Ctrl+O для загрузки спрайтов
        self.root.bind("<Control-l>", lambda event: self.load_map())  # Ctrl+L для загрузки карты
        self.root.bind("<Control-c>", lambda event: self.open_canvas_size_settings())  # Ctrl+C для настроек холста
        self.root.bind("<Control-g>", lambda event: self.open_grid_settings())  # Ctrl+G для настроек сетки
        self.root.bind("<Control-r>", lambda event: self.open_sprite_settings())  # Ctrl+R для настроек спрайтов

        self.selected_sprite_id = None  # ID выбранного спрайта
        self.selected_sprite_outline = None  # ID контура выбранного спрайта
        self.status_outlines = []  # Хранение контуров статуса

    def setup_ui(self):
        """Настройка пользовательского интерфейса."""
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.control_frame = tk.Frame(self.main_frame, width=200, bg="lightgray")
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.canvas_frame = tk.Frame(self.main_frame)
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.buffer_frame = tk.Frame(self.main_frame, width=100, bg="white")  # Буферная рамка
        self.buffer_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.info_frame = tk.Frame(self.main_frame, width=200, bg="lightgray")
        self.info_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", lambda e: self.draw_grid())  # Перерисовка сетки при изменении размера

        self.load_button = tk.Button(self.control_frame, text="Load", command=self.open_load_settings)
        self.load_button.pack(pady=10, padx=10)

        self.canvas_size_button = tk.Button(self.control_frame, text="Canvas Size", command=self.open_canvas_size_settings)
        self.canvas_size_button.pack(pady=10, padx=10)

        self.grid_settings_button = tk.Button(self.control_frame, text="Grid Settings", command=self.open_grid_settings)
        self.grid_settings_button.pack(pady=10, padx=10)

        self.sprite_settings_button = tk.Button(self.control_frame, text="Sprite Settings", command=self.open_sprite_settings)
        self.sprite_settings_button.pack(pady=10, padx=10)

        self.death_height_button = tk.Button(self.control_frame, text="Set Death Height", command=self.open_death_height_settings)
        self.death_height_button.pack(pady=10, padx=10)

        self.player_spawn_button = tk.Button(self.control_frame, text="Set Player Spawn", command=self.open_player_spawn_settings)
        self.player_spawn_button.pack(pady=10, padx=10)

        self.save_button = tk.Button(self.control_frame, text="Save", command=self.save_sprites)
        self.save_button.pack(pady=10, padx=10)

        self.delete_button = tk.Button(self.control_frame, text="Delete", command=self.delete_selected_sprite)
        self.delete_button.pack(pady=10, padx=10)

        self.active_checkbox = tk.Checkbutton(self.control_frame, text="status", variable=self.active_state, command=self.toggle_status)
        self.active_checkbox.pack(pady=10, padx=10)

        self.help_button = tk.Button(self.control_frame, text="Help", command=self.show_help)
        self.help_button.pack(pady=10, padx=10)

        self.sprite_image_label = tk.Label(self.info_frame, bg="lightgray")
        self.sprite_image_label.pack(pady=10, padx=10)

        self.sprite_name_label = tk.Label(self.info_frame, text="", bg="lightgray")
        self.sprite_name_label.pack(pady=5, padx=10)

        self.sprite_size_label = tk.Label(self.info_frame, text="", bg="lightgray")
        self.sprite_size_label.pack(pady=10, padx=10)

        # Разделительная линия
        self.divider = tk.Frame(self.info_frame, height=2, bd=1, relief=tk.SUNKEN)
        self.divider.pack(fill=tk.X, padx=5, pady=10)

        # Прокручиваемая рамка для миниатюр спрайтов
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

    def open_load_settings(self):
        """Открытие окна настроек загрузки."""
        load_settings_window = tk.Toplevel(self.root)
        load_settings_window.title("Load Settings")

        self.load_sprites_button = tk.Button(load_settings_window, text="Load Sprites", command=self.load_sprites)
        self.load_sprites_button.pack(pady=10, padx=10)

        self.load_map_button = tk.Button(load_settings_window, text="Load Map", command=self.load_map)
        self.load_map_button.pack(pady=10, padx=10)

    def open_canvas_size_settings(self):
        """Открытие окна настроек размера холста."""
        canvas_size_window = tk.Toplevel(self.root)
        canvas_size_window.title("Canvas Size Settings")

        self.width_label = tk.Label(canvas_size_window, text="Canvas Width:")
        self.width_label.pack(pady=5, padx=10)
        self.width_entry = tk.Entry(canvas_size_window)
        self.width_entry.pack(pady=5, padx=10)

        self.height_label = tk.Label(canvas_size_window, text="Canvas Height:")
        self.height_label.pack(pady=5, padx=10)
        self.height_entry = tk.Entry(canvas_size_window)
        self.height_entry.pack(pady=5, padx=10)

        self.set_canvas_size_button = tk.Button(canvas_size_window, text="Set Canvas Size", command=self.set_canvas_size)
        self.set_canvas_size_button.pack(pady=10, padx=10)

    def open_grid_settings(self):
        """Открытие окна настроек сетки."""
        grid_settings_window = tk.Toplevel(self.root)
        grid_settings_window.title("Grid Settings")

        self.grid_size_label = tk.Label(grid_settings_window, text="Grid Size:")
        self.grid_size_label.pack(pady=5, padx=10)
        self.grid_size_entry = tk.Entry(grid_settings_window)
        self.grid_size_entry.insert(0, str(self.grid_size))
        self.grid_size_entry.pack(pady=5, padx=10)

        self.set_grid_size_button = tk.Button(grid_settings_window, text="Set Grid Size", command=self.set_grid_size)
        self.set_grid_size_button.pack(pady=10, padx=10)

        self.grid_opacity_label = tk.Label(grid_settings_window, text="Grid Opacity:")
        self.grid_opacity_label.pack(pady=5, padx=10)
        self.grid_opacity_scale = tk.Scale(grid_settings_window, from_=0, to=100, orient=tk.HORIZONTAL, command=self.update_grid_opacity)
        self.grid_opacity_scale.set(self.grid_opacity)
        self.grid_opacity_scale.pack(pady=5, padx=10)

    def open_death_height_settings(self):
        """Открытие окна настроек высоты линии смерти."""
        death_height_window = tk.Toplevel(self.root)
        death_height_window.title("Set Death Height")

        self.death_height_label = tk.Label(death_height_window, text="Death Line Y-coordinate:")
        self.death_height_label.pack(pady=5, padx=10)
        self.death_height_entry = tk.Entry(death_height_window)
        self.death_height_entry.pack(pady=5, padx=10)

        self.set_death_height_button = tk.Button(death_height_window, text="Set Death Height", command=self.set_death_height)
        self.set_death_height_button.pack(pady=10, padx=10)

    def open_player_spawn_settings(self):
        """Открытие окна настроек точки спауна игрока."""
        player_spawn_window = tk.Toplevel(self.root)
        player_spawn_window.title("Set Player Spawn")

        self.player_spawn_x_label = tk.Label(player_spawn_window, text="Player Spawn X-coordinate:")
        self.player_spawn_x_label.pack(pady=5, padx=10)
        self.player_spawn_x_entry = tk.Entry(player_spawn_window)
        self.player_spawn_x_entry.pack(pady=5, padx=10)

        self.player_spawn_y_label = tk.Label(player_spawn_window, text="Player Spawn Y-coordinate:")
        self.player_spawn_y_label.pack(pady=5, padx=10)
        self.player_spawn_y_entry = tk.Entry(player_spawn_window)
        self.player_spawn_y_entry.pack(pady=5, padx=10)

        self.set_player_spawn_button = tk.Button(player_spawn_window, text="Set Player Spawn", command=self.set_player_spawn)
        self.set_player_spawn_button.pack(pady=10, padx=10)

    def open_sprite_settings(self):
        """Открытие окна настроек спрайтов."""
        sprite_settings_window = tk.Toplevel(self.root)
        sprite_settings_window.title("Sprite Settings")

        self.scale_factor_label = tk.Label(sprite_settings_window, text="Scale Factor:")
        self.scale_factor_label.pack(pady=5, padx=10)
        self.scale_factor_entry = tk.Entry(sprite_settings_window)
        self.scale_factor_entry.insert(0, "1.0")  # Начальный коэффициент масштабирования
        self.scale_factor_entry.pack(pady=5, padx=10)

        self.set_scale_button = tk.Button(sprite_settings_window, text="Set Scale", command=self.set_scale)
        self.set_scale_button.pack(pady=10, padx=10)

    def set_death_height(self):
        """Установка высоты линии смерти."""
        try:
            self.death_height = int(self.death_height_entry.get())
            print(f"Death line Y-coordinate set to {self.death_height}")
        except ValueError:
            print("Please enter a valid Y-coordinate for the death line.")

    def set_player_spawn(self):
        """Установка точки спауна игрока."""
        try:
            self.player_spawn_x = int(self.player_spawn_x_entry.get())
            self.player_spawn_y = int(self.player_spawn_y_entry.get())
            print(f"Player spawn set to ({self.player_spawn_x}, {self.player_spawn_y})")
        except ValueError:
            print("Please enter valid coordinates for player spawn.")

    def set_canvas_size(self):
        """Установка размера холста."""
        try:
            width = int(self.width_entry.get())
            height = int(self.height_entry.get())
            self.canvas.config(width=width, height=height)
            self.canvas_frame.config(width=width, height=height)
            self.root.geometry(f"{width + self.control_frame.winfo_width() + self.info_frame.winfo_width()}x{height + self.root.winfo_height() - self.canvas.winfo_height()}")
            self.root.resizable(False, False)  # Фиксация размера окна
            self.draw_canvas_border()
        except ValueError:
            print("Please enter valid width and height.")

    def set_grid_size(self):
        """Установка размера сетки."""
        try:
            self.grid_size = int(self.grid_size_entry.get())
            self.draw_grid()
        except ValueError:
            print("Please enter a valid grid size.")

    def update_grid_opacity(self, value):
        """Обновление непрозрачности сетки."""
        alpha = int(value) * 255 // 100
        color = f'#{alpha:02x}{alpha:02x}{alpha:02x}'
        for line_id in self.grid_lines:
            self.canvas.itemconfig(line_id, fill=color)

    def draw_grid(self):
        """Отрисовка сетки."""
        for line_id in self.grid_lines:
            self.canvas.delete(line_id)
        self.grid_lines.clear()

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        for i in range(0, width, self.grid_size):
            line_id = self.canvas.create_line(i, 0, i, height, fill="#d3d3d3")
            self.grid_lines.append(line_id)

        for i in range(0, height, self.grid_size):
            line_id = self.canvas.create_line(0, i, width, i, fill="#d3d3d3")
            self.grid_lines.append(line_id)

        self.draw_canvas_border()

    def draw_canvas_border(self):
        """Отрисовка границы холста."""
        if self.canvas_border:
            self.canvas.delete(self.canvas_border)

        self.canvas_border = self.canvas.create_rectangle(0, 0, self.canvas.winfo_width(), self.canvas.winfo_height(), outline="purple", width=2)

    def set_scale(self):
        """Установка коэффициента масштабирования."""
        try:
            self.scale_factor = float(self.scale_factor_entry.get())
        except ValueError:
            print("Please enter a valid scale factor.")
            return

        print(f"Scale factor set to {self.scale_factor}.")

    def load_sprites(self):
        """Загрузка спрайтов."""
        self.sprite_images_for_nail.clear()
        sprite_dir = filedialog.askdirectory(title="Select Sprite Directory")
        if not sprite_dir:
            return

        sprite_names = []
        max_width, max_height = 0, 0
        for root, dirs, files in os.walk(sprite_dir):
            for file in files:
                if file.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    sprite_path = os.path.join(root, file)
                    image = Image.open(sprite_path)
                    photo_image = ImageTk.PhotoImage(image)
                    self.sprite_images[file] = (photo_image, image.size)  # Сохранение оригинального размера
                    self.sprite_paths[file] = sprite_path  # Сохранение пути к изображению
                    self.sprite_images_for_nail[file] = (photo_image, image.size)  # Сохранение оригинального размера
                    self.sprite_paths_for_nail[file] = sprite_path  # Сохранение пути к изображению
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
        """Отображение миниатюр спрайтов."""
        for widget in self.thumbnails_frame.winfo_children():
            widget.destroy()

        for sprite_name, (photo_image, size) in self.sprite_images_for_nail.items():
            frame = tk.Frame(self.thumbnails_frame, bg="lightgray", width=self.max_sprite_width, height=size[1] + 40)
            frame.pack_propagate(False)
            label = tk.Label(frame, image=photo_image, bg="lightgray")
            label.photo_image = photo_image  # Сохранение ссылки для предотвращения сборки мусора
            label.pack(pady=5, padx=5)
            label.bind("<Button-1>", lambda e, sprite=sprite_name: self.select_sprite_by_thumbnail(sprite))

            size_label = tk.Label(frame, text=f"{size[0]}x{size[1]}", bg="lightgray")
            size_label.pack()

            frame.pack(pady=5, padx=5)

    def select_sprite_by_thumbnail(self, sprite_name):
        """Выбор спрайта по миниатюре."""
        self.selected_sprite = sprite_name
        self.display_sprite_info()
        print(f"Sprite {sprite_name} selected from thumbnails.")

    def place_sprite(self, event):
        """Размещение спрайта на холсте."""
        if not self.sprite_images or not self.selected_sprite:
            return

        sprite_name = self.selected_sprite
        image, original_size = self.sprite_images[sprite_name]

        # Привязка к пиксельной сетке
        grid_x = (event.x // self.grid_size) * self.grid_size
        grid_y = (event.y // self.grid_size) * self.grid_size

        # Масштабирование изображения
        new_size = (int(original_size[0] * self.scale_factor), int(original_size[1] * self.scale_factor))
        resized_image = Image.open(self.sprite_paths[sprite_name]).resize(new_size, Image.Resampling.LANCZOS)
        photo_image = ImageTk.PhotoImage(resized_image)

        sprite_id = self.canvas.create_image(grid_x, grid_y, image=photo_image, anchor=tk.NW, tags="sprite")
        self.placed_sprites.append((sprite_id, sprite_name, grid_x, grid_y, original_size, new_size, self.active_state.get()))

        # Обновление отображаемого изображения
        self.sprite_images[sprite_name + "_" + str(sprite_id)] = (photo_image, new_size)

        self.select_sprite_by_id(sprite_id)
        self.copy_used_sprites()

    def select_sprite(self, event):
        """Выбор спрайта на холсте."""
        selected_items = self.canvas.find_withtag("current")
        if selected_items:
            self.select_sprite_by_id(selected_items[0])

    def toggle_status(self):
        """Переключение статуса спрайта."""
        if self.selected_sprite_id is not None:
            for i, (sprite_id, sprite_name, x, y, original_size, current_size, active) in enumerate(self.placed_sprites):
                if sprite_id == self.selected_sprite_id:
                    self.placed_sprites[i] = (sprite_id, sprite_name, x, y, original_size, current_size, self.active_state.get())
                    print(f"Статус спрайта {sprite_id} обновлен на {'активный' if self.active_state.get() else 'неактивный'}.")
                    break

    def select_sprite_by_id(self, sprite_id):
        """Выбор спрайта по ID."""
        if self.selected_sprite_outline is not None:
            self.canvas.delete(self.selected_sprite_outline)
            self.selected_sprite_outline = None

        self.selected_sprite_id = sprite_id
        sprite_coords = self.canvas.coords(self.selected_sprite_id)
        sprite_bbox = self.canvas.bbox(self.selected_sprite_id)
        self.selected_sprite_outline = self.canvas.create_rectangle(sprite_bbox, outline="red", width=2)
        print(f"Sprite {self.selected_sprite_id} selected.")

        for sprite_id, sprite_name, x, y, original_size, current_size, active in self.placed_sprites:
            if sprite_id == self.selected_sprite_id:
                self.active_state.set(active)
                break

    def deselect_sprite(self, event=None):
        """Снятие выбора спрайта."""
        if self.selected_sprite_outline is not None:
            self.canvas.delete(self.selected_sprite_outline)
            self.selected_sprite_outline = None
            self.selected_sprite_id = None
            self.active_state.set(True)  # Сброс состояния
            print("Sprite deselected.")

    def move_sprite(self, event):
        """Перемещение спрайта."""
        global new_x, new_y
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

            for i, (sprite_id, sprite_name, x, y, original_size, current_size, active) in enumerate(self.placed_sprites):
                if sprite_id == self.selected_sprite_id:
                    new_x = x + dx
                    new_y = y + dy
                    self.placed_sprites[i] = (sprite_id, sprite_name, new_x, new_y, original_size, current_size, active)
                    break

            print(f"Sprite {self.selected_sprite_id} moved {event.keysym} to ({new_x}, {new_y}).")

    def highlight_sprites(self):
        """Выделение спрайтов по статусу."""
        for outline in self.status_outlines:
            self.canvas.delete(outline)
        self.status_outlines.clear()

        for sprite_id, sprite_name, x, y, original_size, current_size, active in self.placed_sprites:
            sprite_bbox = self.canvas.bbox(sprite_id)
            outline_color = "blue" if active else "green"
            outline_id = self.canvas.create_rectangle(sprite_bbox, outline=outline_color, width=2)
            self.status_outlines.append(outline_id)

    def show_highlight_sprites(self, event):
        """Отображение выделенных спрайтов."""
        self.highlight_sprites()

    def hide_highlight_sprites(self, event):
        """Скрытие выделенных спрайтов."""
        for outline in self.status_outlines:
            self.canvas.delete(outline)
        self.status_outlines.clear()

    def key_press(self, event):
        """Обработка нажатия клавиш."""
        if event.keysym in ("Up", "Down", "Left", "Right"):
            self.move_sprite(event)

    def show_help(self):
        """Отображение справки."""
        help_text = (
            "Keyboard Controls:\n"
            " - Arrow Keys: Move selected sprite\n"
            " - h: Highlight sprites by status (hold)\n"
            " - Esc: Deselect sprite\n"
            " - Delete: Delete selected sprite\n"
            " - Ctrl+S: Save sprites\n"
            " - Ctrl+O: Load sprites\n"
            " - Ctrl+L: Load map\n"
            " - Ctrl+C: Canvas settings\n"
            " - Ctrl+G: Grid settings\n"
            " - Ctrl+R: Sprite settings\n"
        )
        messagebox.showinfo("Help", help_text)

    def delete_selected_sprite(self, event=None):
        """Удаление выбранного спрайта."""
        if self.selected_sprite_id is not None:
            self.canvas.delete(self.selected_sprite_id)
            self.placed_sprites = [sprite for sprite in self.placed_sprites if sprite[0] != self.selected_sprite_id]
            print(f"Sprite {self.selected_sprite_id} deleted.")
            self.selected_sprite_id = None

            if self.selected_sprite_outline is not None:
                self.canvas.delete(self.selected_sprite_outline)
                self.selected_sprite_outline = None
        else:
            print("No sprite selected.")

    def save_sprites(self, event=None):
        """Сохранение спрайтов в JSON файл."""
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if not file_path:
            return

        placed_sprites_data = []
        coins_data = []
        portals_data = []

        for _, sprite, x, y, original_size, current_size, active in self.placed_sprites:
            sprite_data = {
                "sprite": sprite,
                "x": x,
                "y": y,
                "original_size": original_size,
                "current_size": current_size,
                "active": active
            }

            if sprite == "coin__01.png":
                coins_data.append(sprite_data)
            elif sprite == "portal_open.png":
                portals_data.append(sprite_data)
            else:
                placed_sprites_data.append(sprite_data)

        data = {
            "placed_sprites": placed_sprites_data,
            "coins": coins_data,
            "portals": portals_data,
            "canvas_size": {"width": self.canvas.winfo_width(), "height": self.canvas.winfo_height()},
            "death_line": {"y_d": self.death_height if hasattr(self, 'death_height') else 0},
            "player_spawn": {"x": self.player_spawn_x if hasattr(self, 'player_spawn_x') else 0,
                             "y": self.player_spawn_y if hasattr(self, 'player_spawn_y') else 0}
        }

        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

        print(f"Saved to {file_path}")

    def copy_used_sprites(self):
        """Копирование использованных спрайтов в директорию used_sprites."""
        used_sprites_dir = os.path.join(os.getcwd(), 'img', f'{self.path_to_img}', 'used_sprites')
        os.makedirs(used_sprites_dir, exist_ok=True)
        used_sprite_names = set(sprite[1] for sprite in self.placed_sprites)

        for sprite_name in used_sprite_names:
            if sprite_name in self.sprite_paths:
                src_path = self.sprite_paths[sprite_name]
                dst_path = os.path.join(used_sprites_dir, sprite_name)

                if os.path.abspath(src_path) == os.path.abspath(dst_path):
                    print(f"Skipping copy for {sprite_name} as source and destination are the same.")
                    continue

                shutil.copy2(src_path, dst_path)
                print(f"Copied {sprite_name} to {dst_path}")

    def load_map(self):
        """Загрузка карты из JSON файла."""
        file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        self.path_to_img = extract_text(file_path)
        if not file_path:
            return

        with open(file_path, 'r') as f:
            data = json.load(f)

        self.canvas.delete("all")
        self.placed_sprites.clear()

        player_cords = data["player_spawn"]
        self.player_spawn_x = player_cords["x"]
        self.player_spawn_y = player_cords["y"]

        death_line = data["death_line"]
        self.death_height = death_line["y_d"]

        placed_sprites = data["placed_sprites"]
        for item in placed_sprites:
            sprite_name = item['sprite']
            x, y = item['x'], item['y']
            original_size = item['original_size']
            current_size = item['current_size']
            active = item.get('active', True)

            if sprite_name in self.sprite_paths:
                original_image = Image.open(self.sprite_paths[sprite_name])
                resized_image = original_image.resize(current_size, Image.Resampling.LANCZOS)
                photo_image = ImageTk.PhotoImage(resized_image)
                sprite_id = self.canvas.create_image(x, y, image=photo_image, anchor=tk.NW, tags="sprite")
                self.sprite_images[sprite_name + "_" + str(sprite_id)] = (photo_image, current_size)
                self.placed_sprites.append((sprite_id, sprite_name, x, y, original_size, current_size, active))
            else:
                sprite_path = os.path.join('img', f'{self.path_to_img}', 'used_sprites', sprite_name)
                self.sprite_paths[sprite_name] = sprite_path
                if os.path.exists(sprite_path):
                    original_image = Image.open(sprite_path)
                    resized_image = original_image.resize(current_size, Image.Resampling.LANCZOS)
                    photo_image = ImageTk.PhotoImage(resized_image)
                    sprite_id = self.canvas.create_image(x, y, image=photo_image, anchor=tk.NW, tags="sprite")
                    self.sprite_images[sprite_name + "_" + str(sprite_id)] = (photo_image, current_size)
                    self.placed_sprites.append((sprite_id, sprite_name, x, y, original_size, current_size, active))

        if "canvas_size" in data:
            canvas_size = data["canvas_size"]
            self.canvas.config(width=canvas_size["width"], height=canvas_size["height"])
            self.draw_canvas_border()

        self.copy_used_sprites()

    def display_sprite_info(self):
        """Отображение информации о спрайте."""
        sprite_name = self.selected_sprite
        if sprite_name in self.sprite_images:
            image, original_size = self.sprite_images[sprite_name]
            self.sprite_image_label.config(image=image)
            self.sprite_image_label.image = image
            self.sprite_name_label.config(text=sprite_name)
            self.sprite_size_label.config(text=f"Size: {original_size[0]} x {original_size[1]}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SpritePlacerApp(root)
    root.mainloop()
