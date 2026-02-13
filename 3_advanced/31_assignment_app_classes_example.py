#*********************************************************************#
# Class exercise

class Dataset():
    """ Any folder of images should be a dataset, all datasets have  
        some common features that we we will always want to access  """
    def __init__(self):
        self.folderName = ""
        self.filePath = ""
        self.imageCount = 0

    def get_name(self, folder):
        self.folderName = os.path.basename(folder)

    def get_filepath(self, folder):
        self.filePath = folder

    def get_image_count(self, folder):
        image_folder = os.listdir(folder)
        try:
            self.imageCount = len([image for image in image_folder if image.lower().endswith((".png",".jpg",".jpeg",".cr2",".cr3"))])
        except FileNotFoundError:
            self.imageCount = 0


class hdri_dataset(Dataset):
    def __init__(self, folder):
        super().__init__()

        self.get_name(folder)
        self.get_filepath(folder)
        self.get_image_count(folder)

        print(f"HDRI name: {self.folderName}")
        print(f"Image count: {self.imageCount}")
        print(f"File location: {self.filePath}")


class texture_dataset(Dataset):
    def __init__(self, folder):
        super().__init__()

        self.get_name(folder)
        self.get_filepath(folder)
        self.get_image_count(folder)

        print(f"Asset name: {self.folderName}")
        print(f"Image count: {self.imageCount}")
        print(f"File location: {self.filePath}")


class overview_dataset(Dataset):
    def __init__(self, folder):
        super().__init__()

        self.get_name(folder)
        self.get_filepath(folder)
        self.get_image_count(folder)

        print(f"Slate name: {self.folderName}")
        print(f"Image count: {self.imageCount}")
        print(f"File location: {self.filePath}")


shoot_path = r"D:\VFX\assets_and_courses\courses\Advanced_python_course\course_notes\shoot_day_002_sorted"

for folder_name in os.listdir(shoot_path):
    folder_path = os.path.join(shoot_path, folder_name)
    if os.path.isdir(folder_path):
        overview_dataset(folder_path)
        print("\n")

