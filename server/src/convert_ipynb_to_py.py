import os
import nbformat
from nbconvert import PythonExporter

def convert_notebook(notebook_path, output_folder):
    """Convert a single Jupyter Notebook (.ipynb) to a Python script (.py)."""
    if not notebook_path.endswith(".ipynb"):
        print(f"Skipping non-notebook file: {notebook_path}")
        return

    try:
        # Read the notebook
        with open(notebook_path, "r", encoding="utf-8") as f:
            notebook = nbformat.read(f, as_version=4)

        # Convert to Python script
        python_exporter = PythonExporter()
        python_script, _ = python_exporter.from_notebook_node(notebook)

        # Save as .py file in the output folder
        base_filename = os.path.basename(notebook_path).replace(".ipynb", ".py")
        py_filename = os.path.join(output_folder, base_filename)

        with open(py_filename, "w", encoding="utf-8") as f:
            f.write(python_script)

        print(f"✅ Converted '{notebook_path}' to '{py_filename}'")

    except FileNotFoundError:
        print(f"Error: File '{notebook_path}' not found.")

def convert_all_notebooks_in_folder(source_folder, output_folder):
    """Convert all Jupyter Notebooks in the source folder to Python scripts in the output folder."""
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through all files in the source folder
    for filename in os.listdir(source_folder):
        notebook_path = os.path.join(source_folder, filename)
        if os.path.isfile(notebook_path):
            convert_notebook(notebook_path, output_folder)

if __name__ == "__main__":
        source_folder = "."
        output_folder = "../public"
        convert_all_notebooks_in_folder(source_folder, output_folder)
