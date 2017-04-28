# MP3 Folder Organizer
# Takes a directory filled with MP3 files as a command-line argument, and attempts to organize the files into
#   folders based on the artist name and album name in the metadata of the MP3 files
import argparse
import eyed3
import os
import shutil


# Takes the given input string, and tries to filter out any characters which
#   are illegal to have in a filename, such as "\" or """
def filter_filename_illegal_chars(input_str):
    filename_illegal_chars = ["<", ">", ":", "\"", "/", "\\", "|", "?", "*"]
    filtered_str = ""
    for c in input_str:
        if c not in filename_illegal_chars:
            if c > 31:  # Character also cannot be in range 0 through 31 besides not being listed illegal characters
                filtered_str = filtered_str + c
    return filtered_str


# Organizes MP3 files in the given directory into folders based off of metadata artist name and album name
def organize_mp3s_in_folder(folder):
    try:
        # Loop through all MP3 files in the directory
        everything_in_folder = os.listdir(folder)
        print(str(everything_in_folder))

        for folder_item in everything_in_folder:
            folder_item_with_path = folder + "/" + folder_item
            # Make sure the current item is a .mp3 file
            if os.path.isfile(folder_item_with_path) and \
                    folder_item_with_path.rfind(".mp3") == len(folder_item_with_path) - 4:
                # For the MP3 file, grab artist name and album name metadata, filter out any special
                #   characters that would result in illegal file name, then move file to the new subdirectory
                print(folder_item_with_path)
                mp3_file = eyed3.load(folder_item_with_path)
                mp3_file_artist = mp3_file.tag.artist
                mp3_file_album = mp3_file.tag.album
                print(mp3_file_artist + "/" + mp3_file_album)
    except StandardError, e:
        print str(e)


# Main method of the script, which checks user input for validity and runs the script
#   if everything seems to be properly set up
def main():
    # Read in folder to organize
    parser = argparse.ArgumentParser()
    parser.add_argument("mp3_folder")
    args = parser.parse_args()
    root_folder = args.mp3_folder

    # Organize the MP3 files in the given folder
    eyed3.log.setLevel("ERROR")  # Set log level to ERROR to avoid WARNING messages from appearing in output
    organize_mp3s_in_folder(root_folder)

main()
