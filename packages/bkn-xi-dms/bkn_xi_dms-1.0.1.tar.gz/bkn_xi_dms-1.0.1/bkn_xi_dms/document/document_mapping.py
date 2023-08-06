import re
import os
text = "The quick brown fox jumps over the lazy dog"
# pattern = "2_IJAZAH SD_197212051999112001_1985.pdf"

# Use the search() function to find the first occurrence of the pattern in the text

# for keyval in list_jenis_dokument:
#     name = keyval["name"]
#     match = re.search(name.lower(), pattern.lower())

#     if match:
#         print(keyval["id"])
#         print(keyval["name"])
#     else:
#         print("Pattern not found")
#         doc = 0

# for keyval in list_jenis_dokument:
#     name = keyval["name"]
#     match = re.search(pattern.lower(), name.lower())
#     if match:
#         print(keyval["id"])
#         print(keyval["name"])
#     else:
#         print("Pattern not found")

list_jenis_dokument = []


def to_text(list, path):
    with open(path, 'w') as f:
        f.write('\n'.join(list))
        # pickle.dump(list, f)

    print("done file at the", path)


path_write = "C:\\Users\\Rifo\\Desktop\\output2.txt"
path_directory = "c:\\dmsUploadExperiment\\"

list_folder = os.listdir(path_directory)
list_files = []
for folder in list_folder:
    path_folder = os.path.join(path_directory + folder)
    list_document = os.listdir(path_directory + folder)

    for document in list_document:
        doc = 1
        for keyval in list_jenis_dokument:
            name = keyval["name"]

            if (re.search(name.lower(), document.lower())):
                print(name.lower() + "-" + document.lower())
                doc = 0
        if doc == 1:
            list_files.append(os.path.join(
                path_directory + folder + "\\" + document))
to_text(list_files, path_write)
