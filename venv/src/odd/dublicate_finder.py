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

def generate_filename_with_filesize(abspath):
    size = os.path.getsize(abspath)
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

    file_types_inscope = ["csv", "ps1", "wdl"]

    # Walk through all files and folders within directory
    for path, dirs, files in os.walk(src_folder):
        print("Analyzing {}".format(path))
        for each_file in files:
            #if each_file.split(".")[-1].lower() in file_types_inscope:
                # The path variable gets updated for each subfolder
                file_path = os.path.join(os.path.abspath(path), each_file)
                # If there are more files with same checksum append to list
                #md5_dict[generate_md5(file_path)].append(file_path)
                filesize_dict[generate_filename_with_filesize(file_path)].append(file_path)

    # # Identify keys (checksum) having more than one values (file names)
    # duplicate_files = (
    #     val for key, val in md5_dict.items() if len(val) > 1)
    #
    # # Write the list of duplicate files to csv file
    # with open("duplicates.csv", "w") as log:
    #     # Lineterminator added for windows as it inserts blank rows otherwise
    #     csv_writer = csv.writer(log, quoting=csv.QUOTE_MINIMAL, delimiter=",",
    #                             lineterminator="\n")
    #     header = ["File Names"]
    #     csv_writer.writerow(header)
    #
    #     for file_name in duplicate_files:
    #         csv_writer.writerow(file_name)

    # for key in filesize_dict:
    #     if len(filesize_dict[key]) > 1: print(key, " -> ", filesize_dict[key])
    #
    # for key in md5_dict:
    #     if len(md5_dict[key]) > 1: print(key, " -> ", md5_dict[key])

    folders_dic = defaultdict(list)
    for value in filesize_dict.values():
        if len(value) > 1:
            for item in value:
                abspath = item.rsplit("\\",1)[0]
                filename = item.rsplit("\\",1)[1]
                folders_dic[abspath].append(filename)
                # Should append not only filename but [(Filename,Filesize,[List of other folders])]  List of other folders=value.exclude(item)
                # So every folder will have info on dublicate files (with sizes). Each dubplicate file will have info in which folders it also located
                # By multiplying filesize on the the length of list of othe folders list = possible free space to get after removing duplicates
                # SUM all such multiplies and you get total space occupied by dublicates.



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
            #row = key," -> ",percent_of_duplicates," of Duplicates: ",str(len(folders_dic[key]))," from ",str(number_of_files_in_a_folder(key))," files in a folder"
            #row = " ".join([key,"->",percent_of_duplicates,"of Duplicates:",str(len(folders_dic[key])),"from",str(number_of_files_in_a_folder(key)),"files in a folder"])
            print(row)
            csv_writer.writerow(row)


    print("Done")
