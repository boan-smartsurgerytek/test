import os
import os.path as path
foldepath = "f:\\SurgeryAnalytics\\AI_Cases\\Dentistry\\1_Linknet_efficientnetb7_0_0\\B_AI_training\\ckpt\\"
os.chdir(foldepath)                     #切換到指定目錄
path = os.getcwd()                      #將目前路徑指定給path
print("目前的路徑"+path)                 #顯示目前目錄    
print(os.listdir(path))                 #顯示該目錄的資料
if not os.path.isdir(foldepath):        #判斷目錄不存在
    print(foldepath," 此目錄不存在，由電腦建立目錄..")
else:
    print(foldepath," 此目錄存在..")
my_dict = {}
for filename in os.listdir(foldepath):
    if filename.endswith(".h5"): 
        print(filename.split("_"))
        print(filename.split("_")[1])
        k = filename.split("_")[1].strip()    # key trim
        my_dict[k] = filename.split("_")[2].strip()  # value trim
        continue
    else:
        continue
print(my_dict) 
# Get top 3 values from dictionary
top_3_dict = sorted(my_dict.items(), key=lambda x: x[1], reverse=True)[:3]
print(top_3_dict)   
    
for k, v in top_3_dict:
    print(k, v) 
 
for filename in os.listdir(foldepath):
    mark = 0 
    for k, v in top_3_dict:
        mark = mark + 1
        if filename.find(v)>=0:
            print('保') 
            print(filename)
            break
        elif filename.find(v)< 0 :
            if mark > 2:
                print('刪') 
                print(filename)
                continue
  
