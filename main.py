# checkDuplicates.py
# Python 2.7.6

"""
Given a folder, walk through all files within the folder and subfolders
and get list of all files that are duplicates
The md5 checcksum for each file will determine the duplicates
"""

import os
import hashlib
from collections import defaultdict
import csv

#src_folder = "C:\\Temp\\test_dupl"
src_folder = "E:\\Fotos_early"

class fileProps:
    def __init__(self,filename,size,dir):
        self.filename=filename
        self.ext=filename.split(".")[-1].lower()
        self.size=size
        self.dir=dir
        self.fullpath = dir + "\\" + filename
    # filename = ""
    # size = 0
    # ext = ""
    # dir = ""
    # fullpath = ""

class dirProps:
    def __init__(self,filename,size,dirs):
        self.filename=filename
        self.size=size
        self.dirs = dirs
    # filename = ""
    # filesize = 0
    # dirs = {}


def number_of_files_in_a_folder(dir):
    """
    Function returns the number of files in a directory
    """
    onlyfiles = next(os.walk(dir))[2]  # dir is your directory path as string
    return len(onlyfiles)

def generate_md5(fname, chunk_size=1024):
    """
    Function which takes a file name and returns md5 checksum of the file
    """
    hash = hashlib.md5()
    with open(fname, "rb") as f:
        # Read the 1st block of the file
        chunk = f.read(chunk_size)
        # Keep reading the file until the end and update hash
        while chunk:
            hash.update(chunk)
            chunk = f.read(chunk_size)

    # Return the hex checksum
    return hash.hexdigest()

def get_file_size(abspath):
    return os.path.getsize(abspath)

def generate_filename_with_filesize(abspath):
    size = get_file_size(abspath)
    filename = abspath.rsplit("\\", 1)[1]
    return filename+"_"+str(size)


if __name__ == "__main__":
    """
    Starting block of script
    """

    # The dict will have a list as values
    md5_dict = defaultdict(list)
    filesize_dict = defaultdict(list)

    ## file_types_inscope = ["ppt", "pptx", "pdf", "txt", "html",
    ##                       "mp4", "jpg", "png", "xls", "xlsx", "xml",
    ##                       "vsd", "py", "json"]

    # file_types_inscope = ["csv", "ps1", "wdl"]

    # Walk through all files and folders within directory and append all files to filesize_dict
    # filesize_dict (file_id, fileProps) where file_id=filename+_+filesize
    # fileProps contains [filename, file-size, file-extention, folder-path, full-path (folder-path+file-name)]
    for path, dirs, files in os.walk(src_folder):
        print("Analyzing {}".format(path))
        for each_file in files:
            #if each_file.split(".")[-1].lower() in file_types_inscope:
                # The path variable gets updated for each subfolder
                dir = os.path.abspath(path)
                fullpath = os.path.join(dir, each_file)
                # If there are more files with same id append to list
                filesize_dict[generate_filename_with_filesize(fullpath)].append(fileProps(each_file,get_file_size(fullpath),dir))

    # folders_dic (folder, [folderProps]) is a dictionary which match each folder to a collection of files which were found as a dublicates in previous step
    # each file is represented as a folderProps object where the filename is only one property: [filename, filesize, [Set of folders]]
    # [Set of folders] which correspond to each file are actually the folders were this file was found as a dublicate
    folders_dic = defaultdict(list)

    # Walk through all the files from previous step and put to folders_dic only ones where the number of folders is more than 1 (file is located in more than 1 folder)
    for value in filesize_dict.values():
        if len(value) > 1:
            for item in value:
                dir = item.dir
                filename=item.filename
                size=item.size
                dirs_obj=value.copy()
                dirs_obj.remove(item)
                dirs=list()
                for each_dir in dirs_obj: dirs.append(each_dir.dir)
                folders_dic[dir].append(dirProps(filename,size,dirs))
                # Should append not only filename but [(Filename,Filesize,[List of other folders])]  List of other folders=value.exclude(item)
                # So every folder will have info on dublicate files (with sizes). Each dubplicate file will have info in which folders it also located
                # By multiplying filesize on the the length of list of othe folders list = possible free space to get after removing duplicates
                # SUM all such multiplies and you get total space occupied by dublicates.

    input()

    with open("duplicates.csv", "w") as log:
        # Lineterminator added for windows as it inserts blank rows otherwise
        csv_writer = csv.writer(log, quoting=csv.QUOTE_MINIMAL, delimiter=",",
                                lineterminator="\n")
        header = ["Duplicates of "+src_folder+" grouped by Folders"]
        csv_writer.writerow(header)

        for key in folders_dic:
            # print(key, " -> ", folders_dic[key]," Duplicates: ", len(folders_dic[key])," from ",number_of_files_in_a_folder(key)," files in a folder")
            percent_of_duplicates = str(
                "{:,.2f}".format(len(folders_dic[key]) * 100 / number_of_files_in_a_folder(key))) + "%"
            row = ["%s -> %s of dublicates: %d from %d files in a folder" % (key,percent_of_duplicates,len(folders_dic[key]),number_of_files_in_a_folder(key))]
            row2 = [""]
            #row = key," -> ",percent_of_duplicates," of Duplicates: ",str(len(folders_dic[key]))," from ",str(number_of_files_in_a_folder(key))," files in a folder"
            #row = " ".join([key,"->",percent_of_duplicates,"of Duplicates:",str(len(folders_dic[key])),"from",str(number_of_files_in_a_folder(key)),"files in a folder"])
            print(row)
            csv_writer.writerow(row)


    print("Done")
