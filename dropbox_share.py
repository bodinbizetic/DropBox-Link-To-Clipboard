from dropbox_wrapp import DropBox
from token_loader import loadToken
from os.path import basename
import os
import shutil
import zipfile
import sys
import pyperclip
import ctypes

token_path = "token.txt"

class PathDoesNotExists(Exception):
    pass

class File:

    def __init__(self, path):
        if os.path.exists(path) == False:
            raise PathDoesNotExists()
        self.path = path


    def ReadBuffer(self):
        with open(self.path, "rb") as file:
            return file.read()

    def GetName(self):
        return basename(self.path)

    def Zip(self):
        if os.path.isdir(self.path):
            return self._ZipFolder()
        else:
            return self._ZipFile()

    def Delete(self):
        if os.path.isdir(self.path):
            return self._DeleteFolder()
        else:
            return self._DeleteFile()

    def _ZipFile(self):
        name = os.path.split(os.path.splitext(self.path)[0])[1] + ".zip"
        zipf = zipfile.ZipFile(name, 'w', zipfile.ZIP_DEFLATED)
        zipf.write(self.path)
        zipf.close()
        return File(name)

    def _ZipFolder(self):
        new_path = os.path.split(self.path)[1]
        shutil.make_archive(new_path, 'zip', self.path)
        return File(new_path + ".zip")

    def _DeleteFile(self):
        os.remove(self.path)

    def _DeleteFolder(self):
        shutil.rmtree(self.path)


def UploadToDropBox(path):
    dp = DropBox(loadToken("token.txt"))
    input_file = File(path)
    zipFile = input_file.Zip()
    dp.UploadFile(zipFile)
    link = dp.GetLink(zipFile.GetName())
    zipFile.Delete()
    return link


def main():
    link = ""
    if len(sys.argv) > 1:
        link = UploadToDropBox(sys.argv[1])
    else:
        path = input("Input path\n>>> ")
        link = UploadToDropBox(path)
    print(link)
    pyperclip.copy(link)
    ctypes.windll.user32.MessageBoxW(0, "Upload done!", "Done", 1)



if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        input("Press any key to continue...")
