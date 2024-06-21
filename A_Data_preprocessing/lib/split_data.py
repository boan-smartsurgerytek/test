import numpy as np
import random
import shutil
from os import listdir, mkdir
from os.path  import join, isdir, splitext

class SplitData(object):
    def __init__(self, root_folder_path, root_save_path,
                 test_folder_list=[], val_folder_list=[],
                 label_type="Mask", random_choice=False, use_for_TFRecord=False):
        self.root_folder_path = root_folder_path
        self.root_save_path = root_save_path
        self.test_folder_list = test_folder_list
        self.val_folder_list = val_folder_list
        self.label_type = label_type
        self.random_choice = random_choice
        self.use_for_TFRecord = use_for_TFRecord

        self.work_test = self.test_folder_list!=[]
        self.work_val = self.val_folder_list!=[] or self.random_choice
        self.folder_name_list = listdir(root_folder_path)
        
        self.run()

    def run(self):
        self.create_dataset_folder()
        if self.work_test:
            print("Split testing set...")
            self.split_test()
            print("\n")
        if self.work_val and self.val_folder_list!=[]:
            print("Split validation set...")
            self.split_val()
            print("\n")
            
        if self.random_choice:
            print("Random split training and validation set...")
        else:
            print("Split training set...")
        self.split_train()

    def create_dataset_folder(self):
        if self.work_test:
            test_folder_path = join(self.root_save_path, "test")
            self.test_img_path = join(test_folder_path, "img")
            self.test_label_path = join(test_folder_path, "label")
            self.check_create_folder_path(test_folder_path)
            self.check_create_folder_path(self.test_img_path)
            self.check_create_folder_path(self.test_label_path)
                
        if self.work_val:
            val_folder_path = join(self.root_save_path, "val")
            self.val_img_path = join(val_folder_path, "img")
            self.val_label_path = join(val_folder_path, "label")
            self.check_create_folder_path(val_folder_path)
            self.check_create_folder_path(self.val_img_path)
            self.check_create_folder_path(self.val_label_path)

        train_folder_path = join(self.root_save_path, "train")
        self.train_img_path = join(train_folder_path, "img")
        self.train_label_path = join(train_folder_path, "label")
        self.check_create_folder_path(train_folder_path)
        self.check_create_folder_path(self.train_img_path)
        self.check_create_folder_path(self.train_label_path)

    def check_create_folder_path(self, folder_path):
        if not isdir(folder_path):
            mkdir(folder_path)

    def split_test(self):
        if self.label_type == "Mask":
            self.split_mask(self.test_folder_list, 'test')
        else:
            self.split_array(self.test_folder_list, 'test')

    def split_val(self):
        if self.label_type == 'Mask':
            self.split_mask(self.val_folder_list, 'val')
        else:
            self.split_array(self.val_folder_list, 'val')

    def split_train(self):
        if self.random_choice:
            if self.label_type == 'Mask':
                self.random_split_mask(self.folder_name_list)
            else:
                self.random_split_array(self.folder_name_list)
        else:
            if self.label_type == 'Mask':
                self.split_mask(self.folder_name_list, 'train')
            else:
                self.split_array(self.folder_name_list, 'train')

    def split_mask(self, folder_list, save_folder_name):
        for folder_name in folder_list:
            folder_path = join(self.root_folder_path, folder_name)
            img_folder_path = join(folder_path, "image")
            mask_folder_path = join(folder_path, "mask")

            img_list = listdir(img_folder_path)
            mask_list = listdir(mask_folder_path)
            
            self.move_img(img_folder_path, img_list, save_folder_name)
            self.move_mask(mask_folder_path, mask_list, save_folder_name)
            print("Split folder {} ssuccessfully!".format(folder_name))
            if save_folder_name != "train":
                self.folder_name_list.remove(folder_name)
            
    def split_array(self, folder_list, save_folder_name):
        for folder_name in folder_list:
            folder_path = join(self.root_folder_path, folder_name)
            img_list = [x for x in listdir(folder_path) if x.find(".png")!=-1]
            array_list = [x for x in listdir(folder_path) if x.find(".npy")!=-1]
            
            self.move_img(folder_path, img_list, save_folder_name)
            self.move_array(folder_path, array_list, save_folder_name)
            print("Split folder {} ssuccessfully!".format(folder_name))
            if save_folder_name != "train":
                self.folder_name_list.remove(folder_name)

    def move_img(self, img_folder_path, img_list, save_folder_name):
        if save_folder_name == "test":
            save_folder_path = self.test_img_path
        elif save_folder_name == "val":
            save_folder_path = self.val_img_path
        else:
            save_folder_path = self.train_img_path
            
        for img_name in img_list:
            img_path = join(img_folder_path, img_name)
            save_img_path = join(save_folder_path, img_name)
            shutil.copyfile(img_path, save_img_path)
            
    def move_mask(self, mask_folder_path, mask_list, save_folder_name):
        if save_folder_name == "test":
            save_folder_path = self.test_label_path
        elif save_folder_name == "val":
            save_folder_path = self.val_label_path
        else:
            save_folder_path = self.train_label_path
            
        for mask_name in mask_list:
            mask_path = join(mask_folder_path, mask_name)
            save_mask_path = join(save_folder_path, mask_name)
            shutil.copyfile(mask_path, save_mask_path)

    def move_array(self, folder_path, array_list, save_folder_name):
        if save_folder_name == "test":
            save_folder_path = self.test_label_path
        elif save_folder_name == "val":
            save_folder_path = self.val_label_path
        else:
            save_folder_path = self.train_label_path
            
        for array_name in array_list:
            array_path = join(folder_path, array_name)
            save_array_path = join(save_folder_path, array_name)
            if self.use_for_TFRecord:
                array = np.load(array_path)
                expand_array = self.expand_array_dim(array)
                np.save(save_array_path, expand_array)
            else:
                shutil.copyfile(array_path, save_array_path)
            
    def expand_array_dim(self, npy_array):
        extend_array = np.expand_dims(npy_array, axis=-1)
        return extend_array

    def random_split_mask(self, folder_list):
        for folder_name in folder_list:
            img_folder_path = join(self.root_folder_path, folder_name, "image")
            mask_folder_path = join(self.root_folder_path, folder_name, "mask")
            img_list = listdir(img_folder_path)
            for img_name in img_list:
                threshold = random.random()
                if threshold <= 0.1:
                    save_img_path = join(self.val_img_path, img_name)
                    save_mask_path = join(self.val_label_path, img_name)
                else:
                    save_img_path = join(self.train_img_path, img_name)
                    save_mask_path = join(self.train_label_path, img_name)
                    
                img_path = join(img_folder_path, img_name)
                mask_path = join(mask_folder_path, img_name)
                
                shutil.copyfile(img_path, save_img_path)
                shutil.copyfile(mask_path, save_mask_path)
                
            print("Split folder {} ssuccessfully!".format(folder_name))
            
    def random_split_array(self, folder_list):
        for folder_name in folder_list:
            folder_path = join(self.root_folder_path, folder_name)
            img_list = {splitext(x)[0] for x in listdir(folder_path)}
            for img_name in img_list:
                threshold = random.random()
                if threshold <= 0.1:
                    save_img_path = self.val_img_path
                    save_npy_path = self.val_label_path
                else:
                    save_img_path = self.train_img_path
                    save_npy_path = self.train_label_path
                    
                img_path = join(folder_path, img_name+".png")
                npy_path = join(folder_path, img_name+".npy")
                
                shutil.copyfile(img_path, save_img_path)
                if self.use_for_TFRecord:
                    array = np.load(npy_path)
                    expand_array = self.expand_array_dim(array)
                    np.save(save_npy_path, expand_array)
                else:
                    shutil.copyfile(npy_path, save_npy_path)

            print("Split folder {} ssuccessfully!".format(folder_name))