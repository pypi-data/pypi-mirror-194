import os
import shutil


def replace_text_in_files(directory, old_text, new_text):
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            file_path = subdir + os.sep + file
            ex = file.split(".")[-1]
            if ex not in ["ico", "png", "jpg", "jfif", "jpeg", "gif", "pyc"]:
                with open(file_path, "r") as f:
                    filedata = f.read()
                newdata = filedata.replace(old_text, new_text)
                with open(file_path, "w") as f:
                    f.write(newdata)


def replace_folder_name(root_dir, old_name, new_name):
    for path, dirs, files in os.walk(root_dir):
        for dir_ in dirs:
            if dir_ == old_name:
                old_path = os.path.join(path, old_name)
                new_path = os.path.join(path, new_name)
                os.rename(old_path, new_path)


def replace_file_name(current_file_name, new_file_name, current_dir):
    old_folder_path = os.path.join(current_dir, current_file_name)
    new_folder_path = os.path.join(current_dir, new_file_name)

    shutil.move(old_folder_path, new_folder_path)
