import os
import re
import shutil
import logging

# -------- DEFINE GLOBAL VARIABLES 
# Destination Directories (jekyll project folder)
DEST_BASE = "/Users/s/11_code/smaroukis.github.io"
DEST_POSTS = os.path.join(DEST_BASE, "_posts") # where the converted files will go
DEST_IMG = os.path.join(DEST_BASE, "assets", "img") # where the images will be copied to

# Source Directories (e.g. Obsidian vault)
SRC_BASE = "/Users/s/Library/Mobile Documents/iCloud~md~obsidian/Documents/Genesis/"
SRC_SUBDIR_POSTS = "01-99_Personal/30-49_Projects-Personal/40-blog/_posts"
SRC_SUBDIR_IMG = "z_attachments" # top level directory where the images are stored, script will search subdirectories

SRC_POSTS = os.path.join(SRC_BASE, SRC_SUBDIR_POSTS)
SRC_IMG = os.path.join(SRC_BASE, SRC_SUBDIR_IMG)

# Setup logging
LOG_FILE = os.path.join(os.getcwd(), "error.log")
logging.basicConfig(filename = LOG_FILE, level=logging.DEBUG)

### ------- IMAGE REGEX MATCHING ------------

# summary:: matches wiki link style filename with or without pipe character
# returns: match object
def match_line(content):
    # wiki_img_filename
    pattern_wiki = r"!\[\[(.*?)(?:\|(.*))?\]\]"
    if match := re.search(pattern_wiki, content):
        if re.search(r'\.(?:jpg|jpeg|png|gif)', match.group(1)):
            match_type = "wiki_img_filename"
            return (match_type, match)
        #else:
            #match_type = "wiki_page_filename"
            #TODO: convert reference to wiki page to valid jekyll link
    
    # md_img_filename
    pattern_markdown = r"!\[(.*)\]\((.*)\)"
    if match := re.search(pattern_markdown, content):
        if re.search(r'\.(?:jpg|jpeg|png|gif)', match.group(2)):
            match_type = "md_img_filename"
            return (match_type, match)
        #else:
            #match_type = "md_page_filename"
            #TODO: convert reference to wiki page to valid jekyll link
            # also handle aliases here
    
    match_type = "None"
    return (match_type, match)
    
    
#  valid inputs
# ![[image.png]] | ![[image.png | 300]] | ![[/long/path/to/image.png]] | ![[/long/path/to/image.png | 300]]
# nb. doesn't work for multiple images on a line
# requires: match from match_lines of type "wiki_img_filename"
# returns ["anything.png", "300"] or "anything.jpg"
def modify_wiki_img_filename(match):
    
    filename = match.group(1).strip() # handle whitespaces e.g. "![[image.png | 300]]"
    if '/' in filename:
        filename = filename.split('/')[-1]
    alt_text = filename.split('.')[0]
    # replace the filename with ![alt-text]
    result = f'![{alt_text}]({filename})'
    
    # special consideration for Obsidian style image resizing: `![[image.png | 300]]`
    if match.group(2):  
        # match.groups() returns ('first_match', None), so length is always two
        width = match.group(2).strip()
        result += f'{{: width="{width}"}}'
    
    # Find the image on the local machine and copy it to the output
    copy_image_wrapper(filename)
    
    return result + "\n"
        

# valid inputs
# ![](filename.png) | ![alt-text](filename.png) | ![alt-text](/path/to/filename.png) | ![alt-text with spaces.png](/path/to/filename.png)
def modify_md_img_filename(match):
    result = ''
    
    alt_text = match.group(1)
    filename = match.group(2)
    # strip /path/to/file to just file
    if '/' in filename:
        filename = filename.split('/')[-1]
    if '/' in alt_text:
        alt_text = alt_text.split('/')[-1]
    result = f"![{alt_text}]({filename})"
    
    # Find the image on the local machine and copy it to the output
    copy_image_wrapper(filename)
    
    return result + "\n"

### -------- IMAGE COPYING -----------

# Requires global variables SRC_IMG and DEST_IMG
def copy_image_wrapper(filename):
    try:
        copy_image(filename, SRC_IMG, DEST_IMG)
    except Exception as e:
        logging.error(e)

# Given a filename, Walks the source directory and copies the first match to the destination
# Logs all copy actions to the log file
def copy_image(filename, source_dir, dest_dir):
    # Check if the destination directory exists, if not create it
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
   
    # Search for the file in the source directory and all subdirectories
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file == filename:
                # File found, copy it to the destination directory
                src_path = os.path.join(root, file)
                dest_path = os.path.join(dest_dir, file)
                shutil.copy2(src_path, dest_dir)
                logging.info(f"Moved file in src=['{src_path}'] to dest=['{dest_path}'])")
                return
    # If the file is not found, raise an error
    raise FileNotFoundError(f"{filename} not found in {source_dir}")
    
    
# ----- Other utilities -------

# Get all markdown files in current working directory
def get_md_files(dir):
    try: 
        files = os.listdir(dir)
    except FileNotFoundError as e:
        logging.error(e)
        raise

    md_files = [file for file in files if file.endswith('.md')]
    n_files = len(md_files)
    
    if n_files == 0:
        logging.info("No markdown files found")
        print("No markdown files found")
        exit()

    print(f"Found {n_files} markdown files:")
    logging.info(f"Found {n_files} markdown files:")
    for item in md_files:
            print("\t" + item)
    
    return md_files
    
    
### ------- MAIN --------------


def main():

    # ------ BEGIN MAIN
    # Get Files
    logging.info(" \n\n --------- Starting Script --------- ")
    logging.info(" Provided paths:")
    logging.info(f"\n\tSRC_POSTS: {SRC_POSTS}" + f"\n\tSRC_IMG: {SRC_IMG}" + f"\n\tDEST_IMG: {DEST_IMG}" + f"\n\tDEST_POSTS: {DEST_POSTS}")
    md_files = get_md_files(SRC_POSTS)

    for filename in md_files:

        input_filepath = os.path.join(SRC_POSTS, filename)
        output_filepath = os.path.join(DEST_POSTS, filename)

        # for line in file
        print("Reading file: \n\t" + input_filepath)
        logging.info("Reading file: \n\t" + input_filepath)
        with open(input_filepath, 'r') as f:
            lines = f.readlines()

        # dictionary of line modification functions
        # keys should match result of match_line()
        # value is the function that modifies the line
        modify_fmap = {
            "wiki_img_filename": modify_wiki_img_filename,
            "md_img_filename": modify_md_img_filename,
            # other match types
            #"md_page_filename": modify_md_page_filename,
            #"wiki_page_filename": modify_wiki_page_filename
        }

        # create output file
        print("Writing to output file: \n\t" + output_filepath)
        logging.info(f"Writing to output file: \n\t" + output_filepath)
        with open(output_filepath, 'w') as f:
            in_code_block = False
            for line in lines:
                # skip code blocks
                if line.startswith("```"):
                    in_code_block = not in_code_block
                elif in_code_block:
                    f.write(line) 
                    continue
                # check for matches
                match_type, match = match_line(line)
                if match:
                    if modify_func := modify_fmap.get(match_type):
                        new_line = modify_func(match)
                # else just copy as is
                else:
                    new_line = line
                f.write(new_line)

    
### ----- RUN ONLY FROM COMMAND LINE -------
if __name__ == "__main__":
    main()
