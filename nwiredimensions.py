from PIL import Image, ImageTk
from xlwt import Workbook
from scipy import ndimage
from tkinter import ttk 
import matplotlib.pyplot as plt
import tkinter as tk
import numpy as np
import cv2

#GLOBAL VARIABLES--------------------------------------------------------------
wb = Workbook()  
x_st, y_st, x_e, y_e = 0, 0, 0, 0
point1,point2,point3,point4 = [],[],[],[]                                      
cropp = False

#FUNCTIONS---------------------------------------------------------------------
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

def setFunction(param):
    global ek, ek1, ek2, ek3, ek4, scale, tilt, t, howmany, path, root, roota, roota1, roota2, roota3
    if param == 1 : 
        tilt = float(ek1.get())
        roota.destroy()
    if param == 2 : 
        t = float(ek2.get())
        roota1.destroy()
    if param == 3 : 
        howmany = int(ek3.get())
        roota2.destroy()
    if param == 4 : 
        path = ek4.get()
        roota3.destroy()

def setFileName():
    global e1, excelname, roots
    string = e1.get()
    excelname = string+'.xls'
    roots.destroy()

def filter_pic(picture, sigma, threshold):
    pic = ndimage.imread(picture, mode  = 'L', flatten = True)                
    pic = ndimage.gaussian_filter(pic, sigma)                                                          
    pic_grad = np.gradient(pic)                                                     
    Gx = pic_grad[0]
    Gy = pic_grad[1]
    mag = np.sqrt(Gx**2 + Gy**2)                                               
    over = (mag > threshold).astype(int)
    thresh = mag*over  
    return thresh

def showImgB(image,path,root,value):
    cv2.imwrite(('gray'+path),ndimage.gaussian_filter(image,value))
    image = 'gray'+path
    load = Image.open(image)
    render = ImageTk.PhotoImage(load)
    img = tk.Label(root, image=render)
    img.image = render
    img.place(x=100, y=100)      

def printtext():
    global e, sigma
    string = e.get() 
    value = (float(string))    
    sigma = value
    pic_array = filter_pic(path, value, 4.0)    
    thresh_pic = plt.figure(1)
    thresh_pic_ax = thresh_pic.add_subplot(111)
    thresh_pic_ax.imshow(pic_array, interpolation = "None", cmap = 'pink')
    thresh_pic_ax.axis("off")
    thresh_pic.subplots_adjust(left = 0, right = 1, top = 1, bottom = 0)
    plt.draw()    
    showImgB(image,path,root,value)

def maximum(picture, row, column, L_or_R):                                      
    if L_or_R == "Right":
        while picture[row, column] <= picture[row, column + 1]:
            column += 1
    else:
        while picture[row, column] <= picture[row, column - 1]:
            column -= 1
    return column

def subpixel(picture, row, column, L_or_R, max_col):                           
    g = []
    d = []
    while picture[row, column] != 0:
        g.append(picture[row, column])
        d.append(column - max_col)
        if L_or_R == "Right":
            column += 1
        else:
            column -= 1
    g = np.array(g)
    d = np.array(d)
    delta = sum(g*d)/sum(g)
    return delta 

def plotPoints(picture_ax, right_point, left_point, height_point):
    picture_ax.scatter(right_point, height_point, color = 'c', marker = '.')
    picture_ax.scatter(left_point, height_point, color = 'm', marker  = '.')
    plt.draw()            

def find_edge(m_value, n_value):
    m = m_value
    n = n_value
    value = pic_array[m, n]
    while value == 0:                                               
        n += 1
        value = pic_array[m, n]
    n_nonzero = n
    n_max = maximum(pic_array, m, n, "Right")
    subpixel_n = subpixel(pic_array, m, n_nonzero, "Right", n_max) + n_max
    right = subpixel_n  
    n = n_value
    value = pic_array[m, n]    
    while value == 0:                                                         
        n -= 1
        value = pic_array[m, n]
    n_nonzero = n
    n_max = maximum(pic_array, m, n, "Left")
    subpixel_n = subpixel(pic_array, m, n_nonzero, "Left", n_max) + n_max
    left = subpixel_n    
    return (right, left, m)                                                    

def click(event):
    global diam, height, special, specialcount, diam_pix, height_pix, clicks, count, num
    n_orig = int(event.xdata)
    m_orig = int(event.ydata)        
    if specialcount != 0:
        results = find_edge(m_orig, n_orig)
        plotPoints(thresh_pic_ax, results[0], results[1], results[2])
        diam_pix.append(abs(results[0] - results[1]))
        height_pix.append(results[2])
        specialcount -= 1
    else:
        results = find_edge(m_orig, n_orig)
        plotPoints(thresh_pic_ax, results[0], results[1], results[2])
        diam_pix.append(abs(results[0] - results[1]))
        height_pix.append(results[2])  
        diam = np.array(diam_pix)/scale
        height = np.array(height_pix)
        height = ((height - height[0])/scale)/np.sin(np.radians(tilt))
        for i in range(len(height)):
            print (str(abs(height[i])).ljust(15), '\t', diam[i])
            sheet1.write(count,0,str(diam[i])+' mm')
            sheet1.write(count,1,str(abs(height[i]))+' mm')
            count+=1
            num+=1
            if(height[i-special] == 0):
               count+=1
            wb.save(excelname)
        print ('\n')
        diam_pix = []
        height_pix = []
        diam = []
        height = []
        specialcount = special       
    clicks+=1    
    if(clicks == 1):
         print('\n')
         print("Height (mm)\t\t Diameter (mm)")  

#MAIN--------------------------------------------------------------------------
if 1:
    #GUI-----------------------------------------------------------------------
    roota3 = tk.Tk()
    roota3.geometry('250x250')
    lbl4 = ttk.Label(text='ENTER IMAGE PATH')
    lbl4.pack()
    ek4 = ttk.Entry(roota3)
    ek4.pack()
    ek4.focus_set()
    bk4 = ttk.Button(roota3, text='ENTER',command = lambda: setFunction(4))
    bk4.pack()
    roota3.mainloop()
    
    #GUI-----------------------------------------------------------------------
    root = tk.Tk()
    root.geometry('500x500')
    image = cv2.imread(path)
    image = image[0:(image.shape[0]-(image.shape[0]-300)),0:(image.shape[1]-(image.shape[1]-300))]
    msg = ttk.Label(text='ENTER SIGMA')
    msg.pack()
    e = ttk.Entry(root)
    e.pack()
    e.focus_set()
    b = ttk.Button(root,text='ENTER',command=printtext)
    b.pack()
    root.mainloop()
    
    #GUI-----------------------------------------------------------------------
    roota = tk.Tk()
    roota.geometry('250x250')
    lbl1 = ttk.Label(text='ENTER TILT DEGREES')
    lbl1.pack()
    ek1 = ttk.Entry(roota)
    ek1.pack()
    ek1.focus_set()
    bk1 = ttk.Button(roota, text='ENTER',command = lambda: setFunction(1))
    bk1.pack()
    roota.mainloop()
    
    #GUI-----------------------------------------------------------------------
    roota1 = tk.Tk()
    roota1.geometry('250x250')
    lbl2 = ttk.Label(text='ENTER THRESHOLD (4.0)')
    lbl2.pack()
    ek2 = ttk.Entry(roota1)
    ek2.pack()
    ek2.focus_set()
    bk2 = ttk.Button(roota1, text='ENTER',command = lambda: setFunction(2))
    bk2.pack()
    roota1.mainloop()
    
    #GUI-----------------------------------------------------------------------
    roota2 = tk.Tk()
    roota2.geometry('250x250')
    lbl3 = ttk.Label(text='ENTER NUM OF POINTS TO TAKE')
    lbl3.pack()
    ek3 = ttk.Entry(roota2)
    ek3.pack()
    ek3.focus_set()
    bk3 = ttk.Button(roota2, text='ENTER',command = lambda: setFunction(3))
    bk3.pack()
    roota2.mainloop()
    
    #GUI-----------------------------------------------------------------------
    roots = tk.Tk()
    roots.geometry('250x250')
    msg1 = ttk.Label(text='ENTER FILE NAME FOR EXCEL SHEET')
    msg1.pack()
    e1 = ttk.Entry(roots)
    e1.pack()
    e1.focus_set()
    b1 = ttk.Button(roots,text='ENTER',command=setFileName)
    b1.pack()
    roots.mainloop()
    
    #SPREADSHEET---------------------------------------------------------------
    sheet1 = wb.add_sheet("Sheet 1")
    sheet1.write(0,1,'HEIGHT')
    sheet1.write(0,0,'DIAMETER')
    sheet1.write(1,0,'')
    sheet1.write(1,1,'')
    sheet1.col(0).width = 6000
    sheet1.col(1).width = 6000
    sheet1.col(2).width = 6000
       
    #PARAMETERS----------------------------------------------------------------                       
    img_name = path
    unfiltered = ndimage.imread(img_name)                                                             
    count = 2 
    num = 1
    step = 50                                                                 
    special = howmany-1
    specialcount = special                                                     
    diam_pix = []
    height_pix = []
    clicks = 0
    press = 0
    number = 0 
    scale = pxls(img_name)
    
    #GUI-----------------------------------------------------------------------
    rootb = tk.Tk()
    rootb.geometry('600x550')
    eb = ttk.Entry(rootb)
    eb.pack()
    eb.focus_set()
    titleb = ttk.Label(text='ENTER SCALE BAR CONVERSION IN MICRONS')  
    titleb.pack()
    bb = ttk.Button(rootb,text='NM',command=lambda:convert(0))
    bb.pack()
    bb1 = ttk.Button(rootb,text='MM',command=lambda:convert(1))
    bb1.pack()
    rootb.mainloop()
    print(scale)
       
    #MATPLOTLIB----------------------------------------------------------------
    pic_array = filter_pic(img_name, sigma, t)  
    thresh_pic = plt.figure(1)
    thresh_pic_ax = thresh_pic.add_subplot(111)
    thresh_pic_ax.imshow(pic_array, interpolation = "None", cmap = 'pink')
    thresh_pic_ax.axis("off")
    thresh_pic.subplots_adjust(left = 0, right = 1, top = 1, bottom = 0)
    plt.draw()    
    
    #GRAB CLICKS---------------------------------------------------------------
    cid = thresh_pic.canvas.mpl_connect('button_press_event', click) 
