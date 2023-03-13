# TODO
# Effect: Given a folder or a filename (full path), for each file **copy** all the referenced images 
# into a specified folder (useful for moving files between vaults)

# Attachments folder nomenclature
# case: 
#   (default, single file) → attachements in new folder named `<filename>_attachments` in the same directory as the file
#   (default, folder) → attachments under `/path/to/folder/attachments`
#   (user-defined) → user gives folder name relative to where file/folder is located (don't need full path)

# Pseudocode
# Ask user for the source folder/file path → would be nice for a gui to open up an open file finder prompt
# Ask user for the user-defined attachement folder name, or create by default
# Ask user if there is a destination for the files 
    # note we will first copy the images referenced
    # in case other files are using them
    # but we will move the file requested
    # other **markdown files** mentioned won't be moved/copied
    # only the ones provided
