import zipfile
import os


def Myzip(path):
    def zipDir(dirpath, outFullName):
        zip = zipfile.ZipFile(outFullName, 'w', zipfile.ZIP_DEFLATED)
        for path, _, fileList in os.walk(dirpath):
            relativePath = path.replace(dirpath, '')
            for filename in fileList:
                zip.write(os.path.join(path, filename),
                          os.path.join(relativePath, filename))
        zip.close()

    folderList = os.listdir(path)

    for folder in folderList:
        if path[-1] == '\\':
            dirpath = path + folder
        else:
            dirpath = path + '\\' + folder
        outFullName = dirpath + '.zip'
        zipDir(dirpath, outFullName)
