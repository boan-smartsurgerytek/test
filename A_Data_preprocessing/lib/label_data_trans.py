import time
import numpy as np
import json
import cv2
from os import listdir, mkdir
from os.path import isdir, join, splitext, isfile

"""
Transformation API for labeled data from SmartSurgery Labeling tool.
"""

class TransLabelNum(object):
    """
    Inputs-
    imgFolderPath: Root folder path include all sub label folders. Structure like:
        imgFolderPath \n
        ├─video1 \n
        │  └─img1_1.png \n
        │  └─img1_2.npy \n
        │  └─img1_3.json \n
        │  └─... \n
        └─video2 \n
        │  └─... \n
        ... \n
    
    saveFolderPath: Folder path of save transformed data.

    correctLabel: A list or a dictionary.\n
     If type of correctLabel is list, label data will be transformed num by the list order. (Background alawys be 0, list DO NOT include background.) \n
     If type of correctLabel is dictionary, the dictionary KEYS must be label names, VALUES must be numbers, label data will be transformed num by the specify num. (Background alawys be 0, list DO NOT include background.)
    
    saveType: Choose saving type after transformation. Only "Mask" or "Npy". Default Mask.
    """
    def __init__(self, imgFolderPath, saveFolderPath, correctLabel,imageType, saveType='Mask'):
        self.imgFolderPath = imgFolderPath
        self.saveFolderPath = saveFolderPath
        self.correctLabel = correctLabel
        self.saveType = saveType
        self.imageType = imageType
        self.labelDict = self.createLabelDict(self.correctLabel)
        self.showLabelDict()
        self.run()

    def run(self):
        for videoIdx in listdir(self.imgFolderPath):
            self.folderIDName = videoIdx
            time_start = time.time()
            self.folderPath = join(self.imgFolderPath, str(videoIdx))
            self.saveSubFolderPath = join(self.saveFolderPath, str(videoIdx))
            self.detectFolderExist(self.saveSubFolderPath)
            
            self.labelList = list(self.labelDict.keys())
            if self.labelList == []:
                print(self.saveSubFolderPath)
                continue
            if self.saveType == 'Mask':
                self.createImgMaskFolder(self.saveSubFolderPath)
            
            fileList = self.createUniFileList(self.folderPath)
            for fileName in fileList:
                jsonFilePath = join(self.folderPath, fileName+'.json')
                if not isfile(jsonFilePath):
                    print(jsonFilePath)
                    continue
                jsonFile = self.readJSONFile(fileName)
                img = self.readImg(fileName)
                nparray = self.readNpy(fileName)
                if img.size == 0 or nparray.size == 0:
                    continue
                correctedArray = self.createCorrectedArray(nparray, jsonFile)
                if correctedArray==[]:
                    continue
                if self.saveType == 'Mask':
                    self.saveImgMask(fileName, img, correctedArray)
                else:
                    self.saveImgNpy(fileName, img, correctedArray)

            time_end = time.time()
            print("Transform folder_{} cost {} sec. \n".format(videoIdx, round(time_end - time_start, 2)))
    
    def detectFolderExist(self, saveFolderPath):
        if isdir(saveFolderPath):
            pass
        else:
            mkdir(saveFolderPath)

    def createLabelDict(self, correctLabel):
        if type(correctLabel) == list:
            labelDict = dict()
            count = 1
            for label in correctLabel:
                labelDict[label] = count
                count += 1
        elif type(correctLabel) == dict:
            labelDict = correctLabel
        return labelDict
    
    def showLabelDict(self):
        print("Transform Label Dictionary:")
        for (className, labelNum) in self.labelDict.items():
            print("{}: {}".format(className, labelNum))
        print("-"*40+"\n")

    def createImgMaskFolder(self, saveSubFolderPath):
        imgFolderPath = join(saveSubFolderPath, 'image')
        maskFolderPath = join(saveSubFolderPath, 'mask')
        self.detectFolderExist(imgFolderPath)
        self.detectFolderExist(maskFolderPath)

    def createUniFileList(self, folderPath):
        fileList = listdir(folderPath)
        uniFileList = list( set( map(lambda x: splitext(x)[0], fileList) ) )
        if 'Thumbs' in uniFileList:
            uniFileList.remove('Thumbs')
        return uniFileList

    def readJSONFile(self, fileName):
        jsonFilePath = join(self.folderPath, fileName+'.json')
        try:
            with open(jsonFilePath, "r") as f:
                text = f.read()
        except IOError as er:
            print("Error: Json file load failed or Can not find the file path '{}'".format(er.filename))
        # jsonFile: Key-id, Value-class. The class might duplicate.
        jsonFile = json.loads(text)
        return jsonFile

    def readImg(self, fileName):
        imgPath = join(self.folderPath, fileName+'.'+self.imageType)
        try:
            img = cv2.imread(imgPath)
            np.dtype(img)
        except TypeError:
            pass
        else:
            print(f"Error: {fileName} {self.imageType} file load failed")
        return img

    def readNpy(self, fileName):
        npyPath = join(self.folderPath, fileName+'.npy')
        try:
            nparray = np.load(npyPath)
        except (IOError, FileNotFoundError) as er:
            print("Error: npy file load failed or Can not find the file path '{}'".format(er.filename))
        return nparray

    def createCorrectedArray(self, nparray, jsonFile):
        jsonClassList = list(jsonFile.values())
        jsonLabelStr = list(jsonFile.keys())
        jsonLabel = list(map(int, jsonLabelStr))
        
        correctedArray = np.zeros(nparray.shape, dtype='int32')
        Empty = True
        for i in range(len(jsonClassList)):
            if jsonClassList[i] not in self.labelList:
                next
            else:
                correctedArray[nparray == jsonLabel[i]] = int(self.labelDict[jsonClassList[i]])
                Empty = False
        if Empty ==True:
            correctedArray = []
        return correctedArray

    def saveImgMask(self, fileName, img, correctedArray):
        saveImgPath = join(self.saveSubFolderPath, 'image', fileName+'.png')
        saveMaskPath = join(self.saveSubFolderPath, 'mask', fileName+'.png')
        cv2.imwrite(saveImgPath, img)
        cv2.imwrite(saveMaskPath, correctedArray)

    def saveImgNpy(self, fileName, img, correctedArray):
        saveImgPath = join(self.saveSubFolderPath, fileName+'.png')
        saveMaskPath = join(self.saveSubFolderPath, fileName+'.npy')
        cv2.imwrite(saveImgPath, img)
        np.save(saveMaskPath, correctedArray)
        