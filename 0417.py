import pupil_apriltags as apriltag 
import cv2
import numpy as np
import time
from pupil_apriltags import Detector

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cv2.namedWindow('camera', cv2.WINDOW_AUTOSIZE)
detector1 = apriltag.Detector(families='tag36h11')


initial_color_done=[0,0,0,0,0,0]#white blue green orange red white #確認各顏色為中心之面是否完成掃描
initial_color=[[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]#white blue green orange red white
               ,[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]#各顏色為中心之面的初始顏色

now_color=[0,0,0,0,0,0,0,0,0]#讀取進來之九宮格

color_detect_x=[0,0,0,0,0,0,0,0,0]#tag之x座標
color_detect_y=[0,0,0,0,0,0,0,0,0]#tag之y座標
color_detect_id=[0,0,0,0,0,0,0,0,0]#tag之id

def check_edge(x,y):#確認兩個tag是否為同一邊塊
    if((x==2 and y==20)or(x==20 and y==2)):#白綠
        return 1
    elif((x==4 and y==38)or(x==38 and y==4)):#白紅
        return 1
    elif((x==6 and y==29)or(x==29 and y==6)):#白橘
        return 1
    elif((x==8 and y==11)or(x==11 and y==8)):#白藍
        return 1
    elif((x==13 and y==42)or(x==42 and y==13)):#藍紅
        return 1
    elif((x==15 and y==31)or(x==31 and y==15)):#藍橘
        return 1
    elif((x==24 and y==40)or(x==40 and y==24)):#綠紅
        return 1
    elif((x==22 and y==33)or(x==33 and y==22)):#綠橘
        return 1
    elif((x==47 and y==17)or(x==17 and y==47)):#黃藍
        return 1
    elif((x==49 and y==44)or(x==44 and y==49)):#黃紅
        return 1
    elif((x==51 and y==35)or(x==35 and y==51)):#黃橘
        return 1
    elif((x==53 and y==26)or(x==26 and y==53)):#黃綠
        return 1
    else :#都不是
        return 0
    
def print_color(x):#把tag id換成顏色
    if(x>=1 and x<=9):
        return'白'
    elif(x>=10 and x<=18):
        return'藍'
    elif(x>=19 and x<=27):
        return'綠'
    elif(x>=28 and x<=36):
        return'橘'
    elif(x>=37 and x<=45):
        return'紅'
    elif(x>=46 and x<=54):
        return'黃'


while (1):
    ret, image = cap.read()

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    count=0
    
    results1 = detector1.detect(gray)
    
    for tag in results1:
        count=count+1
    
    if(count==9):
        count=0
        for tag in results1:
        
            cv2.circle(image, tuple(tag.corners[0].astype(int)), 4,(255,255,255), 2)
            cv2.circle(image, tuple(tag.corners[1].astype(int)), 4,(255,255,255), 2)
            cv2.circle(image, tuple(tag.corners[2].astype(int)), 4,(255,255,255), 2)
            cv2.circle(image, tuple(tag.corners[3].astype(int)), 4,(255,255,255), 2)
            
            color_detect_x[count]=tag.corners[0].astype(int)[0]
            color_detect_y[count]=tag.corners[0].astype(int)[1]
            color_detect_id[count]=tag.tag_id
            
            count=count+1
    
        
    for i in range(8,0,-1):
        for j in range(0,i):
            if(color_detect_y[j]>color_detect_y[j+1]):
                temp=color_detect_x[j]
                color_detect_x[j]=color_detect_x[j+1]
                color_detect_x[j+1]=temp
                temp=color_detect_y[j]
                color_detect_y[j]=color_detect_y[j+1]
                color_detect_y[j+1]=temp
                temp=color_detect_id[j]
                color_detect_id[j]=color_detect_id[j+1]
                color_detect_id[j+1]=temp

                
    for i in range(2,0,-1):
        for j in range(0,i):
            if(color_detect_x[j]>color_detect_x[j+1]):
                temp=color_detect_x[j]
                color_detect_x[j]=color_detect_x[j+1]
                color_detect_x[j+1]=temp
                temp=color_detect_y[j]
                color_detect_y[j]=color_detect_y[j+1]
                color_detect_y[j+1]=temp
                temp=color_detect_id[j]
                color_detect_id[j]=color_detect_id[j+1]
                color_detect_id[j+1]=temp
    for i in range(5,3,-1):
        for j in range(3,i):
            if(color_detect_x[j]>color_detect_x[j+1]):
                temp=color_detect_x[j]
                color_detect_x[j]=color_detect_x[j+1]
                color_detect_x[j+1]=temp
                temp=color_detect_y[j]
                color_detect_y[j]=color_detect_y[j+1]
                color_detect_y[j+1]=temp
                temp=color_detect_id[j]
                color_detect_id[j]=color_detect_id[j+1]
                color_detect_id[j+1]=temp
    for i in range(8,6,-1):
        for j in range(6,i):
            if(color_detect_x[j]>color_detect_x[j+1]):
                temp=color_detect_x[j]
                color_detect_x[j]=color_detect_x[j+1]
                color_detect_x[j+1]=temp
                temp=color_detect_y[j]
                color_detect_y[j]=color_detect_y[j+1]
                color_detect_y[j+1]=temp
                temp=color_detect_id[j]
                color_detect_id[j]=color_detect_id[j+1]
                color_detect_id[j+1]=temp

    
    for i in range(0,9):
        now_color[i]=color_detect_id[i]
        
    if(initial_color_done[int((now_color[4]-5)/9)]==0 and now_color[4]!=0):
        initial_color_done[int((now_color[4]-5)/9)]=1
        for i in range(0,9):
            initial_color[int((now_color[4]-5)/9)][i]=color_detect_id[i]
            

      
    cv2.imshow('camera', image)
    cv2.waitKey(1)
    
    if(sum(initial_color_done)==6):
        break

for i in range(1,5):
    for j in range(1,5):
        if j==1:
            index=7
        if j==2:
            index=1
        if j==3 :
            index=5
        if j==4:
            index=3
        for k in range(1,5):
            if(check_edge(initial_color[0][index],initial_color[i][1])==1):
                break
            temp=initial_color[i][1]
            initial_color[i][1]=initial_color[i][3]
            initial_color[i][3]=initial_color[i][7]
            initial_color[i][7]=initial_color[i][5]
            initial_color[i][5]=temp
            temp=initial_color[i][0]
            initial_color[i][0]=initial_color[i][6]
            initial_color[i][6]=initial_color[i][8]
            initial_color[i][8]=initial_color[i][2]
            initial_color[i][2]=temp


while(check_edge(initial_color[1][7],initial_color[5][1])==0):
    temp=initial_color[5][1]
    initial_color[5][1]=initial_color[5][3]
    initial_color[5][3]=initial_color[5][7]
    initial_color[5][7]=initial_color[5][5]
    initial_color[5][5]=temp
    temp=initial_color[5][0]
    initial_color[5][0]=initial_color[5][6]
    initial_color[5][6]=initial_color[5][8]
    initial_color[5][8]=initial_color[5][2]
    initial_color[5][2]=temp        

for i in range(1,5):
    if(check_edge(initial_color[0][7],initial_color[1][1])==1):
        break
    temp=initial_color[0][1]
    initial_color[0][1]=initial_color[0][3]
    initial_color[0][3]=initial_color[0][7]
    initial_color[0][7]=initial_color[0][5]
    initial_color[0][5]=temp
    temp=initial_color[0][0]
    initial_color[0][0]=initial_color[0][6]
    initial_color[0][6]=initial_color[0][8]
    initial_color[0][8]=initial_color[0][2]
    initial_color[0][2]=temp
    
    
print('display:')
for i in range(0,6):
    print('\n')
    for j in range(0,3):
        print(print_color(initial_color[i][3*j]),
              print_color(initial_color[i][3*j+1]),
              print_color(initial_color[i][3*j+2]),'\n')

    

