import os
import glob
import tensorflow as tf
from lib.cwdS import Cwd_path  #取得目前檔案的位置
from tensorflow import keras
from tensorflow.python.platform import tf_logging as logging
# from tensorflow.python.util.compat import collections_abc
import collections
# class CSVLogger(Callback):
path="";
class RJ(keras.callbacks.Callback):   
    def __init__(self, A, B):
        super(RJ, self).__init__()
        self.sep = B
        # self.filename = filename
        self.epochs=0
        # self.append = append
        # self.writer = None
        # self.keys = None
        # self.append_header = True
        self.save_model_path=A #object.save_model_path
        # self._reset_batch_timing()
        # super(RJ, self).__init__()

    # def on_train_begin(self, logs=None):
    #     if self.append:
    #         if file_io.file_exists(self.filename):
    #             with open(self.filename, 'r' + self.file_flags) as f:
    #                 self.append_header = not bool(len(f.readline()))
    #         mode = 'a'
    #     else:
    #         mode = 'w'
    #     # if not os.path.isdir(save_model_path):
    #     #     os.mkdir(save_model_path)
    #     # logs = dict([(k, logs[k]) if k in logs else (k, 'NA') for k in self.keys])
    #     logging.warning('on_train_begin') 
    #     if not os.path.isdir('on_train_begin'):
    #         os.mkdir('on_train_begin')
            
#     def on_train_end(self, logs=None):
#         logging.warning('on_train_end')        
#         if not os.path.isdir('on_train_end'):
#             os.mkdir('on_train_end')
            
    def on_epoch_end(self,epoch,logs=None):
        print(self.sep,self.save_model_path)
#         self.epochs += 1
#         epoch=self.epochs
#         logs = logs or {}
#         # logging.warning('on_epoch_begin')
#         print("on_epoch_begin_on_epoch_begin"+str(epoch))
#         if not os.path.isdir('on_epoch_begin'):
#             os.mkdir('on_epoch_begin')
#             # files = glob.glob("mydir/*.txt") # 獲取所有 ".txt" 檔案 self.save_model_path
#             files = glob.glob(self.save_model_path + "/*.h5") 
#             min_size = float("inf") # 設定一個無限大的最小值
#             min_file = None # 設定一個空的最小檔案
#             # for callback in self.callbacks:
#             #     callback.on_epoch_begin(epoch, logs)
#             # self._reset_batch_timing()
#             # import os
#             # import glob
#             for file in files:
#                 size = os.path.getsize(file) # 獲取每個檔案的大小
#     #           print(file, size) # 列印每個檔案的名稱和大小
#                 print("刪除最小檔案 ")
    
#             # if size < min_size: # 如果檔案的大小小於最小值
#             #    min_size = size # 更新最小值
#             #    min_file = file # 更新最小檔案
               
#         #         if min_file: # 如果有找到最小檔案
#         # #       print("The smallest file is", min_file, "with size", min_size) # 列印最小檔案的名稱和大小
#         # #       os.remove(min_file) # 刪除最小檔案
#         #             print("刪除最小檔案 "+ str(min_file))
#         #         else: # 如果沒有找到最小檔案
#         #             print("No files found") # 列印沒有找到任何檔案
        
        
        

#     # def _reset_batch_timing(self):
#     #     self._delta_t_batch = 0.
#     #     self._delta_ts = collections.defaultdict( lambda: collections.deque([], maxlen=self.queue_length))