import os


def make_sure_path_exists(path: str, ignore_extension: bool = False) -> None:
    path = os.path.dirname(path) if not ignore_extension and len(path.split(".")) > 1 else path

    root = "/"
    dirs = path.split("/")[1:]
    for directory in dirs:
        section = os.path.join(root, directory)
        root = section
        if not os.path.isdir(section) and not os.path.isfile(section):
            os.mkdir(section)
