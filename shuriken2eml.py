#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse

class ShurikenConvert(object):
    __DELIMITTER = b"====================KeyABCabc0123456789XYZxyz-Mailer-MailBox-Delmit-Line-Do-Not-Edit-JustSystem====================\r\n"
    __srcDir = ""
    __srcFile = None

    def __iter__(self):
        return self

    def open(self, filename):
        self.__srcDir = os.path.dirname(filename)
        if len(self.__srcDir) == 0:
            self.__srcDir = "."
        self.__srcFile = open(filename, "rb") 
        self.__readFirstDelimitter = False

    def __next__(self):
        eml = bytes()
        for line in self.__srcFile:
            if line == self.__DELIMITTER:
                if self.__readFirstDelimitter == True:
                    return eml
                else:
                    self.__readFirstDelimitter = True
            else:
                eml = eml + line
        if len(eml) == 0:
            raise StopIteration()
        else:
            return eml
                
def convertSingleFile(mbxPath, outDir=""):
    outCount = 0
    srcDir = os.path.dirname(mbxPath)
    if len(srcDir) == 0:
        srcDir = "."

    convert = ShurikenConvert()
    convert.open(mbxPath)
    for eml in convert:
        outCount = outCount + 1
        outFile = open(srcDir + "\\" + str(outCount) + ".eml", mode="wb")
        outFile.write(eml)

def convertAllFiles(dirPath):
    for file in os.listdir(dirPath):
        if file.lower().endswith(".mbx"):
            os.makedirs(dirPath + "\\" + os.path.splitext(file)[0], exist_ok=True)
            convertSingleFile(dirPath + "\\" + file, os.path.splitext(file)[0] + "\\")

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("path", help="mbx file path or directory path (if -d is specified)")
    argparser.add_argument("-d", action="store_true", help="process all *.mbx files in the specified directory")
    args=argparser.parse_args()
    if args.d == True:
        convertAllFiles(args.path)
    else:
        convertSingleFile(args.path)

if __name__ == "__main__":
    main()
