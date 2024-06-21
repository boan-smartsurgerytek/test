import torch
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
import cv2
import numpy as np
import segmentation_models_pytorch as smp
import os.path as path   # add by charley 1110830
import json              # add by charley 1110830
import operator          # add by charley 1110830
"""
The API for predicting pictures in specific folder.
"""
device = 0
class PredFolderImg(object):
    """
    Inputs-
    basicParameters: A list that include\n
        1. imgFolderPath: Image folder path which you want to use AI model predicting.
        2. savePredImgFolderPath: The saving folder path of predict image.

    modelParameters: A list that include\n
        1. modelName: Model name which you used to training.
        2. backboneName: Backbone name which you used to training.
        3. numClasses: Number of classes, value needed add 1 (unlabeled).
        4. colorList: A list that each element contains a BGR color list. It color will correspond classes index.
        5. ckptFolderPath: The folder path that checkpoint file(.h5) saving.
    """
    def __init__(self, basicParameters, modelParameters,data_height,data_width):
        # print("TF version: {}.".format(tf.__version__))
        # print("Keras version: {}.\n".format(keras.__version__))
        self.imgFolderPath = basicParameters[0]
        self.savePredImgFolderPath = basicParameters[1]

        self.modelName = modelParameters[0]
        self.backboneName = modelParameters[1]
        self.numClasses = modelParameters[2]
        self.colorList = modelParameters[3]
        self.ckptFolderPath = modelParameters[4]
        print(modelParameters[4])
        self.ACTIVATION = 'sigmoid' if self.numClasses == 1 else 'softmax2d'
        # self.preprocessInput = sm.get_preprocessing(self.backboneName)
        self.preprocessInput = smp.encoders.get_preprocessing_fn(self.backboneName, "imagenet")
        # self.createModel()
        self.data_height=data_height
        self.data_width=data_width
        self.run()

    # def createModel(self):
    #     exec("self.model = sm.{}(self.backboneName, classes=self.numClasses, activation=self.activation)".format(self.modelName))

    def loadModelWeight(self, ckptPath):
        self.model = torch.load(ckptPath)

    def createFolder(self, path):
        if not os.path.exists(path):
            os.mkdir(path)

    def predSingleImg(self, imgPath, savePath):
        img = cv2.imread(imgPath)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        hight, width, _ = img.shape
        resizeImg = cv2.resize(img, (self.data_width, self.data_height), interpolation=cv2.INTER_CUBIC)
        resizeImg = self.preprocessInput(resizeImg)
        resizeImg = resizeImg.transpose(2, 0, 1).astype('float32')
        x_tensor = torch.from_numpy(resizeImg).to(device).unsqueeze(0)   
        pr_mask = self.model.forward(x_tensor)#(1,n,480,640)
        # m = torch.nn.Softmax(dim=1)
        # pr_mask = m(pr_mask)
        pr_mask = (torch.argmax(pr_mask, dim = 1))#(1,480,640)
        pr_mask = (pr_mask.squeeze().cpu().numpy())#(480,640)
        # print(np.unique(pr_mask))   
        predImg = np.zeros([self.data_height, self.data_width, 3])

        for i in np.arange(1, len(self.colorList)+1):
            loc = np.where(pr_mask == i)
            predImg[loc] = self.colorList[i-1]

        predImg = cv2.resize(predImg, (width, hight), interpolation=cv2.INTER_NEAREST)
        cv2.imwrite(savePath, predImg)
    def run_ckpt(self): #Add by charley 1110830 找出最佳的ckpname 
        dic = {}
        # if '.ipynb_checkpoints' in file_name_list:
        #     file_name_list.remove('.ipynb_checkpoints')
        for ckptFileName in os.listdir(self.ckptFolderPath):
            # print(ckptFileName) # 列示全部的ckpt值
            if ckptFileName=='.ipynb_checkpoints':
                 print('Delete_list_name:'+ckptFileName)
            else :
                k = ckptFileName.split('_')[2].strip() # key trim
                dic[k] = ckptFileName.split('_')[3].strip()  # value trim
        print(dic)  # 列示全部的ckpt值    
        json_object = json.dumps(dic, indent=4)
        max_keys = [key for key, value in dic.items() if value == max(dic.values())]
        print(max_keys[0]) #如為多個找出其中一個即可
        print("best solution ckpt-{} !".format(max_keys[0]))
        self.ckpname=max_keys[0] #存入自訂變數
        #return self.ckpname     
        
    def run(self):
        self.run_ckpt() #list ckptname     
        
        for ckptFileName in os.listdir(self.ckptFolderPath):
            if ckptFileName=='.ipynb_checkpoints':
                 print('Delete_list_name:'+ckptFileName)
            else :
                weightIdx = self.modelName+'_'+self.backboneName+'_'+ckptFileName.split('_')[2]
                # print("weightIdx : "+weightIdx)
                if ckptFileName.split('_')[2] != self.ckpname: #找出最佳的 by charley
                    #print(ckptFileName.split('_')[2])
                    print("Ignore not add folder ckpt-{} !".format(ckptFileName.split('_')[2].strip()))
                    continue
                imgSaveFolderPath = os.path.join(self.savePredImgFolderPath, 'pred-'+weightIdx)
                self.createFolder(imgSaveFolderPath)
                # print("imgSaveFolderPath"+imgSaveFolderPath)

                ckptPath = os.path.join(self.ckptFolderPath, ckptFileName)
                # print(ckptPath)
                self.loadModelWeight(ckptPath)
                # print(self.imgFolderPath)
                rowCount = 0
                for file in os.listdir(self.imgFolderPath):
                    rowCount += 1
                    if (rowCount%100) == 0: #--------------------------new20221108-yita----------------
                        print("處理進度DataNum:" + str(rowCount) )#--------------------------new20221108-yita----------------
                    # print(file)
                    fileName = os.path.splitext(file)[0]
                    imgPath = os.path.join(self.imgFolderPath, file)
                    savePath = os.path.join(imgSaveFolderPath, fileName + '_pred.png')
                    self.predSingleImg(imgPath, savePath)

                print("Predict ckpt-{} image ssuccessfully!".format(weightIdx))

    