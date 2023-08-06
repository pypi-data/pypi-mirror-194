import os
from list_all_files_recursively import get_folder_file_complete_path


def delete_tmp_files():
    delfiles = []
    if g := os.environ.get("TEMP"):
        delfiles.append(g)
    if g := os.environ.get("TMP"):
        delfiles.append(g)
    delfiles = list(set(delfiles))
    delfiles = [x for x in delfiles if x]
    fi = get_folder_file_complete_path(folders=delfiles)
    for file in fi:
        try:
            os.remove(file.path)
        except Exception as fe:
            continue
