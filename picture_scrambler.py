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
import random

matplotlib.use('TkAgg')     # has to be here due to plt.show() command - https://stackoverflow.com/questions/56656777/userwarning-matplotlib-is-currently-using-agg-which-is-a-non-gui-backend-so

grid_size = 9

image_name = '043B'     # image_name
directory_name = '/Users/valosek/Documents/python_projects/200dpi/'
image_path = directory_name + image_name + '.bmp'

image = img.imread(image_path)      # fetch image using matplotlib.image
image_shuffled = image.copy()       # create copy of original image

image_size = image.shape        # get image size
image_x = image_size[0]         # get size in x-axis
image_y = image_size[1]         # get size in y-axis

### Show original image
# plt.imshow(image)
# plt.show()

index_x = range(1,int(image_x/grid_size*(grid_size+1)),int(image_x/grid_size))      # define posititons in voxel for cutting/splitting input image
index_y = range(1,int(image_y/grid_size*(grid_size+1)),int(image_x/grid_size))

index_subplot=0
subimage_min = []
sub_image = []

for step_x in range(grid_size):
    for step_y in range(grid_size):
        index_subplot = index_subplot + 1
        sub_image.append(image[index_x[step_x]:index_x[step_x + 1], index_y[step_y]:index_y[step_y + 1], :])    # cut/split input image into grid and save individual subimages into one 4D array
        # plt.subplot(grid_size,grid_size,index_subplot)      # create empty subplot
        # plt.imshow(sub_image[index_subplot-1])

        subimage_min.append(sub_image[index_subplot-1].min())   # compute min of individual subimages

#plt.show()


sub_image_random = sub_image.copy()     # Create copy of original 4D matrix with individual subimages
random.shuffle(sub_image_random)        # Shuffle randomly subimages
index_subplot=0

for step_x in range(grid_size):
    for step_y in range(grid_size):
        index_subplot = index_subplot + 1
        #plt.subplot(grid_size,grid_size,index_subplot)      # create empty subplot
        #plt.imshow(sub_image_random[index_subplot-1])       # plot randomly shuffled subimages

        image_shuffled[index_x[step_x]:index_x[step_x + 1], index_y[step_y]:index_y[step_y + 1], :] = sub_image_random[index_subplot-1]

# plt.show()

### Show shuffled image
# plt.imshow(image_shuffled)
# plt.show()

img.imsave(directory_name + image_name + '_shuffled.bmp',image_shuffled)        # Save shuffled image