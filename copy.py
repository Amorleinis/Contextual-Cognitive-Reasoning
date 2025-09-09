import os
import zipfile

# Root folder of your workspace
workspace_root = r"C:\Users\allue\OneDrive\Desktop\contextual_reasoning_v1.2"

# Output zip file
output_zip = r"C:\Users\allue\OneDrive\Desktop\contextual_reasoning_workspace.zip"

def zipdir(path, ziph):
    # Zip all files and folders in path
    for root, dirs, files in os.walk(path):
        for file in files:
            abs_file_path = os.path.join(root, file)
            # Save relative path inside zip
            rel_path = os.path.relpath(abs_file_path, os.path.join(path, '..'))
            ziph.write(abs_file_path, rel_path)

with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipdir(workspace_root, zipf)

print(f"Workspace zipped successfully into: {output_zip}")
