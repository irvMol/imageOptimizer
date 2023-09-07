import os
import os.path
from PIL import Image, ImageOps
import tkinter as tk
from tkinter import filedialog, IntVar


def toggle_slider_state():
    if resize_var.get():
        percentage_slider.config(state="normal")
    else:
        percentage_slider.config(state="disabled")


def toggle_rename_state():
    if rename_var.get():
        project_name_entry.config(state="normal")
    else:
        project_name_entry.config(state="disabled")


def resize_image(img_path, percent):
    try:
        img = Image.open(img_path)
        img = ImageOps.exif_transpose(img)
        width = int(img.size[0] * percent / 100)
        height = int(img.size[1] * percent / 100)
        new_size = (width, height)
        img = img.resize(new_size)
        return img
    except IOError:
        print("Error resizing image:", img_path)
        return None


def rename_image(img_path, project_name, index, img_dir):
    try:
        file_name, file_extension = os.path.splitext(img_path)
        new_img_path = os.path.join(
            img_dir, f"{project_name}{index}{file_extension}")
        os.rename(img_path, new_img_path)
        return new_img_path
    except Exception as e:
        print(f"Error renaming image: {img_path} - {e}")
        return None


def generate_thumbnails(img_dir, thumbnail_size):
    thumbnail_dir = os.path.join(img_dir, "thumbnails")

    if not os.path.exists(thumbnail_dir):
        os.makedirs(thumbnail_dir)

    for i, file in enumerate(os.listdir(img_dir)):
        cur_img_path = os.path.join(img_dir, file)
        if os.path.isfile(cur_img_path) and thumbnail_var.get():
            try:
                img = resize_image(cur_img_path, thumbnail_size)
                if img:
                    thumbnail_path = os.path.join(thumbnail_dir, file)
                    img.save(thumbnail_path, optimize=True, quality=85)
                    print(f"Generated thumbnail for {file}")
            except IOError:
                print("Wrong file type or error generating thumbnail for " + file)


def process_images():
    project_name = project_name_entry.get()
    img_dir = filedialog.askdirectory(title="Select Image Directory")
    percent = int(percentage_slider.get())

    if not project_name or not img_dir:
        result_label.config(
            text="Please provide project name and select a directory.")
        return

    rename_option = rename_var.get()
    resize_option = resize_var.get()
    generate_thumbnail_option = thumbnail_var.get()

    for i, file in enumerate(os.listdir(img_dir)):
        cur_img_path = os.path.join(img_dir, file)

        # Check if the file is an image file (supports various extensions)
        image_extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp")

        if os.path.isfile(cur_img_path):

            if rename_option and project_name not in file and cur_img_path.lower().endswith(image_extensions):
                new_img_path = rename_image(
                    cur_img_path, project_name, i, img_dir)
                if new_img_path:
                    print(
                        f"Renamed {file} to {os.path.basename(new_img_path)}")
                    cur_img_path = new_img_path  # Update the current path to the renamed path

            if resize_option:
                try:
                    # Check if the file is an image file (supports various extensions)
                    if cur_img_path.lower().endswith(image_extensions):
                        resized_img = resize_image(cur_img_path, percent)
                        original_extension = os.path.splitext(cur_img_path)[1]
                        if resized_img:
                            new_img_path = os.path.join(
                                img_dir, f"{project_name}{i}{original_extension}")
                            resized_img.save(
                                new_img_path, optimize=True, quality=85)
                            print(
                                f"Resized {os.path.basename(cur_img_path)}")
                    else:
                        print(f"Skipping non-image file: {file}")
                except IOError:
                    print("Error processing " + file)

    if generate_thumbnail_option:
        thumbnail_size = int(thumbnail_size_entry.get())
        generate_thumbnails(img_dir, thumbnail_size)

    result_label.config(text="Image processing complete.")


# Create the Tkinter window
window = tk.Tk()
window.title("Image Processing Tool")

# Create and arrange widgets
project_name_label = tk.Label(window, text="Project Name:")
project_name_label.pack()

project_name_entry = tk.Entry(window, state="disabled")
project_name_entry.pack()

rename_var = IntVar()
rename_checkbox = tk.Checkbutton(
    window, text="Rename Images", variable=rename_var, command=toggle_rename_state)
rename_checkbox.pack()

resize_var = IntVar()
resize_checkbox = tk.Checkbutton(
    window, text="Resize Images", variable=resize_var,  command=toggle_slider_state)
resize_checkbox.pack()

thumbnail_var = IntVar()
thumbnail_checkbox = tk.Checkbutton(
    window, text="Generate Thumbnails", variable=thumbnail_var)
thumbnail_checkbox.pack()


percentage_label = tk.Label(window, text="Resize Percentage: ")
percentage_label.pack()

percentage_slider = tk.Scale(
    window, from_=1, to=125, orient="horizontal", length=200)
percentage_slider.set(50)
percentage_slider.pack()


# Create and arrange widgets for thumbnail generation

thumbnail_size_label = tk.Label(window, text="Thumbnail Size Percentage:")
thumbnail_size_label.pack()

thumbnail_size_entry = tk.Entry(window)
thumbnail_size_entry.pack()

process_button = tk.Button(
    window, text="Process Images", command=process_images)
process_button.pack()

result_label = tk.Label(window, text="")
result_label.pack()

# Initialize slider state
toggle_slider_state()

# Start the Tkinter main loop
window.mainloop()
