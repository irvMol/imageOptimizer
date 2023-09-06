import os
import os.path
from PIL import Image, ImageOps
import tkinter as tk
from tkinter import filedialog

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

def process_images():
    project_name = project_name_entry.get()
    img_dir = filedialog.askdirectory(title="Select Image Directory")
    percent = int(percentage_slider.get())

    if not project_name or not img_dir:
        result_label.config(
            text="Please provide project name and select a directory.")
        return

    for i, file in enumerate(os.listdir(img_dir)):
        if project_name not in file:
            try:
                cur_img_path = os.path.join(img_dir, file)
                resized_img = resize_image(cur_img_path, percent)
                if resized_img:
                    new_img_path = rename_image(
                        cur_img_path, project_name, i, img_dir)
                    if new_img_path:
                        resized_img.save(
                            new_img_path, optimize=True, quality=85)
            except IOError:
                print("Wrong file type or error processing " + file)
        else:
            print("Project name found in file name. Skipping file.")

    result_label.config(text="Image processing complete.")

# Create the Tkinter window
window = tk.Tk()
window.title("Image Processing Tool")

# Create and arrange widgets
project_name_label = tk.Label(window, text="Project Name:")
project_name_label.pack()

project_name_entry = tk.Entry(window)
project_name_entry.pack()

percentage_label = tk.Label(window, text="Resize Percentage: ")
percentage_label.pack()

percentage_slider = tk.Scale(window, from_=1, to=100, orient="horizontal", length=200)
percentage_slider.set(50)
percentage_slider.pack()

process_button = tk.Button(
    window, text="Process Images", command=process_images)
process_button.pack()

result_label = tk.Label(window, text="")
result_label.pack()

# Start the Tkinter main loop
window.mainloop()