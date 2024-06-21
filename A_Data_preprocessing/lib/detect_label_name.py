
import os
import json
class DetectLabelName(object):

    def __init__(self, allFolderPath):
        self.allFolderPath = allFolderPath
        self.appearLabel = set()
        self.run()

    def run(self):
        for folder_name in os.listdir(self.allFolderPath):
            folder_path = os.path.join(self.allFolderPath, folder_name)
            folder_json_path = [x for x in os.listdir(folder_path) if os.path.splitext(x)[1]==".json"]
            
            for json_file in folder_json_path:
                json_path = os.path.join(folder_path, json_file)
                with open(json_path, "r") as f:
                    text = f.read()
                # dcLabel: Key-id, Value-class. The class might duplicate.
                file_label_dict = json.loads(text)
                label_set = set(file_label_dict.values())
                diff_set = label_set.difference(self.appearLabel)
                if diff_set != set():
                    self.appearLabel.update(diff_set)
                    print("Update appear label: \n {} \n".format(self.appearLabel))
    def get_list(self):
        return self.appearLabel   