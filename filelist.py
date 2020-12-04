import os
import pathlib
filelist = []
outF = open("filelist.txt", "w")
path = pathlib.Path('G:\MMDB\Filme')
print(path)
for root, dirs, files in os.walk(path, topdown=False):
    for name in files:
        filename = ""
        for char in name:
            if char.isalnum():
                filename += char
            else:
                if filename.endswith('.'):
                    pass
                else:
                    filename += "."
        outF.write(filename)
        outF.write("\n")
        filelist.append(filename)
print(filelist)
outF.close()
   #for name in dirs:
    #  print(os.path.join(root, name))
