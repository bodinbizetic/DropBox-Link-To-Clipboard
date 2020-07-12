import dropbox

class DropBoxFileNotFound(Exception):
    pass

class DropBox:

    def __init__(self, token):
        self.dropbox = dropbox.Dropbox(token)
    
    def UploadFile(self, file):
        name = file.GetName()
        if name != "":
            name = "/" + name
        self.dropbox.files_alpha_upload(file.ReadBuffer(), name)

    def GetLink(self, fileName):
        all_files = self.dropbox.files_list_folder("")
        url = ""
        for dFile in all_files.entries:
            if dFile.name == fileName:
                url_obj = self.dropbox.sharing_create_shared_link(dFile.path_lower)
                url = url_obj.url
                break
        if url == "":
            raise FileNotFoundError()
        return url
