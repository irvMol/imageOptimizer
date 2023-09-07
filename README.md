````markdown
# imageOptimizer

imageOptimizer is a simple Python application with a graphical user interface (GUI) that allows users to rename and/or resize a batch of images within a selected directory. This tool is especially useful for tasks like organizing and preparing images for various projects. I use it a lot during web design or making thumbnails.

## Features

- Rename images by appending a project name and an index to the original file names.
- Resize images by specifying a percentage of the original dimensions. Can Resize up to 125%.
- Option to choose between renaming, resizing, or both.
- Ability to process images in bulk within a selected directory.
- User-friendly GUI for easy interaction.
- Ability to dynamically create thumbnails.

## Requirements

- Python 3.x
- Tkinter (Python's standard GUI library)
- Pillow (Python Imaging Library, required for image processing)

## How to Use

1. Clone or download this repository to your local machine.

2. Install the required Python libraries if you haven't already, preferably in a virtual environment:

   ```bash
   pip install pillow
   ```
````

3. Run the `imageOptimizer.py` script:

   ```bash
   python imageOptimizer.py
   ```

4. Use the GUI to perform the following steps:

   - Enter the project name in the "Project Name" field.
   - Check the "Rename Images" checkbox to enable renaming if needed.
   - Check the "Resize Images" checkbox to enable resizing if needed.
   - Use the slider to set the desired resize percentage (if resizing is enabled).
   - Click the "Process Images" button to initiate the image processing.

5. Select a directory containing the images you want to process using the file dialog that appears.

## License

imageOptimizer is open-source software released under the [MIT License](LICENSE). You are free to use, modify, and distribute it as per the terms of the license.

## Author

Irving Moliina

If you encounter any issues or have suggestions for improvement, please feel free to [create an issue](https://github.com/irvMol/imageOptimizer/issues) on GitHub.

Happy image processing!
