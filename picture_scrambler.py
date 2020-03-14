########################################
#
# Script for scrambling/shuffling input image(s).
# Output data will be stored in input directory
# with created directory like 'scrambled_data'.
# Jan Valosek, 2020, fMRI lab Olomouc
# Jan Vicha, 2020
# VER = 14-03-2020
#
########################################

import matplotlib.image as img
import matplotlib.pyplot as plt
import matplotlib
import os, sys, random

########### Settings for Change
# INPUT_DIR = ""
# INPUT_DIR = '/Users/valosek/Documents/python_projects/200dpi/'
INPUT_DIR = '/Users/jan/Projects/personal/valda/image_shuffler/data/'
OUTPUT_DIR_NAME = 'scrambled_data'
ENABLED_FORMATS = ["bmp"]
GRID_SIZE = 9
########### Base Settings 
matplotlib.use('TkAgg')     # has to be here due to plt.show() command - https://stackoverflow.com/questions/56656777/userwarning-matplotlib-is-currently-using-agg-which-is-a-non-gui-backend-so
########### 

class Scrambler():

    def __init__(self):
        self.__input_dir = ""
        self.__output_dir = ""
        self.__img_paths = {}   #format: { "img_name": "img_path"}
        self.__count_saved_img = 0

    def main_logic(self):
        """
        Main logic for making scrambling images.
        """        
        self.__input_dir = self.__get_input_dir()

        if self.__input_dir is None:
            return

        self.__img_paths = self.__get_img_paths(self.__input_dir, ENABLED_FORMATS)
        if len(self.__img_paths) == 0:
            print("Vstupni adresar neobsahuje zadne povolene soubory.")
            return

        self.__output_dir = self.__make_output_dir(self.__input_dir, OUTPUT_DIR_NAME)
        if self.__output_dir is None:
            return

        self.__make_output(self.__img_paths, self.__output_dir)



    def __get_input_dir(self):
        """
        This function control global variable INPUT_DIR if is valid and if not then,
        control input argument for valid directory path.        
        :return: Return valid directory path or None.
        :rtype: str, None
        """        
        
        # CHECK INPUT_DIR FROM SCRIPT
        if len(INPUT_DIR) != 0:
            if self.__check_dir(INPUT_DIR):
                print("Byla zvolena validni cesta ve scriptu k adresari.")
                return INPUT_DIR
            else:
                print("Byla zvolena NEvalidni cesta ve scriptu k adresari.")
                return None

        # CHECK INPUT_DIR FROM input ARGUMENT
        if len(sys.argv) > 1:
            if self.__check_dir(sys.argv[1]):
                print("Cesta k adresari ze vstupu je validni.")
                return sys.argv[1]
            else:
                print("Zadana cesta k adresari je neplatna.")
                return None
        else:
            print("Nebyla zadana cesta k adresari.")
            return None

    def __check_dir(self, input_dir):
        """
        :param input_dir: input directory path
        :type input_dir: str
        :return: Return True if input_dir is valid, otherwise return False.
        :rtype: bool
        """
        if type(input_dir) is not str or len(input_dir) == 0:
            return False

        elif not os.path.isdir(input_dir):
            return False
        else:
            return True
        
    def __get_img_paths(self, input_dir, enabled_formats):
        """
        Return directory with all images name and images path. Include only enabled formats.
        :param input_dir: Input directory path with images
        :type input_dir: str
        :param enabled_formats: list of enabled formats
        :type enabled_formats: [str]
        :return: Return img name with img path. format: { "img_name": "img_path"}
        :rtype: dict
        """        
        img_paths = {}
        for file_name in os.listdir(input_dir):
            file_path = os.path.join(input_dir,file_name) 
            if os.path.isfile(file_path) and file_name.split(".")[-1].lower() in enabled_formats:
                img_paths[file_name] = file_path

        return img_paths

    def __make_output_dir(self, input_dir, output_dir_name):
        """
        Make output directory for data storing in input_dir path.
        Check if input_dir exists, then ensure output directory in path.
        :param input_dir: input directory path
        :type input_dir: str
        :param output_dir_name: name output directory
        :type output_dir_name: str
        :return: Return out_dir if is exists or was created. Otherwise return None.
        :rtype: str, None
        """                      
        if not os.path.exists(input_dir):
            print("Nezdarilo se vytvorit output  adresar, protoze neni zadan spravne vstupni adresar.")
            return None
        out_dir = os.path.join(input_dir, output_dir_name)
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
            print(f"Ve vstupnim adresari byl vytvoren novy adresar s nazvem: '{output_dir_name}'")
        return out_dir

    def __make_output(self, img_paths, output_dir):

        for img_name, img_path in img_paths.items():

            image = img.imread(img_path)      # fetch image using matplotlib.image
            image_shuffled = image.copy()       # create copy of original image

            width = image.shape[0]
            height = image.shape[1]

            ### Show original image
            # plt.imshow(image)
            # plt.show()

            index_x = range(1,int(width/GRID_SIZE*(GRID_SIZE+1)),int(width/GRID_SIZE))      # define posititons in voxel for cutting/splitting input image
            index_y = range(1,int(height/GRID_SIZE*(GRID_SIZE+1)),int(height/GRID_SIZE))
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
            img.imsave(os.path.join(output_dir, img_renamed),image_shuffled)
            self.__count_saved_img += 1

        print(f"Pocet ulozenych obrazku: {self.__count_saved_img}")


if __name__ == "__main__":
    scrambler = Scrambler()
    scrambler.main_logic()
