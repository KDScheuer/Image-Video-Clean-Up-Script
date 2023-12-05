import os
import datetime
import shutil
import getpass

PHOTO_EXTENSIONS = (".JPG", ".JPEG", ".PNG", ".HEIC")
VIDEO_EXTENSIONS = (".MP4", ".MOV")

MONTHS = {
    1: "1. January",
    2: "2. February",
    3: "3. March",
    4: "4. April",
    5: "5. May",
    6: "6. June",
    7: "7. July",
    8: "8. August",
    9: "9. September",
    10: "10. October",
    11: "11. November",
    12: "12. December"
}


def get_directory():
    """Gets the directory in which to recursively search for files"""
    user = getpass.getuser()
    source_directory = f"C:\\Users\\{user}\\OneDrive\\Pictures\\"
    while True:
        print(f"Source Directory: {source_directory}")
        user_auth = input("Does this path look correct (Y/N): ")
        if user_auth.upper() == "Y":
            print("Locating Images")
            return source_directory
        else:
            source_directory = input("Please Enter the Source Directory")


def file_enumeration(source_path):
    """Finds all files in the provided path and returns a list with the absolute paths"""
    photos, videos = [], []
    for root, dirs, files in os.walk(source_path):
        dirs[:] = [d for d in dirs if not len(d) == 4]
        for file in files:
            if file.upper().endswith(PHOTO_EXTENSIONS):
                photos.append(os.path.join(root, file))
            elif file.upper().endswith(VIDEO_EXTENSIONS):
                videos.append(os.path.join(root, file))
    print(f"Found {len(photos)} Photos and {len(videos)} Videos")
    return photos, videos


def get_date_taken(item_list):
    """Finds date last modified as not all photos have exif data, Returns a dict in {year: {month: file_path} format"""
    items = {}

    for item in item_list:
        creation_time = os.path.getmtime(item)
        creation_date = datetime.datetime.fromtimestamp(creation_time)
        year_key = int(creation_date.year)
        month_key = MONTHS[int(creation_date.month)]
        items.setdefault(year_key, {}).setdefault(month_key, []).append(item)

    return items


def create_dir_and_move_files(path, media_type, media):
    """Creates Directories as Year/Month/Photos or Videos in provided path and moves files"""
    for year_key, year_values in media.items():
        for month_key, values in year_values.items():
            new_path = os.path.join(path, str(year_key), str(month_key), media_type)
            os.makedirs(new_path, exist_ok=True)

            for value in values:
                try:
                    shutil.move(value, new_path)
                except Exception as e:
                    print(f"Error moving {value} {media_type}: {e}")


def main():

    source_path = get_directory()
    photos, videos = file_enumeration(source_path)

    photos_with_date = get_date_taken(photos)
    videos_with_date = get_date_taken(videos)

    print(photos_with_date)
    create_dir_and_move_files(source_path, "Photos", photos_with_date)
    create_dir_and_move_files(source_path, "Videos", videos_with_date)

    input("All Files Moved Press Any key to exit")


if __name__ == "__main__":
    main()
