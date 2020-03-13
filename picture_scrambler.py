########################################
#
# Script for scrambling/shuffling input image(s)
#
# Jan Valosek, 2020, fMRI lab Olomouc
# VER = 12-02-2020
#
########################################

import matplotlib.image as img
import matplotlib.pyplot as plt
import matplotlib
import os, sys, random


########### Settings 
matplotlib.use('TkAgg')     # has to be here due to plt.show() command - https://stackoverflow.com/questions/56656777/userwarning-matplotlib-is-currently-using-agg-which-is-a-non-gui-backend-so
GRID_SIZE = 9
ENABLED_FORMATS = ["bmp"]
IMG_PATHS = {} # format: { "img_name": "img_path"}
# INPUT_DIR = ""
# INPUT_DIR = '/Users/valosek/Documents/python_projects/200dpi/'
INPUT_DIR = '/Users/jan/Projects/personal/valda/image_shuffler/data/'
OUTPUT_DIR_NAME = 'output_data'
########### 
class Scrambler():

    def __init__(self):
        self.__input_dir = ""

    def __check_dir_argument(self):
        """
        Check if global variable input dir is empty. IF not then set it and control. If not
        check directory path from input argument script and set into class variable.
        """        
        if len(INPUT_DIR) > 0:
            if not os.path.isdir(INPUT_DIR):
                print("Zvolena vnitrni cesta k adresari je nevalidni")
                return False
            print("Byla zvolena vnitrni cesta k adresari.")
            self.__input_dir = INPUT_DIR
            return True

        elif len(sys.argv) <= 1:
            print("Nebyla zadana cesta k adresari.")
            return False

        elif not os.path.isdir(sys.argv[1]):
            print("Zadana cesta k adresari je neplatna.")
            return False
        else:
            print("Adresar byl zadan uspesne.")
            self.__input_dir = sys.argv[1]
            return True
        
    def make_img_path_list(self):
        """
        Method check global input dir variable if not empty and check it.
        If is empty then control input script arguments. If all is correct then fill list with all
        images path include enabled formats.
        """    
        if not self.__check_dir_argument():
            return
    
        for file_name in os.listdir(self.__input_dir):
            file_path = os.path.join(self.__input_dir,file_name) 
            if os.path.isfile(file_path) and file_name.split(".")[-1].lower() in ENABLED_FORMATS:
                IMG_PATHS[file_name] = file_path

    def make_output_dir(self):
        if not len(self.__input_dir) > 0:
            print("Nezdarilo se vytvorit output_data adresar, protoze neni zadan spravne vstupni adresar.")
            return False
        out_dir = os.path.join(INPUT_DIR, OUTPUT_DIR_NAME)
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        return True
        

    def make_output(self):
        if not self.make_output_dir():
            return

        for img_name, img_path in IMG_PATHS.items():

            image = img.imread(img_path)      # fetch image using matplotlib.image
            image_shuffled = image.copy()       # create copy of original image

            image_size = image.shape        # get image size
            image_x = image_size[0]         # get size in x-axis
            image_y = image_size[1]         # get size in y-axis

            ### Show original image
            # plt.imshow(image)
            # plt.show()

            index_x = range(1,int(image_x/GRID_SIZE*(GRID_SIZE+1)),int(image_x/GRID_SIZE))      # define posititons in voxel for cutting/splitting input image
            index_y = range(1,int(image_y/GRID_SIZE*(GRID_SIZE+1)),int(image_x/GRID_SIZE))

            index_subplot=0
            subimage_min = []
            sub_image = []

            for step_x in range(GRID_SIZE):
                for step_y in range(GRID_SIZE):
                    index_subplot = index_subplot + 1
                    sub_image.append(image[index_x[step_x]:index_x[step_x + 1], index_y[step_y]:index_y[step_y + 1], :])    # cut/split input image into grid and save individual subimages into one 4D array
                    # plt.subplot(GRID_SIZE,GRID_SIZE,index_subplot)      # create empty subplot
                    # plt.imshow(sub_image[index_subplot-1])

                    subimage_min.append(sub_image[index_subplot-1].min())   # compute min of individual subimages

            #plt.show()


            sub_image_random = sub_image.copy()     # Create copy of original 4D matrix with individual subimages
            random.shuffle(sub_image_random)        # Shuffle randomly subimages
            index_subplot=0

            for step_x in range(GRID_SIZE):
                for step_y in range(GRID_SIZE):
                    index_subplot = index_subplot + 1
                    #plt.subplot(GRID_SIZE,GRID_SIZE,index_subplot)      # create empty subplot
                    #plt.imshow(sub_image_random[index_subplot-1])       # plot randomly shuffled subimages

                    image_shuffled[index_x[step_x]:index_x[step_x + 1], index_y[step_y]:index_y[step_y + 1], :] = sub_image_random[index_subplot-1]

            # plt.show()

            ### Show shuffled image
            # plt.imshow(image_shuffled)
            # plt.show()
            img_renamed = img_name.split(".")[0] + '_shuffled.' + img_name.split(".")[1]
            img.imsave(os.path.join(INPUT_DIR, OUTPUT_DIR_NAME, img_renamed),image_shuffled)

if __name__ == "__main__":
    scrambler = Scrambler()
    scrambler.make_img_path_list()
    scrambler.make_output()



exit(0)
image_path = directory_name + image_name + '.bmp'

image = img.imread(image_path)      # fetch image using matplotlib.image
image_shuffled = image.copy()       # create copy of original image

image_size = image.shape        # get image size
image_x = image_size[0]         # get size in x-axis
image_y = image_size[1]         # get size in y-axis

### Show original image
# plt.imshow(image)
# plt.show()

index_x = range(1,int(image_x/GRID_SIZE*(GRID_SIZE+1)),int(image_x/GRID_SIZE))      # define posititons in voxel for cutting/splitting input image
index_y = range(1,int(image_y/GRID_SIZE*(GRID_SIZE+1)),int(image_x/GRID_SIZE))

index_subplot=0
subimage_min = []
sub_image = []

for step_x in range(GRID_SIZE):
    for step_y in range(GRID_SIZE):
        index_subplot = index_subplot + 1
        sub_image.append(image[index_x[step_x]:index_x[step_x + 1], index_y[step_y]:index_y[step_y + 1], :])    # cut/split input image into grid and save individual subimages into one 4D array
        # plt.subplot(GRID_SIZE,GRID_SIZE,index_subplot)      # create empty subplot
        # plt.imshow(sub_image[index_subplot-1])

        subimage_min.append(sub_image[index_subplot-1].min())   # compute min of individual subimages

#plt.show()


sub_image_random = sub_image.copy()     # Create copy of original 4D matrix with individual subimages
random.shuffle(sub_image_random)        # Shuffle randomly subimages
index_subplot=0

for step_x in range(GRID_SIZE):
    for step_y in range(GRID_SIZE):
        index_subplot = index_subplot + 1
        #plt.subplot(GRID_SIZE,GRID_SIZE,index_subplot)      # create empty subplot
        #plt.imshow(sub_image_random[index_subplot-1])       # plot randomly shuffled subimages

        image_shuffled[index_x[step_x]:index_x[step_x + 1], index_y[step_y]:index_y[step_y + 1], :] = sub_image_random[index_subplot-1]

# plt.show()

### Show shuffled image
# plt.imshow(image_shuffled)
# plt.show()

img.imsave(directory_name + image_name + '_shuffled.bmp',image_shuffled)        # Save shuffled image