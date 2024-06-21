import os
import glob
from lib.cwdS import Cwd_path  #取得目前檔案的位置
from tensorflow import keras
from tensorflow.python.platform import tf_logging as logging
import collections
# class CSVLogger(Callback):
path="";
class RJ(keras.callbacks.Callback):   
    def __init__(self, save_model_path, separator=',', append=False):
        self.sep = separator
        # self.filename = filename
        self.epochs=0
        self.append = append
        self.writer = None
        self.keys = None
        self.append_header = True
        self.save_model_path=save_model_path #object.save_model_path

    def on_train_begin(self, logs=None):
        if self.append:
            if file_io.file_exists(self.filename):
                with open(self.filename, 'r' + self.file_flags) as f:
                    self.append_header = not bool(len(f.readline()))
            mode = 'a'
        else:
            mode = 'w'
        # if not os.path.isdir(save_model_path):
        #     os.mkdir(save_model_path)
        # logs = dict([(k, logs[k]) if k in logs else (k, 'NA') for k in self.keys])
        logging.warning('on_train_begin') 
        if not os.path.isdir('on_train_begin'):
            os.mkdir('on_train_begin')
            
    def on_train_end(self, logs=None):
        import os
        self.epochs += 1
        epoch=self.epochs
        logs = logs or {}
        # logging.warning('on_epoch_begin')
        # print("on_epoch_begin_on_epoch_begin"+str(epoch))
        files = glob.glob(self.save_model_path + "/*.h5") 
        # print(files)

        my_dict = {}
        for filename in files:
            if filename.endswith(".h5"): 
                # print(filename.split("_"))
                # print(filename.split("_")[9])
                k = filename.split("_")[len(filename.split("_"))-3].strip()          # key trim
                my_dict[k] = filename.split("_")[len(filename.split("_"))-2].strip()  # value trim
                continue
            else:
                continue
        # print(my_dict) 
        # Get top 3 values from dictionary
        top_3_dict = sorted(my_dict.items(), key=lambda x: x[1], reverse=True)[:3]
        print(top_3_dict)   

        # for k, v in top_3_dict:
            # print(k, v) 

        for filename in files:
            mark = 0 
            for k, v in top_3_dict:
                mark = mark + 1
                if filename.find(v)>=0:
                    print('保留') 
                    print(filename)
                    # print(str(len(filename.split("_"))))
                    break
                elif filename.find(v)< 0 :
                    if mark > 2:
                        print('刪除') 
                        print(filename)
                        os.remove(filename)
                        continue
        if not os.path.isdir('on_train_end'):
            os.mkdir('on_train_end')
            
    def on_epoch_begin(self,epoch,logs=None):
            # check_H5()
        import os
        self.epochs += 1
        epoch=self.epochs
        logs = logs or {}
        # logging.warning('on_epoch_begin')
        # print("on_epoch_begin_on_epoch_begin"+str(epoch))
        files = glob.glob(self.save_model_path + "/*.h5") 
        # print(files)

        my_dict = {}
        for filename in files:
            if filename.endswith(".h5"): 
                # print(filename.split("_"))
                # print(filename.split("_")[9])
                k = filename.split("_")[len(filename.split("_"))-3].strip()    # key trim
                my_dict[k] = filename.split("_")[len(filename.split("_"))-2].strip()  # value trim
                continue
            else:
                continue
        # print(my_dict) 
        # Get top 3 values from dictionary
        top_3_dict = sorted(my_dict.items(), key=lambda x: x[1], reverse=True)[:3]
        print(top_3_dict)   

        # for k, v in top_3_dict:
            # print(k, v) 

        for filename in files:
            mark = 0 
            for k, v in top_3_dict:
                mark = mark + 1
                if filename.find(v)>=0:
                    print('保留') 
                    print(filename)
                    # print(str(len(filename.split("_"))))
                    break
                elif filename.find(v)< 0 :
                    if mark > 2:
                        print('刪除') 
                        print(filename)
                        os.remove(filename)
                        continue
         
  

   
        
        
        
        
        
 