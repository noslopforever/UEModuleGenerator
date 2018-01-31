#!/usr/bin/python

import os
import sys
import getopt
import shutil

temporaryDir = "./_Temporary"

def copyTemplateToTemporary(InTemplatePath):
    try:
        shutil.rmtree(temporaryDir)
    except:
        # do nothing
        print "kill temporary error"
    shutil.copytree(InTemplatePath, temporaryDir)

def renameFileContent(InDir, InModuleName):
    print "-- read file content : ", InDir
    # rename file content
    fp = open(InDir)
    # get file content
    str = fp.read()
    fp.close()
    print "-- file readed!"

    # replace
    print "-- replace file content"
    newStr = str.replace("%MODULE_NAME%", InModuleName)

    print "-- open file for write"
    # write file
    fp = open(InDir, "w")
    # write file content
    fp.write(newStr)
    fp.close()
    print "-- file wrote!"

def renamePathes(InDir, InModuleName):
    # find files
    files = os.listdir(InDir)
    # rename file name
    for f in files:
        # old module name
        oldFilepath = InDir + '/' + f
        # get path status
        pathIsDir = os.path.isdir(oldFilepath)

        # get new name
        newName = f.replace("%MODULE_NAME%", InModuleName)
        newFilepath = InDir + '/' + newName
        # rename file
        os.rename(oldFilepath, newFilepath)
        # if dir, recursive
        if (pathIsDir):
            if (f[0] == '.'):
                pass
            else:
                renamePathes(newFilepath, InModuleName)
        else:
            # read file content and replace all %MODULE_NAME%
            renameFileContent(newFilepath, InModuleName)

def main(argv):
    moduleName='MODULE'
    templateDir='./Template'
    try:
        opts, args = getopt.getopt(argv, "ht:m:", ["template=", "module="])
    except getopt.GetoptError:
        print 'CreateNewModule -m <ModuleName> -t <TemplateDir>'
    for opt, arg in opts:
        if opt == '-h':
            print 'CreateNewModule -m <ModuleName> -t <TemplateDir>'
            sys.exit()
        elif opt in ("-m", "--module"):
            moduleName = arg
        elif opt in ("-t", "--template"):
            templateDir = arg
    print 'The new module is "', moduleName
    # copy to temporary
    copyTemplateToTemporary(templateDir)
    # rename pathes
    renamePathes(temporaryDir, moduleName)


if __name__ == '__main__':
    main(sys.argv[1:])