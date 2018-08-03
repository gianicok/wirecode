import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk

#GLOBAL VARIABLES--------------------------------------------------------------
x_start, y_start, x_end, y_end = 0, 0, 0, 0
points1,points2,points3,points4,templates = [],[],[],[],[]
cropping = False
x_st, y_st, x_e, y_e = 0, 0, 0, 0
point1,point2,point3,point4 = [],[],[],[]                                      
cropp = False
    
#FUNCTIONS---------------------------------------------------------------------
def passx(x):
    global read
    read = x

def printx():
    global e,roots
    string = e.get() 
    pic = (string) 
    roots.destroy()
    return passx(pic)

def passThru(x):
    global pitch
    pitch = x

def printtext():
    global e,root
    string = e.get() 
    pitch = (int(string))
    root.destroy()
    return passThru(pitch)

def convert(param):
    global eb,rootb, scale
    if param == 1:
        conversion = float(eb.get())
        scale = scale/conversion
        rootb.destroy()
    if param == 0:
        conversion = float(eb.get())
        conversion = conversion/1000
        scale = scale/conversion
        rootb.destroy()
    
def mouse_draw(evt, xx, yy, flg, par):
    global x_st, y_st, x_e, y_e, cropp, temp
    if evt == cv2.EVENT_LBUTTONDOWN:
        x_st, y_st, x_e, y_e = xx, yy, xx, yy
        cropp = True  
    elif evt == cv2.EVENT_MOUSEMOVE:
        if cropp == True:
            x_e, y_e = xx, yy
    elif evt == cv2.EVENT_LBUTTONUP: 
        x_e, y_e = xx, yy
        cropp = False 
        rePoint = [(x_st, y_st), (x_e, y_e)]
        if len(rePoint) == 2: 
            point1.append(rePoint[0][1])
            point2.append(rePoint[1][1])
            point3.append(rePoint[0][0])
            point4.append(rePoint[1][0])                       

def length(image):
    while 1:
        i = image.copy()     
        if cropp == False:
            cv2.imshow('image', image)    
        elif cropp == True:
            cv2.line(i, (x_st, y_st), (x_e, y_e), (0, 256, 0), 2)
            cv2.imshow('image', i)
            length = abs(x_st-x_e) 
        key = cv2.waitKey(1)
        if key == ord('q'):
            break     
    cv2.destroyAllWindows()    
    return length
       
def pxls(read):
    image = cv2.imread(read)
    tempimage = image[image.shape[0]-300:image.shape[0],image.shape[1]-500:image.shape[1]]  
    cv2.rectangle(tempimage, (0,0), (image.shape[0],40), (0,0,0), -1)   
    cv2.putText(tempimage, 'draw a line as long as the micrometer per pixel', (0,30), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255,255,255), 1, cv2.LINE_AA)
    cv2.rectangle(tempimage, (0,35), (image.shape[0],80), (0,0,0), -1) 
    cv2.putText(tempimage, 'once that is done, press the Q key', (0,60), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255,255,255), 1, cv2.LINE_AA)    
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', mouse_draw)
    return length(tempimage)

def createWhite(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)                               
    lower_white = np.array([10,10,10])                                            
    upper_white = np.array([255,255,255])                                      
    mask = cv2.inRange(hsv, lower_white, upper_white)                          
    res = cv2.bitwise_and(image,image, mask= mask)                         
    res = cv2.GaussianBlur(res,(15,15),0)
    return cv2.medianBlur(res,15)

def blurImage(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)                               
    lower_white = np.array([0,0,0])                                            
    upper_white = np.array([255,255,255])                                      
    mask = cv2.inRange(hsv, lower_white, upper_white)                          
    res = cv2.bitwise_and(image,image, mask= mask)                         
    res = cv2.GaussianBlur(res,(15,15),0)
    return cv2.medianBlur(res,15)

def convertToGray(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return(image)
    
def gaussianTransform(image):
    return cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)
    
def prepareImage(image):
    image = blurImage(image)                                                
    image = convertToGray(image)                                                
    image = gaussianTransform(image)                                             
    return image
     
def displayImage(image,windowname):
    cv2.imshow(windowname, image)                                              
    cv2.waitKey(0)                                                             
    cv2.destroyAllWindows() 

def identifyWires(loc, image, w, h, cimage, wimage, result):
    count = 0                                                                 
    actualyield = 0                                                  
    for pt in zip(*loc[::-1]):                                                 
        cv2.rectangle(cimage, pt, (pt[0] + w, pt[1] + h), (0,255,0), 1)
        cv2.rectangle(result, pt, (pt[0] + w, pt[1] + h), (0,255,0), 1)
        cv2.circle(wimage,(pt[0] + w//2, pt[1] + h//2),10,(255,255,255),-1)      
        actualyield+=1                                                                                                         
        count += 1                                                            
    return (actualyield)                                                       

def matchFunction(image, template, threshold,cimage, wimage, result):
    res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)     
    loc = np.where(res >= threshold)                                          
    return identifyWires(loc, image, template.shape[0],template.shape[1], cimage, wimage, result) 

def mouse_crop(event, x, y, flags, param):
    global x_start, y_start, x_end, y_end, cropping, templates
    if event == cv2.EVENT_LBUTTONDOWN:
        x_start, y_start, x_end, y_end = x, y, x, y
        cropping = True  
    elif event == cv2.EVENT_MOUSEMOVE:
        if cropping == True:
            x_end, y_end = x, y
    elif event == cv2.EVENT_LBUTTONUP: 
        x_end, y_end = x, y
        cropping = False 
        refPoint = [(x_start, y_start), (x_end, y_end)]
        if len(refPoint) == 2: 
            roi = oriImage[refPoint[0][1]:refPoint[1][1], refPoint[0][0]:refPoint[1][0]]    
            points1.append(refPoint[0][1])
            points2.append(refPoint[1][1])
            points3.append(refPoint[0][0])
            points4.append(refPoint[1][0])           
            cv2.imshow('cropped', roi)
            
def createTemplates(image):
    for x in range(0,image.shape[1],100):
        cv2.line(image, (x,0), (x,image.shape[1]), (0,0,0), 1)
    for y in range(0,image.shape[0],100):
        cv2.line(image, (0,y), (image.shape[1],y), (0,0,0), 1)
    while 1:
        cv2.rectangle(image, (0,0), (212,40), (0,0,0), -1)   
        cv2.putText(image, 'templates:'+str(len(points1)), (0,30), cv2.FONT_HERSHEY_DUPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
        i = image.copy()     
        if cropping == False:
            cv2.imshow('image', image)    
        elif cropping == True:
            cv2.rectangle(i, (x_start, y_start), (x_end, y_end), (0, 255, 0), 1)
            cv2.imshow('image', i)
            templates.append(i) 
        key = cv2.waitKey(1)
        if key == ord('q'):
            break     
    cv2.destroyAllWindows()    
    for i in range (len(points1)):
        template = oriImage[points1[i]:points2[i], points3[i]:points4[i]]
        templates[i] = template
        
def thYield(image,pitch,read,scale):                      
    pitch /=1000
    height = image.shape[1]/scale
    width = image.shape[0]/scale                                            
    area = (height*width)
    return int((2*area)/(pitch*pitch*1.73205080757))

def loopThrough(image,value, result):
    image=(prepareImage(image))
    displayImage(image,'hi')
    for i in range(len(points1)):
        template = templates[i]
        template = prepareImage(template)
        matchFunction(image,template,value,cimage2,whiteimage, result)

def calculateYield(actualyield, theoreticalyield):
    return ((actualyield/theoreticalyield)*100) 

def contourDetect(whiteimage):
    th, contours, hierarchy = cv2.findContours(whiteimage, cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)    
    cv2.drawContours(whiteimage,contours,1,(255,255,255),6)
    return len(contours)

def showResult(result,whiteimage,scale):
    actualyield = contourDetect(whiteimage)
    theoreticalyield = int(thYield(oriImage,pitch,read,scale))
    percentageyield = int(calculateYield(actualyield,theoreticalyield))    
    ay = 'actual yield: '+str(actualyield)
    ty = 'theoretical yield: '+str(theoreticalyield)
    py = 'percentage yield: '+str(percentageyield)+'% +/- 15%'    
    cv2.rectangle(result, (0,0), (525,120), (0,0,0), -1)   
    cv2.putText(result, ay, (0,30), cv2.FONT_HERSHEY_DUPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
    cv2.putText(result, ty, (0,60), cv2.FONT_HERSHEY_DUPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
    cv2.putText(result, py, (0,90), cv2.FONT_HERSHEY_DUPLEX, 1, (255,255,255), 1, cv2.LINE_AA)    
    result = cv2.resize(result, (0,0), fx=0.8, fy=0.8) 
    displayImage(result,'result')
  
#MAIN-------------------------------------------------------------------------- 
if 1:
    #GUI-----------------------------------------------------------------------
    roots = tk.Tk()
    roots.geometry('600x550')
    msg3 = ttk.Label(text='')
    msg3.pack()
    title = ttk.Label(text='ENTER IMAGE PATH')  
    title.place(x=326,y=275)
    e = ttk.Entry(roots)
    e.place(x=314,y=325)
    e.focus_set()
    b = ttk.Button(roots,text='ENTER',command=printx)
    b.place(x=341,y=370)
    roots.mainloop()
      
    #TEMPLATE------------------------------------------------------------------
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', mouse_crop)  
      
    #IMAGE---------------------------------------------------------------------
    img = cv2.imread(read)
    cimage = cv2.imread(read)
    cimage2 = cv2.imread(read)
    result = cv2.imread(read)
    oriImage = cv2.imread(read)
    image2 = cv2.imread(read)    
    whiteimage = convertToGray(createWhite(img))
       
    #MATCH---------------------------------------------------------------------
    createTemplates(cimage)
    loopThrough(img,0.838, result)
       
    #MOUSE---------------------------------------------------------------------
    x_start, y_start, x_end, y_end = 0, 0, 0, 0
    points1,points2,points3,points4,templates = [],[],[],[],[]
    cropping = False
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', mouse_crop) 
       
    #MATCHx2-------------------------------------------------------------------
    createTemplates(cimage2) 
    loopThrough(image2,0.838, result)
       
    #GUI-----------------------------------------------------------------------
    root = tk.Tk()
    root.geometry('600x550')
    e = ttk.Entry(root)
    e.pack(side = 'right')
    e.focus_set()
    title = ttk.Label(text='ENTER PITCH')  
    title.pack(side = 'left')
    b = ttk.Button(root,text='ENTER',command=printtext)
    b.pack(side='bottom')
    root.mainloop()
    
    #GUI-----------------------------------------------------------------------
    scale = pxls(read)
    rootb = tk.Tk()
    rootb.geometry('600x550')
    eb = ttk.Entry(rootb)
    eb.pack()
    eb.focus_set()
    titleb = ttk.Label(text='ENTER WHAT THE NUMBER OF PIXELS REPRESENTS')  
    titleb.pack()
    bb = ttk.Button(rootb,text='NM',command=lambda:convert(0))
    bb.pack()
    bb1 = ttk.Button(rootb,text='MM',command=lambda:convert(1))
    bb1.pack()
    rootb.mainloop()
    
    #RESULT--------------------------------------------------------------------
    showResult(result,whiteimage,scale)
