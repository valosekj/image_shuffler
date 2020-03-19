########################################
#
# Script for shuffling of image(s).
# Output data will be stored in input directory
# into newly created directory 'scrambled_data'.
#
# Jan Valosek, fMRI laboratory Olomouc
# Jan Vicha
# 2020
# VER = 16-03-2020
#
########################################
import argparse
import matplotlib.image as img
import matplotlib.pyplot as plt
import matplotlib
import os, sys, random
from scipy import ndimage

########### Settings for Change
INPUT_DIR = ""
# INPUT_DIR = '/Users/valosek/Documents/python_projects/picture_scramble/data/'
# INPUT_DIR = '/Users/jan/Projects/personal/valda/image_shuffler/data/'
OUTPUT_DIR_NAME = 'scrambled_data'
ENABLED_FORMATS = ["bmp"]
GRID_SIZE = 9
########### Base Settings 
matplotlib.use('TkAgg')     # has to be here due to plt.show() command - https://stackoverflow.com/questions/56656777/userwarning-matplotlib-is-currently-using-agg-which-is-a-non-gui-backend-so
########### 

class Scrambler():

    # initial constructor to set the values
    def __init__(self):
        self.__input_dir = ""
        self.__output_dir = ""
        self.__img_paths = {}   # format: { "img_name": "img_path"}
        self.__count_saved_img = 0

    def main_logic(self):
        """
        Main logic for making scrambling images.
        """

        # Get parser args
        parser = self.get_parser()
        self.arguments = parser.parse_args()

        # SET input_dir
        if self.arguments.i is None:
            # Only for debuging...
            self.__input_dir = INPUT_DIR
            self.__input_dir = self.__control_input_dir(INPUT_DIR)
        else:
            # normal mode
            self.__input_dir = self.__control_input_dir(self.arguments.i)

        # CONTROL images in paths 
        self.__img_paths = self.__get_img_paths(self.__input_dir, ENABLED_FORMATS)
        if len(self.__img_paths) == 0:
            print("Input directory is empty.")
            exit(0)

        # CHECK output directory
        if self.arguments.o is not None:
            self.__output_dir = self.__make_output_dir(self.__input_dir, self.arguments.o)
        else:
            self.__output_dir = self.__make_output_dir(self.__input_dir, OUTPUT_DIR_NAME)


        # CONTROL grid size
        if self.arguments.g is not None:
            self.__grid_size = self.arguments.g
        else:
            self.__grid_size = GRID_SIZE
        print("Grid size is set to {} x {}".format(self.__grid_size,self.__grid_size))

        # Print info about algorithm
        print("Algorithm is set to '{}'.".format(self.arguments.a))



        # MAKE MAGIC PROCESS
        self.__make_output(self.__img_paths, self.__output_dir)


    def __control_input_dir(self, input_dir):
        """
        Control if input_dir is valid.
        :param input_dir: path directory
        :type input_dir: str
        :return: Return valid directory path or exit script.
        :rtype: str
        """
        if len(input_dir) > 1:
            if self.__check_dir(input_dir):
                print("Path to input directory is correct. Continuing...")
                return input_dir
            else:
                print("ERROR: Path to input directory is incorrect.")
                exit(0)
        else:
            print("No path to input directory is set.")
            exit(0)

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
        Return directory with all image names and images paths. Include only enabled formats.
        :param input_dir: Input directory path with images
        :type input_dir: str
        :param enabled_formats: list of enabled formats
        :type enabled_formats: [str]
        :return: Return img name with img path. format: { "img_name": "img_path"}
        :rtype: {}
        """
        img_paths = {}
        for file_name in os.listdir(input_dir):
            file_path = os.path.join(input_dir,file_name) 
            if os.path.isfile(file_path) and file_name.split(".")[-1].lower() in enabled_formats:
                img_paths[file_name] = file_path

        return img_paths

    def __make_output_dir(self, input_dir, output_dir_name):
        """
        Make output directory for shuffled image(s) in input_dir path.
        Check if input_dir exists, then ensure output directory in path.
        If error then exit script.
        :param input_dir: input directory path
        :type input_dir: str
        :param output_dir_name: name of output directory
        :type output_dir_name: str
        :return: Return out_dir if is exists or was created.
        :rtype: str
        """
        if not os.path.exists(input_dir):
            print("ERROR: Input directory '{}' does not exist or path is incorrect.".format(input_dir))
            exit(0)
        output_dir = os.path.join(input_dir, output_dir_name)
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
            print("Output directory '{}' was successfully created inside '{}'.".format(output_dir_name,input_dir))
        else:
            print("Output directory '{}' already exists in input directory '{}'. Shuffled images will be saved there.".format(output_dir_name,input_dir))
        return output_dir

    def __make_output(self, img_paths, output_dir):
        """
        #TODO zkontroluj popis
        Fetch image, get its size, define pixel positions for shuffle, call shuffle function.
        Save images.
        :param img_paths: img name with img path. format: { "img_name": "img_path"}
        :type img_paths: {}
        :param output_dir: output_dir path
        :type output_dir: str
        """        
        for img_name, img_path in img_paths.items():    # loop through individual images

            image = img.imread(img_path)                # fetch image using matplotlib.image

            width = image.shape[0]
            height = image.shape[1]

            ### Show original image
            # plt.imshow(image)
            # plt.show()

            index_x = range(1,int(width/self.__grid_size*(self.__grid_size+1)),int(width/self.__grid_size))      # define posititons in pixel for splitting input image
            index_y = range(1,int(height/self.__grid_size*(self.__grid_size+1)),int(height/self.__grid_size))

            if self.arguments.a == 'random':
                image_shuffled = self.__random_shuffle(image, index_x, index_y)
            elif self.arguments.a == 'nonzero':
                image_shuffled = self.__nonzero_shuffle(image, index_x, index_y)

            ### Show shuffled image
            # plt.imshow(image_shuffled)
            # plt.show()

            img_renamed = img_name.split(".")[0] + '_shuffled.' + img_name.split(".")[1]
            img.imsave(os.path.join(output_dir, img_renamed),image_shuffled)
            self.__count_saved_img += 1

        print("Number of succesfully processed images: {}".format(self.__count_saved_img))

    def __random_shuffle(self, image, index_x, index_y):
        #TODO dopis
        """[summary]
        
        :param image: [description]
        :type image: [type]
        :param index_x: [description]
        :type index_x: [type]
        :param index_y: [description]
        :type index_y: [type]
        :return: [description]
        :rtype: [type]
        """        
        """
        Shuffle image randomly
        :param image: input image
        :param index_x: range of pixels for image split
        :param index_y: range of pixels for image split
        :return: shuffled image
        """
        image_shuffled = image.copy()  # create copy of original image

        index_subplot = 0
        sub_image = []

        for step_x in range(self.__grid_size):
            for step_y in range(self.__grid_size):
                index_subplot += 1
                sub_image.append(image[index_x[step_x]:index_x[step_x + 1], index_y[step_y]:index_y[step_y + 1], :])  # cut/split input image into grid and save individual subimages into one 4D array
                # plt.subplot(self.__grid_size,self.__grid_size,index_subplot)      # create empty subplot
                # plt.imshow(sub_image[index_subplot-1])

        # plt.show()

        sub_image_random = sub_image.copy()     # Create copy of the original 4D list (list of 3D arrays) with individual subimages
        random.shuffle(sub_image_random)        # Shuffle randomly subimages

        sub_image_random = self.__rotation(sub_image_random)

        index_subplot = 0

        for step_x in range(self.__grid_size):
            for step_y in range(self.__grid_size):
                index_subplot += 1
                # plt.subplot(self.__grid_size,self.__grid_size,index_subplot)      # create empty subplot
                # plt.imshow(sub_image_random[index_subplot-1])       # plot randomly shuffled subimages

                image_shuffled[index_x[step_x]:index_x[step_x + 1], index_y[step_y]:index_y[step_y + 1], :] = sub_image_random[index_subplot - 1]

        # plt.show()

        return image_shuffled

    def __nonzero_shuffle(self, image, index_x, index_y):
        #TODO: dopis
        """[summary]
        
        :param image: [description]
        :type image: [type]
        :param index_x: [description]
        :type index_x: [type]
        :param index_y: [description]
        :type index_y: [type]
        :return: [description]
        :rtype: [type]
        """        
        """
        Shuffle only parts of image containing nonzero elements
        :param image: input image
        :param index_x: range of pixels for image split
        :param index_y: range of pixels for image split
        :return:
        """

        image_shuffled = image.copy()  # create copy of original image

        sub_image = {}

        # MAKE dictionary of non zero pixels
        for step_x in range(self.__grid_size):
            for step_y in range(self.__grid_size):
                _add_part = image[index_x[step_x]:index_x[step_x + 1], index_y[step_y]:index_y[step_y + 1], :]

                if _add_part.min() < 200:
                    sub_image[(step_x, step_y)] = _add_part

        ### Shuffle randomly all values (ndarrays)
        values = list(sub_image.values())
        random.shuffle(values)      # Shuffle randomly individual subimages (ndarrays)

        values = self.__rotation(values)

        shuffled_sub_images = dict()
        for index, key in enumerate(sub_image.keys(), 0):
            shuffled_sub_images[key] = values[index]

        for step_x in range(self.__grid_size):
            for step_y in range(self.__grid_size):
                if (step_x, step_y) in shuffled_sub_images.keys():
                    image_shuffled[index_x[step_x]:index_x[step_x + 1], index_y[step_y]:index_y[step_y + 1], :] = shuffled_sub_images[(step_x, step_y)]

        return image_shuffled


    def get_parser(self):
        #TODO dopis, ale tady mozna nemusis
        """[summary]
        
        :return: [description]
        :rtype: [type]
        """        

        parser = argparse.ArgumentParser(
            description='Perform shuffle/mixing if input image(s). '
                        'Jan Valosek, Jan Vicha, 2020',
            add_help=False,
            prog=os.path.basename(__file__))

        mandatory = parser.add_argument_group("MANDATORY ARGUMENTS")
        mandatory.add_argument(
            "-i",
            metavar='<input_data>',
            help="Folder with input image(s)",
            required=True,
            # required=False,
            )

        optional = parser.add_argument_group("OPTIONAL ARGUMENTS")
        optional.add_argument(
            "-h",
            "--help",
            action="help",
            help="Show this help message and exit.")
        optional.add_argument(
            "-a",
            metavar='<algorithm>',
            help="Type of algorithm. Options: random/nonzero.",
            choices=['random','nonzero'],
            required=False,
            default='nonzero')
        optional.add_argument(
            '-o',
            metavar='<output_dir>',
            help='Output directory.',
            required=False)
        optional.add_argument(
            '-g',
            metavar='<int>',
            type=int,
            help='Grid size. Example: 3.',
            required=False)

        return parser

    def __rotation(self, images):
        """
        Rotate individual subimages inside images variable by randomly selected angle.
        :param images: input images for rotation
        :type images: [ndarrays]
        :return: return random rotated each image
        :rtype: [ndarrays]
        """        

        images_rotated = list()

        # List of possible angles for rotation
        angles = [0,90,180,270]

        # Loop through individual subimages
        for image in images:
            # rotate image by randomly selected angle
            images_rotated.append(ndimage.rotate(image, 
                            angles[random.randint(0,len(angles)-1)],
                            reshape= False,
                            mode="reflect")) # mode ensure remove black edges on sides image

        return images_rotated


if __name__ == "__main__":
    scrambler = Scrambler()
    scrambler.main_logic()
