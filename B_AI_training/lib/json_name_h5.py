from lib.cwdS import Cwd_path  #取得目前檔案的位置
import os
   
class runJsonname_h5():   
    def __new__(object):
        #取得目前檔案的位置
        cwd =str(Cwd_path()) #cwd=str(mazda)確保是字串格式
        # print("cwd : ",cwd)
        # print(cwd)
        AI_Path_ori = f"{cwd.split('/')[len(cwd.split('/'))-1]}" # 取得目前資料夾名稱
        # print('{0} == {1}'.format('AI_Path_ori :',AI_Path_ori))
        AI_Path0 = cwd.split(AI_Path_ori)[0] # 取得上層資料夾全部名稱
        # print('{0} == {1}'.format('AI_Path0 :',AI_Path0))
        AI_Path1=AI_Path0[:len(AI_Path0)-1] #長度減一(取得上層資料夾全部名)(去掉斜線)
        # print('{0} == {1}'.format('AI_Path1 長度減一 :',AI_Path1))
        _AI_Path=AI_Path1.split('\\')#use in windows 
        # print(_AI_Path)
        print('{0} == {1}'.format('_AI_Path windows :',_AI_Path))
        jsonname=_AI_Path[len(_AI_Path)-1].split('/') 
        #print(jsonname)
        AI_Data_jsonFile=AI_Path1 +'/'+ f"{jsonname[len(jsonname)-1]}_config_h5.json" 
        #取得上層資料夾全部名及串入json資料夾名稱
        print('{0} == {1}'.format('AI_Data_jsonFile_h5 :',AI_Data_jsonFile_h5 ))
        return AI_Data_jsonFile_h5
    
def Jsonname_h5():
    return runJsonname_h5()


#引用方式:
# from lib.json_name import Jsonname  
# #取得json檔案的位置and fullname modify by charley 1120117

#呼叫方式:
# AI_Data_jsonFile = Jsonname()
# print(AI_Data_jsonFile )   #注意等等跑AI需要過來複製一下路徑
# with open(AI_Data_jsonFile , 'w') as f:
#     json.dump(config, f)
# config



        
        


