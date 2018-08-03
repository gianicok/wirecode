#------------------------------------------- https://conda.io/miniconda.html
#------------------------------------------- download miniconda and then use the conda package manager to install these packages that are needed to run the code. 

conda install -c anaconda tk #-------------- Tkinter for GUI's
conda install -c conda-forge opencv #------- OpenCV for image processing
conda install -c conda-forge matplotlib #--- Matplotlib for plotting images
conda install -c anaconda numpy #----------- Numpy for multi dimensional arrays (color)
conda install -c anaconda scipy #----------- Scipy contains Ndimage
conda install -c anaconda xlwt #------------ Xlwt used for excel sheets
conda install -c anaconda pil #------------- PIL image goes hand and hand with tkinter#

#---------------------------------------------------------------------------------------------------------------------------------------

YIELD.PY

- Enter path to image when prompted.

- Use left mouse button to drag from top left to bottom right a template. Make sure the cropped area contains just the nanowire and nothing else. For photos where the nanowires generally look the same I recommend to grab 5 wires on the first round. For photos where the nanowires look mostly different I recommend to grab 6 of the common spherical wires and then 4 differently faced wires. In both cases grab templates from different spots of the image and make sure not to just left click must be click and drag. Click the ‘Q’ key once you are done cropping.

- During the second round of template cropping crop out only 5 templates that the computer has missed. Click the ‘Q’ key once you are done cropping. 

- Enter the pitch value when prompted.

- Use the left mouse button to drag a line across the bar that represents pixels per micrometer left to right. Click the ‘Q’ key once you are done measuring. Then proceed to enter how many microns that number of pixels represents. 

- The result image will stay up with the information until any key is pressed.

- Congratulations you have succesfully ran the program!

NWIREDIMENSIONS.PY

- Enter image path

- Enter your Sigma value and modify it until you are confident with your filtered image. The image with the new value is displayed every time you hit enter. Once done modifying, click the X button on the window

- Enter tilt degrees, threshold, and how many points you would like to grab per nanowire. All of these windows are closed once you click ‘ENTER’. 

- Enter the file name for the excel sheet that the data will be written onto. If you would like to create a new excel sheet type a new file name but if you would like to overwrite an existing excel sheet give the new file the same name as the old file you wish to overwrite. Once you decide on a excel sheet name click ‘ENTER’. 

- Use the left mouse button to drag a line across the bar that represents pixels per micrometer left to right. Click the ‘Q’ key once you are done measuring. Then proceed to enter how many microns that number of pixels represents. 

- Click the selected number of points on the wire and do so for however many wires you like. The points will be saved on your image to help prevent marking down the same points. 

- Once you have finished click the ‘X’ button on the window. The spreadsheet should be saved in your .spyder-py3 folder. 

- Congratulations you have succesfully ran the program!
