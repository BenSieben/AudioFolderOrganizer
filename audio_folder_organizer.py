# MP3 Folder Organizer
# Takes a directory filled with MP3 files as a command-line argument, and attempts to organize the files into
#   folders based on the artist name and album name in the metadata of the MP3 files
import argparse
import eyed3
import os
import re
import shutil


# Takes the given input string, and tries to filter out any characters which
#   are illegal to have in a filename, such as "\" or """
def filter_filename_illegal_chars(input_str):
    # Filter out single-bad characters
    filename_illegal_chars = ["<", ">", ":", "\"", "/", "\\", "|", "?", "*"]
    filtered_str = u""
    for c in input_str:
        if c not in filename_illegal_chars:
            if c > 31:  # Character also cannot be in range 0 through 31 besides not being listed illegal characters
                filtered_str = filtered_str + c

    # Filter out some of the more complex patterns
    filtered_str = re.sub("\.(\.)+", "", filtered_str)  # Get rid of multiple periods next to each other
    return filtered_str


# Organizes MP3 files in the given directory into folders based off of metadata artist name and album name
def organize_mp3s_in_folder(folder):
    # Check that given folder directory is valid (if not, quit program)
    try:
        everything_in_folder = os.listdir(unicode(folder))  # Unicode to list items with Unicode encoding
    except StandardError, e:
        print str(e)
        return

    # Loop through all MP3 files in the directory
    for folder_item in everything_in_folder:
        folder_item_with_path = folder + "/" + folder_item
        # Make sure the current item is a .mp3 file
        if os.path.isfile(folder_item_with_path) and \
                (folder_item_with_path.rfind(".mp3") == len(folder_item_with_path) - 4):
            # For the MP3 file, grab artist name and album name metadata
            mp3_file = eyed3.load(folder_item_with_path)
            mp3_file_artist = unicode(mp3_file.tag.artist)
            mp3_file_album = unicode(mp3_file.tag.album)

            # Filter out any "bad" characters from artist name / album name
            cleaned_artist = filter_filename_illegal_chars(mp3_file_artist)
            cleaned_album = filter_filename_illegal_chars(mp3_file_album)

            # Compute paths to artist folder / album folder
            artist_path = folder + "/" + cleaned_artist
            album_path = artist_path + "/" + cleaned_album

            encountered_error = False  # Flag variable to keep track of when something goes wrong in path creation
            # Try to make the artist / album directories
            try:
                os.makedirs(artist_path)
            except OSError, e:
                if not os.path.isdir(artist_path):
                    print "WARNING: " + str(e) + "\nArtist name " + mp3_file_album + \
                          " could not be cleaned to a valid directory name"
                    encountered_error = True
            try:
                os.makedirs(album_path)
            except OSError, e:
                if not os.path.isdir(album_path):
                    print "WARNING: " + str(e) + "\nAlbum name " + mp3_file_artist + \
                          " could not be cleaned to a valid directory name"
                    encountered_error = True

            # If there were no errors in folder creation, move MP3 to the organized folder
            if not encountered_error:
                destination = (album_path + "/" + folder_item)
                print "Moving " + folder_item + " to " + (album_path + "/" + folder_item)
                shutil.copy2(folder_item_with_path, destination)


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
