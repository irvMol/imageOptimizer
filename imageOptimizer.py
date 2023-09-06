import os
import os.path
from PIL import Image, ImageOps
import tkinter as tk
from tkinter import filedialog, IntVar


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

    for i, file in enumerate(os.listdir(img_dir)):
        cur_img_path = os.path.join(img_dir, file)
        if rename_option and project_name not in file:
            new_img_path = rename_image(cur_img_path, project_name, i, img_dir)
            if new_img_path:
                print(f"Renamed {file} to {os.path.basename(new_img_path)}")
        elif resize_option:
            try:
                resized_img = resize_image(cur_img_path, percent)
                if resized_img:
                    new_img_path = os.path.join(
                        img_dir, f"{project_name}{i}.jpg")
                    resized_img.save(new_img_path, optimize=True, quality=85)
                    print(
                        f"Resized {file} and saved to {os.path.basename(new_img_path)}")
            except IOError:
                print("Wrong file type or error processing " + file)

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

percentage_label = tk.Label(window, text="Resize Percentage: ")
percentage_label.pack()

percentage_slider = tk.Scale(
    window, from_=1, to=125, orient="horizontal", length=200)
percentage_slider.set(50)
percentage_slider.pack()

process_button = tk.Button(
    window, text="Process Images", command=process_images)
process_button.pack()

result_label = tk.Label(window, text="")
result_label.pack()

# Initialize slider state
toggle_slider_state()

# Start the Tkinter main loop
window.mainloop()
