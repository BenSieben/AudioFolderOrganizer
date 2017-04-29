# Audio Folder Organizer
# Takes a directory filled with audio files as a command-line argument, and attempts to organize the files into
#   folders based on the artist name and album name in the metadata of the audio files
import argparse
import os
import re
import shutil
from tinytag import TinyTag

# Known audio file types list
KNOWN_AUDIO_FILE_TYPES = [
    ".mp3",
    ".wav",
    ".opus",
    ".flac",
    ".wma",
    ".m4a"
]
# Known illegal characters to have in a file name (on Windows, at least)
FILENAME_ILLEGAL_CHARS = ["<", ">", ":", "\"", "/", "\\", "|", "?", "*"]
for i in range(32):
    FILENAME_ILLEGAL_CHARS.append(chr(i))


# Checks if the given file name should be an audio file or not, based off
#   of the file extension the file_name has
def is_audio_file(file_name):
    for audio_file_type in KNOWN_AUDIO_FILE_TYPES:
        if file_name.rfind(audio_file_type) == len(file_name) - len(audio_file_type):
            return True
    return False


# Takes the given input string, and tries to filter out any characters which
#   are illegal to have in a filename, such as "\" or """
def filter_filename_illegal_chars(input_str):
    # Filter out single-bad characters
    filtered_str = u""
    for c in input_str:
        if c not in FILENAME_ILLEGAL_CHARS:
            filtered_str = filtered_str + c

    # Filter out some of the more complex patterns
    filtered_str = re.sub("\.(\.)+", "", filtered_str)  # Get rid of multiple periods next to each other
    return filtered_str


# Organizes Audio files in the given directory into folders based off of metadata artist name and album name
def organize_audio_files_in_folder(folder):
    # Check that given folder directory is valid (if not, quit program)
    try:
        everything_in_folder = os.listdir(folder)
    except BaseException as e:
        print(str(e))
        return

    # Loop through all audio files in the directory
    total_audio_files = 0
    moved_audio_files = 0
    for folder_item in everything_in_folder:
        folder_item_with_path = folder + "/" + folder_item
        # Make sure the current item is an audio file
        if os.path.isfile(folder_item_with_path) and is_audio_file(folder_item):
            # For the audio file, grab artist name and album name metadata
            audio_tag = TinyTag.get(folder_item_with_path)
            audio_file_artist = audio_tag.artist
            audio_file_album = audio_tag.album

            # Filter out any "bad" characters from artist name / album name
            cleaned_artist = filter_filename_illegal_chars(audio_file_artist)
            cleaned_album = filter_filename_illegal_chars(audio_file_album)

            # Compute paths to artist folder / album folder
            artist_path = folder + "/" + cleaned_artist
            album_path = artist_path + "/" + cleaned_album

            encountered_error = False  # Flag variable to keep track of when something goes wrong in path creation
            # Try to make the artist / album directories
            try:
                os.makedirs(artist_path)
            except OSError as e:
                if not os.path.isdir(artist_path):
                    print("WARNING: " + str(e) + "\nArtist name " + audio_file_album +
                          " could not be cleaned to a valid directory name")
                    encountered_error = True
            try:
                os.makedirs(album_path)
            except OSError as e:
                if not os.path.isdir(album_path):
                    print("WARNING: " + str(e) + "\nAlbum name " + audio_file_artist +
                          " could not be cleaned to a valid directory name")
                    encountered_error = True

            # If there were no errors in folder creation, move audio to the organized folder and increment moved counter
            if not encountered_error:
                destination = (album_path + "/" + folder_item)
                print("Moving " + folder_item + " to " + (album_path + "/" + folder_item))
                shutil.move(folder_item_with_path, destination)
                moved_audio_files = moved_audio_files + 1
            total_audio_files = total_audio_files + 1

    print("Done! " + str(moved_audio_files) + " out of " + str(total_audio_files) + " detected audio files were moved")


# Main method of the script, which checks user input for validity and runs the script
#   if everything seems to be properly set up
def main():
    # Read in folder to organize
    parser = argparse.ArgumentParser()
    parser.add_argument("audio_folder")
    args = parser.parse_args()
    root_folder = args.audio_folder

    # Organize the audio files in the given folder
    organize_audio_files_in_folder(root_folder)

main()
