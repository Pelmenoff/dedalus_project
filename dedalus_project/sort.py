import sys, shutil
from pathlib import Path
from normalize import normalize


CATEGORIES = {"Images": [".jpeg", ".png", ".jpg", ".svg", ".apng", ".avif", ".gif", ".jfif", ".pjpeg", ".pjp", ".svg", ".webp"],
              "Video": [".mp4", ".mov", ".avi", ".mkv", ".webm", ".flv", ".vob", ".ogg"],
              "Documents": [".docx", ".txt", ".pdf", ".doc", ".xlsx", ".pptx"],
              "Audio": [".mp3", ".aiff", ".ogg", ".wav", ".amr"],
              "Archives": [".zip", ".tar", ".gz"]}


def move_file(file: Path, root_dir: Path, categorie: str) -> None:
    target_dir = root_dir.joinpath(categorie)
    if not target_dir.exists():
        target_dir.mkdir()
    file.replace(target_dir.joinpath(f"{normalize(file.stem)}{file.suffix}"))


def delete_empty_folders(path: Path) -> None:
    for item in reversed(list(path.glob("**/*"))):
        if item.is_dir() and not any(item.iterdir()):
                item.rmdir()


def get_categories(file: Path) -> str:
    ext = file.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Other"

def get_known_extensions() -> set:
    known_extensions = set()
    for exts in CATEGORIES.values():
        known_extensions.update(exts)
    return known_extensions

def get_known_extensions_in_folder(path: Path) -> set:
    known_extensions = get_known_extensions()
    extensions_in_folder = set()
    for item in path.glob("**/*"):
        if item.is_file():
            ext = item.suffix.lower()
            if ext in known_extensions:
                extensions_in_folder.add(ext)
    return extensions_in_folder

def get_unknown_extensions(path: Path) -> set:
    known_extensions = get_known_extensions()
    unknown_extensions = set()
    for item in path.glob("**/*"):
        if item.is_file() and item.suffix.lower() not in known_extensions:
            unknown_extensions.add(item.suffix.lower())
    return unknown_extensions


def unpack_archive(path: Path, sort: bool) -> None:
    for item in path.glob("**/*"):
        if item.is_file():
            file_ext = item.suffix.lower()
            for cat, exts in CATEGORIES.items():
                if file_ext in exts and cat == "Archives":
                    archive_folder_name = item.stem
                    unpack_path = item.parent / archive_folder_name
                    unpack_path.mkdir(exist_ok=True)
                    shutil.unpack_archive(str(item), extract_dir=str(unpack_path))
                    if sort:
                        sort_folder(unpack_path)
                        delete_empty_folders(unpack_path)
                        print(f"/// {item} - unpacked and sorted")
                    if sort is False:
                        print(f"/// {item} - unpacked")


def sort_folder(path: Path) -> None:
    for item in path.glob("**/*"):
        if item.is_file():
            cat = get_categories(item)
            move_file(item, path, cat)


def main():
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return "/// No path to folder"
    
    if not path.exists():
        return f"/// Folder {path} not found."

    confirmation = input(f"/// Are you sure you want to sort the files in folder {path}? (Y - Yes, N - No) >>> ")
    if confirmation.lower() != "y":
        return "/// Sorting aborted."

    sort_folder(path)
    print(f"/// [{path}] \n/// Sorted")
    delete_empty_folders(path)
    print("/// Empty folders deleted")
    wait_sort = True

    while wait_sort:
        sort = input("/// Sort unpacked archives? (Y - Yes, N - No) >>> ")
        if sort == "Y" or sort == "y":
            sort = True
            unpack_archive(path, True)
            wait_sort = False
        elif sort == "N" or sort == "n":
            sort = False
            unpack_archive(path, False)
            wait_sort = False
    
    files = {cat: [] for cat in CATEGORIES}
    for cat, ext in CATEGORIES.items():
        cat_dir = path.joinpath(cat)
        if cat_dir.exists():
            f = [file.name for file in cat_dir.glob("*")]
            files[cat] = f

    print("/// Files in each category:")
    for cat, files in files.items():
        print(f"/// {cat}: {files}")

    known_extensions = get_known_extensions_in_folder(path)
    print("/// \n/// Known Extensions:")
    print(f"/// {known_extensions}")

    unknown_extensions = get_unknown_extensions(path)
    print("/// \n/// Unknown Extensions:")
    print(f"/// {unknown_extensions}")


if __name__ == "__main__":
    main()