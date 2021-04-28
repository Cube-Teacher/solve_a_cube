import pupil_apriltags as apriltag 
import cv2
import numpy as np
import time
from pupil_apriltags import Detector

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cv2.namedWindow('camera', cv2.WINDOW_AUTOSIZE)
detector1 = apriltag.Detector(families='tag36h11')

start_flag=0

key=0

operation=[]

initial_color_done=[0,0,0,0,0,0]#white blue green orange red white #確認各顏色為中心之面是否完成掃描
initial_color=[[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]#white blue green orange red white
               ,[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]#各顏色為中心之面的初始顏色

now_color=[0,0,0,0,0,0,0,0,0]#讀取進來之九宮格
top_color=[0,0,0,0,0,0,0,0,0]

color_detect_x=[0,0,0,0,0,0,0,0,0]#tag之x座標
color_detect_y=[0,0,0,0,0,0,0,0,0]#tag之y座標
color_detect_id=[0,0,0,0,0,0,0,0,0]#tag之id

def swap_four_element(w,x,y,z):
    return x,y,z,w


def check_valid():
    if(top_color[0]==now_color[0] and top_color[1]==now_color[1] and top_color[3]==now_color[3]#右排下轉
   and top_color[4]==now_color[4] and top_color[6]==now_color[6] and top_color[7]==now_color[7]
   and now_color[2]==initial_color[2][6] and now_color[5]==initial_color[2][3] and now_color[8]==initial_color[2][0]):
        initial_color[0][2],initial_color[2][6],initial_color[5][2],initial_color[1][2]=swap_four_element(initial_color[0][2],initial_color[2][6],initial_color[5][2],initial_color[1][2])
        initial_color[0][5],initial_color[2][3],initial_color[5][5],initial_color[1][5]=swap_four_element(initial_color[0][5],initial_color[2][3],initial_color[5][5],initial_color[1][5])
        initial_color[0][8],initial_color[2][0],initial_color[5][8],initial_color[1][8]=swap_four_element(initial_color[0][8],initial_color[2][0],initial_color[5][8],initial_color[1][8])
        initial_color[3][0],initial_color[3][2],initial_color[3][8],initial_color[3][6]=swap_four_element(initial_color[3][0],initial_color[3][2],initial_color[3][8],initial_color[3][6])
        initial_color[3][1],initial_color[3][5],initial_color[3][7],initial_color[3][3]=swap_four_element(initial_color[3][1],initial_color[3][5],initial_color[3][7],initial_color[3][3])
        return 1
    
    elif(top_color[0]==now_color[0] and top_color[1]==now_color[1] and top_color[3]==now_color[3]#右排上轉
   and top_color[4]==now_color[4] and top_color[6]==now_color[6] and top_color[7]==now_color[7]
   and now_color[2]==initial_color[1][2] and now_color[5]==initial_color[1][5] and now_color[8]==initial_color[1][8]):
        initial_color[0][2],initial_color[1][2],initial_color[5][2],initial_color[2][6]=swap_four_element(initial_color[0][2],initial_color[1][2],initial_color[5][2],initial_color[2][6])
        initial_color[0][5],initial_color[1][5],initial_color[5][5],initial_color[2][3]=swap_four_element(initial_color[0][5],initial_color[1][5],initial_color[5][5],initial_color[2][3])
        initial_color[0][8],initial_color[1][8],initial_color[5][8],initial_color[2][0]=swap_four_element(initial_color[0][8],initial_color[1][8],initial_color[5][8],initial_color[2][0])
        initial_color[3][0],initial_color[3][6],initial_color[3][8],initial_color[3][2]=swap_four_element(initial_color[3][0],initial_color[3][6],initial_color[3][8],initial_color[3][2])
        initial_color[3][1],initial_color[3][3],initial_color[3][7],initial_color[3][5]=swap_four_element(initial_color[3][1],initial_color[3][3],initial_color[3][7],initial_color[3][5])
        return 2
    
    elif(top_color[1]==now_color[1] and top_color[2]==now_color[2] and top_color[4]==now_color[4]#左排下轉
   and top_color[5]==now_color[5] and top_color[7]==now_color[7] and top_color[8]==now_color[8]
   and now_color[0]==initial_color[2][8] and now_color[3]==initial_color[2][5] and now_color[6]==initial_color[2][2]):
        initial_color[0][0],initial_color[2][8],initial_color[5][0],initial_color[1][0]=swap_four_element(initial_color[0][0],initial_color[2][8],initial_color[5][0],initial_color[1][0])
        initial_color[0][3],initial_color[2][5],initial_color[5][3],initial_color[1][3]=swap_four_element(initial_color[0][3],initial_color[2][5],initial_color[5][3],initial_color[1][3])
        initial_color[0][6],initial_color[2][2],initial_color[5][6],initial_color[1][6]=swap_four_element(initial_color[0][6],initial_color[2][2],initial_color[5][6],initial_color[1][6])
        initial_color[4][0],initial_color[4][6],initial_color[4][8],initial_color[4][2]=swap_four_element(initial_color[4][0],initial_color[4][6],initial_color[4][8],initial_color[4][2])
        initial_color[4][1],initial_color[4][3],initial_color[4][7],initial_color[4][5]=swap_four_element(initial_color[4][1],initial_color[4][3],initial_color[4][7],initial_color[4][5])
        return 3
    
    elif(top_color[1]==now_color[1] and top_color[2]==now_color[2] and top_color[4]==now_color[4]#左排上轉
   and top_color[5]==now_color[5] and top_color[7]==now_color[7] and top_color[8]==now_color[8]
   and now_color[0]==initial_color[1][0] and now_color[3]==initial_color[1][3] and now_color[6]==initial_color[1][6]):
        initial_color[0][0],initial_color[1][0],initial_color[5][0],initial_color[2][8]=swap_four_element(initial_color[0][0],initial_color[1][0],initial_color[5][0],initial_color[2][8])
        initial_color[0][3],initial_color[1][3],initial_color[5][3],initial_color[2][5]=swap_four_element(initial_color[0][3],initial_color[1][3],initial_color[5][3],initial_color[2][5])
        initial_color[0][6],initial_color[1][6],initial_color[5][6],initial_color[2][2]=swap_four_element(initial_color[0][6],initial_color[1][6],initial_color[5][6],initial_color[2][2])
        initial_color[4][0],initial_color[4][2],initial_color[4][8],initial_color[4][6]=swap_four_element(initial_color[4][0],initial_color[4][2],initial_color[4][8],initial_color[4][6])
        initial_color[4][1],initial_color[4][5],initial_color[4][7],initial_color[4][3]=swap_four_element(initial_color[4][1],initial_color[4][5],initial_color[4][7],initial_color[4][3])
        return 4
    
    elif(top_color[3]==now_color[3] and top_color[4]==now_color[4] and top_color[5]==now_color[5]#上排右轉
   and top_color[6]==now_color[6] and top_color[7]==now_color[7] and top_color[8]==now_color[8]
   and now_color[0]==initial_color[4][6] and now_color[1]==initial_color[4][3] and now_color[2]==initial_color[4][0]):
        initial_color[0][0],initial_color[4][6],initial_color[5][8],initial_color[3][2]=swap_four_element(initial_color[0][0],initial_color[4][6],initial_color[5][8],initial_color[3][2])
        initial_color[0][1],initial_color[4][3],initial_color[5][7],initial_color[3][5]=swap_four_element(initial_color[0][1],initial_color[4][3],initial_color[5][7],initial_color[3][5])
        initial_color[0][2],initial_color[4][0],initial_color[5][6],initial_color[3][8]=swap_four_element(initial_color[0][2],initial_color[4][0],initial_color[5][6],initial_color[3][8])
        initial_color[2][0],initial_color[2][2],initial_color[2][8],initial_color[2][6]=swap_four_element(initial_color[2][0],initial_color[2][2],initial_color[2][8],initial_color[2][6])
        initial_color[2][1],initial_color[2][5],initial_color[2][7],initial_color[2][3]=swap_four_element(initial_color[2][1],initial_color[2][5],initial_color[2][7],initial_color[2][3])
        return 5
    
    elif(top_color[3]==now_color[3] and top_color[4]==now_color[4] and top_color[5]==now_color[5]#上排左轉
   and top_color[6]==now_color[6] and top_color[7]==now_color[7] and top_color[8]==now_color[8]
   and now_color[0]==initial_color[3][2] and now_color[1]==initial_color[3][5] and now_color[2]==initial_color[3][8]):
        initial_color[0][0],initial_color[3][2],initial_color[5][8],initial_color[4][6]=swap_four_element(initial_color[0][0],initial_color[3][2],initial_color[5][8],initial_color[4][6])
        initial_color[0][1],initial_color[3][5],initial_color[5][7],initial_color[4][3]=swap_four_element(initial_color[0][1],initial_color[3][5],initial_color[5][7],initial_color[4][3])
        initial_color[0][2],initial_color[3][8],initial_color[5][6],initial_color[4][0]=swap_four_element(initial_color[0][2],initial_color[3][8],initial_color[5][6],initial_color[4][0])
        initial_color[2][0],initial_color[2][6],initial_color[2][8],initial_color[2][2]=swap_four_element(initial_color[2][0],initial_color[2][6],initial_color[2][8],initial_color[2][2])
        initial_color[2][1],initial_color[2][3],initial_color[2][7],initial_color[2][5]=swap_four_element(initial_color[2][1],initial_color[2][3],initial_color[2][7],initial_color[2][5])
        return 6
    
    elif(top_color[0]==now_color[0] and top_color[1]==now_color[1] and top_color[2]==now_color[2]#下排右轉
   and top_color[3]==now_color[3] and top_color[4]==now_color[4] and top_color[5]==now_color[5]
   and now_color[6]==initial_color[4][8] and now_color[7]==initial_color[4][5] and now_color[8]==initial_color[4][2]):
        initial_color[0][6],initial_color[4][8],initial_color[5][2],initial_color[3][0]=swap_four_element(initial_color[0][6],initial_color[4][8],initial_color[5][2],initial_color[3][0])
        initial_color[0][7],initial_color[4][5],initial_color[5][1],initial_color[3][3]=swap_four_element(initial_color[0][7],initial_color[4][5],initial_color[5][1],initial_color[3][3])
        initial_color[0][8],initial_color[4][2],initial_color[5][0],initial_color[3][6]=swap_four_element(initial_color[0][8],initial_color[4][2],initial_color[5][0],initial_color[3][6])
        initial_color[1][0],initial_color[1][6],initial_color[1][8],initial_color[1][2]=swap_four_element(initial_color[1][0],initial_color[1][6],initial_color[1][8],initial_color[1][2])
        initial_color[1][1],initial_color[1][3],initial_color[1][7],initial_color[1][5]=swap_four_element(initial_color[1][1],initial_color[1][3],initial_color[1][7],initial_color[1][5])
        return 7
    
    elif(top_color[0]==now_color[0] and top_color[1]==now_color[1] and top_color[2]==now_color[2]#下排左轉
   and top_color[3]==now_color[3] and top_color[4]==now_color[4] and top_color[5]==now_color[5]
   and now_color[6]==initial_color[3][0] and now_color[7]==initial_color[3][3] and now_color[8]==initial_color[3][6]):
        initial_color[0][6],initial_color[3][0],initial_color[5][2],initial_color[4][8]=swap_four_element(initial_color[0][6],initial_color[3][0],initial_color[5][2],initial_color[4][8])
        initial_color[0][7],initial_color[3][3],initial_color[5][1],initial_color[4][5]=swap_four_element(initial_color[0][7],initial_color[3][3],initial_color[5][1],initial_color[4][5])
        initial_color[0][8],initial_color[3][6],initial_color[5][0],initial_color[4][2]=swap_four_element(initial_color[0][8],initial_color[3][6],initial_color[5][0],initial_color[4][2])
        initial_color[1][0],initial_color[1][2],initial_color[1][8],initial_color[1][6]=swap_four_element(initial_color[1][0],initial_color[1][2],initial_color[1][8],initial_color[1][6])
        initial_color[1][1],initial_color[1][5],initial_color[1][7],initial_color[1][3]=swap_four_element(initial_color[1][1],initial_color[1][5],initial_color[1][7],initial_color[1][3])
        return 8
    
    elif(top_color[0]==now_color[0] and top_color[2]==now_color[2] and top_color[3]==now_color[3]#中排下轉
   and top_color[5]==now_color[5] and top_color[6]==now_color[6] and top_color[8]==now_color[8]
   and now_color[1]==initial_color[2][7] and now_color[4]==initial_color[2][4] and now_color[7]==initial_color[2][1]):
        initial_color[0][1],initial_color[2][7],initial_color[5][1],initial_color[1][1]=swap_four_element(initial_color[0][1],initial_color[2][7],initial_color[5][1],initial_color[1][1])
        initial_color[0][4],initial_color[2][4],initial_color[5][4],initial_color[1][4]=swap_four_element(initial_color[0][4],initial_color[2][4],initial_color[5][4],initial_color[1][4])
        initial_color[0][7],initial_color[2][1],initial_color[5][7],initial_color[1][7]=swap_four_element(initial_color[0][7],initial_color[2][1],initial_color[5][7],initial_color[1][7])
        return 9
    
    elif(top_color[0]==now_color[0] and top_color[2]==now_color[2] and top_color[3]==now_color[3]#中排上轉
   and top_color[5]==now_color[5] and top_color[6]==now_color[6] and top_color[8]==now_color[8]
   and now_color[1]==initial_color[1][1] and now_color[4]==initial_color[1][4] and now_color[7]==initial_color[1][7]):
        initial_color[0][1],initial_color[1][1],initial_color[5][1],initial_color[2][7]=swap_four_element(initial_color[0][1],initial_color[1][1],initial_color[5][1],initial_color[2][7])
        initial_color[0][4],initial_color[1][4],initial_color[5][4],initial_color[2][4]=swap_four_element(initial_color[0][4],initial_color[1][4],initial_color[5][4],initial_color[2][4])
        initial_color[0][7],initial_color[1][7],initial_color[5][7],initial_color[2][1]=swap_four_element(initial_color[0][7],initial_color[1][7],initial_color[5][7],initial_color[2][1])
        return 10
    
    elif(top_color[0]==now_color[0] and top_color[1]==now_color[1] and top_color[2]==now_color[2]#橫排右轉
   and top_color[6]==now_color[6] and top_color[7]==now_color[7] and top_color[8]==now_color[8]
   and now_color[3]==initial_color[4][7] and now_color[4]==initial_color[4][4] and now_color[5]==initial_color[4][1]):
        initial_color[0][3],initial_color[4][7],initial_color[5][5],initial_color[3][1]=swap_four_element(initial_color[0][3],initial_color[4][7],initial_color[5][5],initial_color[3][1])
        initial_color[0][4],initial_color[4][4],initial_color[5][4],initial_color[3][4]=swap_four_element(initial_color[0][4],initial_color[4][4],initial_color[5][4],initial_color[3][4])
        initial_color[0][5],initial_color[4][1],initial_color[5][3],initial_color[3][7]=swap_four_element(initial_color[0][5],initial_color[4][1],initial_color[5][3],initial_color[3][7])
        return 11
    
    elif(top_color[0]==now_color[0] and top_color[1]==now_color[1] and top_color[2]==now_color[2]#橫排左轉
   and top_color[6]==now_color[6] and top_color[7]==now_color[7] and top_color[8]==now_color[8]
   and now_color[3]==initial_color[3][1] and now_color[4]==initial_color[3][4] and now_color[5]==initial_color[3][7]):
        initial_color[0][3],initial_color[3][1],initial_color[5][5],initial_color[4][7]=swap_four_element(initial_color[0][3],initial_color[3][1],initial_color[5][5],initial_color[4][7])
        initial_color[0][4],initial_color[3][4],initial_color[5][4],initial_color[4][4]=swap_four_element(initial_color[0][4],initial_color[3][4],initial_color[5][4],initial_color[4][4])
        initial_color[0][5],initial_color[3][7],initial_color[5][3],initial_color[4][1]=swap_four_element(initial_color[0][5],initial_color[3][7],initial_color[5][3],initial_color[4][1])
        return 12
    
    elif(top_color[0]==now_color[2] and top_color[1]==now_color[5] and top_color[2]==now_color[8]#右轉
   and top_color[3]==now_color[1] and top_color[4]==now_color[4] and top_color[5]==now_color[7]
   and top_color[6]==now_color[0] and top_color[7]==now_color[3] and top_color[8]==now_color[6] and key==0):
        initial_color[0][0],initial_color[0][6],initial_color[0][8],initial_color[0][2]=swap_four_element(initial_color[0][0],initial_color[0][6],initial_color[0][8],initial_color[0][2])
        initial_color[0][1],initial_color[0][3],initial_color[0][7],initial_color[0][5]=swap_four_element(initial_color[0][1],initial_color[0][3],initial_color[0][7],initial_color[0][5])
        initial_color[1][0],initial_color[3][0],initial_color[2][0],initial_color[4][0]=swap_four_element(initial_color[1][0],initial_color[3][0],initial_color[2][0],initial_color[4][0])
        initial_color[1][1],initial_color[3][1],initial_color[2][1],initial_color[4][1]=swap_four_element(initial_color[1][1],initial_color[3][1],initial_color[2][1],initial_color[4][1])
        initial_color[1][2],initial_color[3][2],initial_color[2][2],initial_color[4][2]=swap_four_element(initial_color[1][2],initial_color[3][2],initial_color[2][2],initial_color[4][2])
        return 13
    
    elif(top_color[0]==now_color[6] and top_color[1]==now_color[3] and top_color[2]==now_color[0]#左轉
   and top_color[3]==now_color[7] and top_color[4]==now_color[4] and top_color[5]==now_color[1]
   and top_color[6]==now_color[8] and top_color[7]==now_color[5] and top_color[8]==now_color[2] and key==0):
        initial_color[0][0],initial_color[0][2],initial_color[0][8],initial_color[0][6]=swap_four_element(initial_color[0][0],initial_color[0][2],initial_color[0][8],initial_color[0][6])
        initial_color[0][1],initial_color[0][5],initial_color[0][7],initial_color[0][3]=swap_four_element(initial_color[0][1],initial_color[0][5],initial_color[0][7],initial_color[0][3])
        initial_color[1][0],initial_color[4][0],initial_color[2][0],initial_color[3][0]=swap_four_element(initial_color[1][0],initial_color[4][0],initial_color[2][0],initial_color[3][0])
        initial_color[1][1],initial_color[4][1],initial_color[2][1],initial_color[3][1]=swap_four_element(initial_color[1][1],initial_color[4][1],initial_color[2][1],initial_color[3][1])
        initial_color[1][2],initial_color[4][2],initial_color[2][2],initial_color[3][2]=swap_four_element(initial_color[1][2],initial_color[4][2],initial_color[2][2],initial_color[3][2])
        return 14
    
    elif(now_color[0]==initial_color[4][6] and now_color[1]==initial_color[4][3] and now_color[2]==initial_color[4][0]#右翻
   and now_color[3]==initial_color[4][7] and now_color[4]==initial_color[4][4] and now_color[5]==initial_color[4][1]
   and now_color[6]==initial_color[4][8] and now_color[7]==initial_color[4][5] and now_color[8]==initial_color[4][2]):
        initial_color[0][0],initial_color[4][6],initial_color[5][8],initial_color[3][2]=swap_four_element(initial_color[0][0],initial_color[4][6],initial_color[5][8],initial_color[3][2])
        initial_color[0][1],initial_color[4][3],initial_color[5][7],initial_color[3][5]=swap_four_element(initial_color[0][1],initial_color[4][3],initial_color[5][7],initial_color[3][5])
        initial_color[0][2],initial_color[4][0],initial_color[5][6],initial_color[3][8]=swap_four_element(initial_color[0][2],initial_color[4][0],initial_color[5][6],initial_color[3][8])
        initial_color[2][0],initial_color[2][2],initial_color[2][8],initial_color[2][6]=swap_four_element(initial_color[2][0],initial_color[2][2],initial_color[2][8],initial_color[2][6])
        initial_color[2][1],initial_color[2][5],initial_color[2][7],initial_color[2][3]=swap_four_element(initial_color[2][1],initial_color[2][5],initial_color[2][7],initial_color[2][3])
        initial_color[0][6],initial_color[4][8],initial_color[5][2],initial_color[3][0]=swap_four_element(initial_color[0][6],initial_color[4][8],initial_color[5][2],initial_color[3][0])
        initial_color[0][7],initial_color[4][5],initial_color[5][1],initial_color[3][3]=swap_four_element(initial_color[0][7],initial_color[4][5],initial_color[5][1],initial_color[3][3])
        initial_color[0][8],initial_color[4][2],initial_color[5][0],initial_color[3][6]=swap_four_element(initial_color[0][8],initial_color[4][2],initial_color[5][0],initial_color[3][6])
        initial_color[1][0],initial_color[1][6],initial_color[1][8],initial_color[1][2]=swap_four_element(initial_color[1][0],initial_color[1][6],initial_color[1][8],initial_color[1][2])
        initial_color[1][1],initial_color[1][3],initial_color[1][7],initial_color[1][5]=swap_four_element(initial_color[1][1],initial_color[1][3],initial_color[1][7],initial_color[1][5])
        initial_color[0][3],initial_color[4][7],initial_color[5][5],initial_color[3][1]=swap_four_element(initial_color[0][3],initial_color[4][7],initial_color[5][5],initial_color[3][1])
        initial_color[0][4],initial_color[4][4],initial_color[5][4],initial_color[3][4]=swap_four_element(initial_color[0][4],initial_color[4][4],initial_color[5][4],initial_color[3][4])
        initial_color[0][5],initial_color[4][1],initial_color[5][3],initial_color[3][7]=swap_four_element(initial_color[0][5],initial_color[4][1],initial_color[5][3],initial_color[3][7])
        return 15
    
    elif(now_color[0]==initial_color[3][2] and now_color[1]==initial_color[3][5] and now_color[2]==initial_color[3][8]#左翻
   and now_color[3]==initial_color[3][1] and now_color[4]==initial_color[3][4] and now_color[5]==initial_color[3][7]
   and now_color[6]==initial_color[3][0] and now_color[7]==initial_color[3][3] and now_color[8]==initial_color[3][6]):
        initial_color[0][0],initial_color[3][2],initial_color[5][8],initial_color[4][6]=swap_four_element(initial_color[0][0],initial_color[3][2],initial_color[5][8],initial_color[4][6])
        initial_color[0][1],initial_color[3][5],initial_color[5][7],initial_color[4][3]=swap_four_element(initial_color[0][1],initial_color[3][5],initial_color[5][7],initial_color[4][3])
        initial_color[0][2],initial_color[3][8],initial_color[5][6],initial_color[4][0]=swap_four_element(initial_color[0][2],initial_color[3][8],initial_color[5][6],initial_color[4][0])
        initial_color[2][0],initial_color[2][6],initial_color[2][8],initial_color[2][2]=swap_four_element(initial_color[2][0],initial_color[2][6],initial_color[2][8],initial_color[2][2])
        initial_color[2][1],initial_color[2][3],initial_color[2][7],initial_color[2][5]=swap_four_element(initial_color[2][1],initial_color[2][3],initial_color[2][7],initial_color[2][5])
        initial_color[0][3],initial_color[3][1],initial_color[5][5],initial_color[4][7]=swap_four_element(initial_color[0][3],initial_color[3][1],initial_color[5][5],initial_color[4][7])
        initial_color[0][4],initial_color[3][4],initial_color[5][4],initial_color[4][4]=swap_four_element(initial_color[0][4],initial_color[3][4],initial_color[5][4],initial_color[4][4])
        initial_color[0][5],initial_color[3][7],initial_color[5][3],initial_color[4][1]=swap_four_element(initial_color[0][5],initial_color[3][7],initial_color[5][3],initial_color[4][1])
        initial_color[0][6],initial_color[3][0],initial_color[5][2],initial_color[4][8]=swap_four_element(initial_color[0][6],initial_color[3][0],initial_color[5][2],initial_color[4][8])
        initial_color[0][7],initial_color[3][3],initial_color[5][1],initial_color[4][5]=swap_four_element(initial_color[0][7],initial_color[3][3],initial_color[5][1],initial_color[4][5])
        initial_color[0][8],initial_color[3][6],initial_color[5][0],initial_color[4][2]=swap_four_element(initial_color[0][8],initial_color[3][6],initial_color[5][0],initial_color[4][2])
        initial_color[1][0],initial_color[1][2],initial_color[1][8],initial_color[1][6]=swap_four_element(initial_color[1][0],initial_color[1][2],initial_color[1][8],initial_color[1][6])
        initial_color[1][1],initial_color[1][5],initial_color[1][7],initial_color[1][3]=swap_four_element(initial_color[1][1],initial_color[1][5],initial_color[1][7],initial_color[1][3])
        return 16
    
    elif(now_color[0]==initial_color[2][8] and now_color[1]==initial_color[2][7] and now_color[2]==initial_color[2][6]#下翻
   and now_color[3]==initial_color[2][5] and now_color[4]==initial_color[2][4] and now_color[5]==initial_color[2][3]
   and now_color[6]==initial_color[2][2] and now_color[7]==initial_color[2][1] and now_color[8]==initial_color[2][0]):
        initial_color[0][2],initial_color[2][6],initial_color[5][2],initial_color[1][2]=swap_four_element(initial_color[0][2],initial_color[2][6],initial_color[5][2],initial_color[1][2])
        initial_color[0][5],initial_color[2][3],initial_color[5][5],initial_color[1][5]=swap_four_element(initial_color[0][5],initial_color[2][3],initial_color[5][5],initial_color[1][5])
        initial_color[0][8],initial_color[2][0],initial_color[5][8],initial_color[1][8]=swap_four_element(initial_color[0][8],initial_color[2][0],initial_color[5][8],initial_color[1][8])
        initial_color[3][0],initial_color[3][2],initial_color[3][8],initial_color[3][6]=swap_four_element(initial_color[3][0],initial_color[3][2],initial_color[3][8],initial_color[3][6])
        initial_color[3][1],initial_color[3][5],initial_color[3][7],initial_color[3][3]=swap_four_element(initial_color[3][1],initial_color[3][5],initial_color[3][7],initial_color[3][3])
        initial_color[0][0],initial_color[2][8],initial_color[5][0],initial_color[1][0]=swap_four_element(initial_color[0][0],initial_color[2][8],initial_color[5][0],initial_color[1][0])
        initial_color[0][3],initial_color[2][5],initial_color[5][3],initial_color[1][3]=swap_four_element(initial_color[0][3],initial_color[2][5],initial_color[5][3],initial_color[1][3])
        initial_color[0][6],initial_color[2][2],initial_color[5][6],initial_color[1][6]=swap_four_element(initial_color[0][6],initial_color[2][2],initial_color[5][6],initial_color[1][6])
        initial_color[4][0],initial_color[4][6],initial_color[4][8],initial_color[4][2]=swap_four_element(initial_color[4][0],initial_color[4][6],initial_color[4][8],initial_color[4][2])
        initial_color[4][1],initial_color[4][3],initial_color[4][7],initial_color[4][5]=swap_four_element(initial_color[4][1],initial_color[4][3],initial_color[4][7],initial_color[4][5])
        initial_color[0][1],initial_color[2][7],initial_color[5][1],initial_color[1][1]=swap_four_element(initial_color[0][1],initial_color[2][7],initial_color[5][1],initial_color[1][1])
        initial_color[0][4],initial_color[2][4],initial_color[5][4],initial_color[1][4]=swap_four_element(initial_color[0][4],initial_color[2][4],initial_color[5][4],initial_color[1][4])
        initial_color[0][7],initial_color[2][1],initial_color[5][7],initial_color[1][7]=swap_four_element(initial_color[0][7],initial_color[2][1],initial_color[5][7],initial_color[1][7])
        return 17
    
    elif(now_color[0]==initial_color[1][0] and now_color[1]==initial_color[1][1] and now_color[2]==initial_color[1][2]#上翻
   and now_color[3]==initial_color[1][3] and now_color[4]==initial_color[1][4] and now_color[5]==initial_color[1][5]
   and now_color[6]==initial_color[1][6] and now_color[7]==initial_color[1][7] and now_color[8]==initial_color[1][8]):
        initial_color[0][2],initial_color[1][2],initial_color[5][2],initial_color[2][6]=swap_four_element(initial_color[0][2],initial_color[1][2],initial_color[5][2],initial_color[2][6])
        initial_color[0][5],initial_color[1][5],initial_color[5][5],initial_color[2][3]=swap_four_element(initial_color[0][5],initial_color[1][5],initial_color[5][5],initial_color[2][3])
        initial_color[0][8],initial_color[1][8],initial_color[5][8],initial_color[2][0]=swap_four_element(initial_color[0][8],initial_color[1][8],initial_color[5][8],initial_color[2][0])
        initial_color[3][0],initial_color[3][6],initial_color[3][8],initial_color[3][2]=swap_four_element(initial_color[3][0],initial_color[3][6],initial_color[3][8],initial_color[3][2])
        initial_color[3][1],initial_color[3][3],initial_color[3][7],initial_color[3][5]=swap_four_element(initial_color[3][1],initial_color[3][3],initial_color[3][7],initial_color[3][5])
        initial_color[0][0],initial_color[1][0],initial_color[5][0],initial_color[2][8]=swap_four_element(initial_color[0][0],initial_color[1][0],initial_color[5][0],initial_color[2][8])
        initial_color[0][3],initial_color[1][3],initial_color[5][3],initial_color[2][5]=swap_four_element(initial_color[0][3],initial_color[1][3],initial_color[5][3],initial_color[2][5])
        initial_color[0][6],initial_color[1][6],initial_color[5][6],initial_color[2][2]=swap_four_element(initial_color[0][6],initial_color[1][6],initial_color[5][6],initial_color[2][2])
        initial_color[4][0],initial_color[4][2],initial_color[4][8],initial_color[4][6]=swap_four_element(initial_color[4][0],initial_color[4][2],initial_color[4][8],initial_color[4][6])
        initial_color[4][1],initial_color[4][5],initial_color[4][7],initial_color[4][3]=swap_four_element(initial_color[4][1],initial_color[4][5],initial_color[4][7],initial_color[4][3])
        initial_color[0][1],initial_color[1][1],initial_color[5][1],initial_color[2][7]=swap_four_element(initial_color[0][1],initial_color[1][1],initial_color[5][1],initial_color[2][7])
        initial_color[0][4],initial_color[1][4],initial_color[5][4],initial_color[2][4]=swap_four_element(initial_color[0][4],initial_color[1][4],initial_color[5][4],initial_color[2][4])
        initial_color[0][7],initial_color[1][7],initial_color[5][7],initial_color[2][1]=swap_four_element(initial_color[0][7],initial_color[1][7],initial_color[5][7],initial_color[2][1])
        return 18
    
    elif(top_color[0]==now_color[2] and top_color[1]==now_color[5] and top_color[2]==now_color[8]#右轉翻
   and top_color[3]==now_color[1] and top_color[4]==now_color[4] and top_color[5]==now_color[7]
   and top_color[6]==now_color[0] and top_color[7]==now_color[3] and top_color[8]==now_color[6] and key==1):
        initial_color[0][0],initial_color[0][6],initial_color[0][8],initial_color[0][2]=swap_four_element(initial_color[0][0],initial_color[0][6],initial_color[0][8],initial_color[0][2])
        initial_color[0][1],initial_color[0][3],initial_color[0][7],initial_color[0][5]=swap_four_element(initial_color[0][1],initial_color[0][3],initial_color[0][7],initial_color[0][5])
        initial_color[1][0],initial_color[3][0],initial_color[2][0],initial_color[4][0]=swap_four_element(initial_color[1][0],initial_color[3][0],initial_color[2][0],initial_color[4][0])
        initial_color[1][1],initial_color[3][1],initial_color[2][1],initial_color[4][1]=swap_four_element(initial_color[1][1],initial_color[3][1],initial_color[2][1],initial_color[4][1])
        initial_color[1][2],initial_color[3][2],initial_color[2][2],initial_color[4][2]=swap_four_element(initial_color[1][2],initial_color[3][2],initial_color[2][2],initial_color[4][2])
        initial_color[1][3],initial_color[3][3],initial_color[2][3],initial_color[4][3]=swap_four_element(initial_color[1][3],initial_color[3][3],initial_color[2][3],initial_color[4][3])
        initial_color[1][4],initial_color[3][4],initial_color[2][4],initial_color[4][4]=swap_four_element(initial_color[1][4],initial_color[3][4],initial_color[2][4],initial_color[4][4])
        initial_color[1][5],initial_color[3][5],initial_color[2][5],initial_color[4][5]=swap_four_element(initial_color[1][5],initial_color[3][5],initial_color[2][5],initial_color[4][5])
        initial_color[1][6],initial_color[3][6],initial_color[2][6],initial_color[4][6]=swap_four_element(initial_color[1][6],initial_color[3][6],initial_color[2][6],initial_color[4][6])
        initial_color[1][7],initial_color[3][7],initial_color[2][7],initial_color[4][7]=swap_four_element(initial_color[1][7],initial_color[3][7],initial_color[2][7],initial_color[4][7])
        initial_color[1][8],initial_color[3][8],initial_color[2][8],initial_color[4][8]=swap_four_element(initial_color[1][8],initial_color[3][8],initial_color[2][8],initial_color[4][8])
        initial_color[5][0],initial_color[5][2],initial_color[5][8],initial_color[5][6]=swap_four_element(initial_color[5][0],initial_color[5][2],initial_color[5][8],initial_color[5][6])
        initial_color[5][1],initial_color[5][5],initial_color[5][7],initial_color[5][3]=swap_four_element(initial_color[5][1],initial_color[5][5],initial_color[5][7],initial_color[5][3])
        return 19
    
    elif(top_color[0]==now_color[6] and top_color[1]==now_color[3] and top_color[2]==now_color[0]#左轉翻
   and top_color[3]==now_color[7] and top_color[4]==now_color[4] and top_color[5]==now_color[1]
   and top_color[6]==now_color[8] and top_color[7]==now_color[5] and top_color[8]==now_color[2] and key==1):
        initial_color[0][0],initial_color[0][2],initial_color[0][8],initial_color[0][6]=swap_four_element(initial_color[0][0],initial_color[0][2],initial_color[0][8],initial_color[0][6])
        initial_color[0][1],initial_color[0][5],initial_color[0][7],initial_color[0][3]=swap_four_element(initial_color[0][1],initial_color[0][5],initial_color[0][7],initial_color[0][3])
        initial_color[1][0],initial_color[4][0],initial_color[2][0],initial_color[3][0]=swap_four_element(initial_color[1][0],initial_color[4][0],initial_color[2][0],initial_color[3][0])
        initial_color[1][1],initial_color[4][1],initial_color[2][1],initial_color[3][1]=swap_four_element(initial_color[1][1],initial_color[4][1],initial_color[2][1],initial_color[3][1])
        initial_color[1][2],initial_color[4][2],initial_color[2][2],initial_color[3][2]=swap_four_element(initial_color[1][2],initial_color[4][2],initial_color[2][2],initial_color[3][2])
        initial_color[1][3],initial_color[4][3],initial_color[2][3],initial_color[3][3]=swap_four_element(initial_color[1][3],initial_color[4][3],initial_color[2][3],initial_color[3][3])
        initial_color[1][4],initial_color[4][4],initial_color[2][4],initial_color[3][4]=swap_four_element(initial_color[1][4],initial_color[4][4],initial_color[2][4],initial_color[3][4])
        initial_color[1][5],initial_color[4][5],initial_color[2][5],initial_color[3][5]=swap_four_element(initial_color[1][5],initial_color[4][5],initial_color[2][5],initial_color[3][5])
        initial_color[1][6],initial_color[4][6],initial_color[2][6],initial_color[3][6]=swap_four_element(initial_color[1][6],initial_color[4][6],initial_color[2][6],initial_color[3][6])
        initial_color[1][7],initial_color[4][7],initial_color[2][7],initial_color[3][7]=swap_four_element(initial_color[1][7],initial_color[4][7],initial_color[2][7],initial_color[3][7])
        initial_color[1][8],initial_color[4][8],initial_color[2][8],initial_color[3][8]=swap_four_element(initial_color[1][8],initial_color[4][8],initial_color[2][8],initial_color[3][8])
        initial_color[5][0],initial_color[5][6],initial_color[5][8],initial_color[5][2]=swap_four_element(initial_color[5][0],initial_color[5][6],initial_color[5][8],initial_color[5][2])
        initial_color[5][1],initial_color[5][3],initial_color[5][7],initial_color[5][5]=swap_four_element(initial_color[5][1],initial_color[5][3],initial_color[5][7],initial_color[5][5])
        return 20
    
    
    return 0

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
        
def read_image():
    ret, image = cap.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    results1 = detector1.detect(gray)
    
    count=0
    
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
    cv2.imshow('camera', image)
    cv2.waitKey(1)
    
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
        
    return image

def read_image_and_detect_change():
    
    image=read_image()   
    change_flag=0
    op=0
    
    for i in range(0,9):
        if(top_color[i]!=now_color[i]):
            change_flag=1
    
    if (change_flag!=0):
        op=check_valid()
            
    if (change_flag!=0 and op):
        for i in range(0,9):
            top_color[i]=now_color[i]
            
        print('display:')
        for j in range(0,3):
            print(print_color(top_color[3*j]),
                  print_color(top_color[3*j+1]),
                  print_color(top_color[3*j+2]),'\n')
            
    cv2.imshow('camera', image)
    cv2.waitKey(1)
    return op

def print_op(op):
    
    if(op==1):
        print('右下')
    elif(op==2):
        print('右上')
    elif(op==3):
        print('左下')
    elif(op==4):
        print('左上')
    elif(op==5):
        print('上右')
    elif(op==6):
        print('上左')
    elif(op==7):
        print('下右')
    elif(op==8):
        print('下左')
    elif(op==9):
        print('中下')
    elif(op==10):
        print('中上')
    elif(op==11):
        print('橫右')
    elif(op==12):
        print('橫左')
    elif(op==13):
        print('右轉')
    elif(op==14):
        print('左轉')
    elif(op==15):
        print('右翻')
    elif(op==16):
        print('左翻')
    elif(op==17):
        print('上翻')
    elif(op==18):
        print('下翻')
    elif(op==19):
        print('右轉翻')
    elif(op==20):
        print('左轉翻')

def check_if_yellow_edge(x):
    if x>=46:
        return 1
    return 0

while (1):
    
    image=read_image()
    
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
    
for i in range(0,9):
    top_color[i]=initial_color[0][i]
    
    
print('display:')
for i in range(0,6):
    print('\n')
    for j in range(0,3):
        print(print_color(initial_color[i][3*j]),
              print_color(initial_color[i][3*j+1]),
              print_color(initial_color[i][3*j+2]),'\n')
        


while(1):

    image=read_image()
    
    
    initial_flag=0
    
    for i in range(0,9):
        if(now_color[i]!=initial_color[0][i]):
            initial_flag=1
            
    if(initial_flag==0):
       print('start!')
       break
   
     
    
    cv2.imshow('camera', image)
    cv2.waitKey(1)
    
while (1):#白藍
    
    operation=[]
    
    if(initial_color[0][7]==8 and initial_color[1][1]==11):
        operation=[19]
    elif(initial_color[1][1]==8 and initial_color[0][7]==11):
        operation=[7,2,13,19]
    elif(initial_color[3][3]==8 and initial_color[1][5]==11):
        operation=[8,19]
    elif(initial_color[1][5]==8 and initial_color[3][3]==11):
        operation=[2,13,19]
    elif(initial_color[4][5]==8 and initial_color[1][3]==11):
        operation=[7,19]
    elif(initial_color[1][3]==8 and initial_color[4][5]==11):
        operation=[4,14,19]
    elif(initial_color[5][1]==8 and initial_color[1][7]==11):
        operation=[7,7,19]
    elif(initial_color[1][7]==8 and initial_color[5][1]==11):
        operation=[7,4,14,19]
    elif(initial_color[0][5]==8 and initial_color[3][1]==11):
        operation=[13,19]
    elif(initial_color[3][1]==8 and initial_color[0][5]==11):
        operation=[1,8,19]
    elif(initial_color[2][3]==8 and initial_color[3][5]==11):
        operation=[19,8,13,20,19]
    elif(initial_color[3][5]==8 and initial_color[2][3]==11):
        operation=[19,2,13,13,20,19]
    elif(initial_color[5][5]==8 and initial_color[3][7]==11):
        operation=[19,7,7,13,20,19]
    elif(initial_color[3][7]==8 and initial_color[5][5]==11):
        operation=[19,7,4,20,19]
    elif(initial_color[0][3]==8 and initial_color[4][1]==11):
        operation=[14,19]
    elif(initial_color[4][1]==8 and initial_color[0][3]==11):
        operation=[3,7,19]
    elif(initial_color[2][5]==8 and initial_color[4][3]==11):
        operation=[20,7,14,19,19]
    elif(initial_color[4][3]==8 and initial_color[2][5]==11):
        operation=[20,4,14,14,19,19]
    elif(initial_color[5][3]==8 and initial_color[4][7]==11):
        operation=[20,7,7,14,19,19]
    elif(initial_color[4][7]==8 and initial_color[5][3]==11):
        operation=[20,8,2,19,19]
    elif(initial_color[0][1]==8 and initial_color[2][1]==11):
        operation=[13,13,19]
    elif(initial_color[2][1]==8 and initial_color[0][1]==11):
        operation=[20,20,7,2,14,19,19,19]
    elif(initial_color[5][7]==8 and initial_color[2][7]==11):
        operation=[20,20,7,7,14,14,19,19,19]
    elif(initial_color[2][7]==8 and initial_color[5][7]==11):
        operation=[20,20,7,4,13,19,19,19]
        
        
    print_op(operation[0])
    
    if(operation[0]==13 or operation[0]==14):
        key=0
    elif(operation[0]==19 or operation[0]==20):
        key=1
    
    
    
    while(len(operation)!=0):
        change_flag=read_image_and_detect_change()
        
        if(change_flag==operation[0] and len(operation)==1):
            operation=[]
            break
        elif(change_flag==operation[0]):
            operation=operation[1:]
            print_op(operation[0])
            if(operation[0]==13 or operation[0]==14):
                key=0
            elif(operation[0]==19 or operation[0]==20):
                key=1
            
            
    break


while (1):#白橘
    
    operation=[]
    
    if(initial_color[0][7]==6 and initial_color[1][1]==29):
        operation=[19]
    elif(initial_color[1][1]==6 and initial_color[0][7]==29):
        operation=[7,14,2,13,19]
    elif(initial_color[3][3]==6 and initial_color[1][5]==29):
        operation=[8,19]
    elif(initial_color[1][5]==6 and initial_color[3][3]==29):
        operation=[14,2,13,19]
    elif(initial_color[4][5]==6 and initial_color[1][3]==29):
        operation=[7,19]
    elif(initial_color[1][3]==6 and initial_color[4][5]==29):
        operation=[13,4,14,19]
    elif(initial_color[5][1]==6 and initial_color[1][7]==29):
        operation=[7,7,19]
    elif(initial_color[1][7]==6 and initial_color[5][1]==29):
        operation=[7,13,4,14,19]
    elif(initial_color[0][5]==6 and initial_color[3][1]==29):
        operation=[1,14,2,13,19]
    elif(initial_color[3][1]==6 and initial_color[0][5]==29):
        operation=[1,8,19]#
    elif(initial_color[2][3]==6 and initial_color[3][5]==29):
        operation=[19,14,8,13,20,19]
    elif(initial_color[3][5]==6 and initial_color[2][3]==29):
        operation=[19,14,14,2,13,13,20,19]#
    elif(initial_color[5][5]==6 and initial_color[3][7]==29):
        operation=[19,14,7,7,13,20,19]
    elif(initial_color[3][7]==6 and initial_color[5][5]==29):
        operation=[19,7,4,20,19]#
    elif(initial_color[2][5]==6 and initial_color[4][3]==29):
        operation=[20,13,7,14,19,19]
    elif(initial_color[4][3]==6 and initial_color[2][5]==29):
        operation=[20,13,13,4,14,14,19,19]
    elif(initial_color[5][3]==6 and initial_color[4][7]==29):
        operation=[20,13,7,7,14,19,19]
    elif(initial_color[4][7]==6 and initial_color[5][3]==29):
        operation=[20,13,8,14,2,19,19]
    elif(initial_color[0][1]==6 and initial_color[2][1]==29):
        operation=[3,13,13,4,19]
    elif(initial_color[2][1]==6 and initial_color[0][1]==29):
        operation=[20,20,7,13,2,14,19,19,19]
    elif(initial_color[5][7]==6 and initial_color[2][7]==29):
        operation=[20,20,14,14,7,7,14,14,19,19,19]
    elif(initial_color[2][7]==6 and initial_color[5][7]==29):
        operation=[20,20,7,14,4,13,19,19,19]
        
        
    print_op(operation[0])
    
    if(operation[0]==13 or operation[0]==14):
        key=0
    elif(operation[0]==19 or operation[0]==20):
        key=1
    
    while(len(operation)!=0):
        change_flag=read_image_and_detect_change()
        
        if(change_flag==operation[0] and len(operation)==1):
            operation=[]
            break
        elif(change_flag==operation[0]):
            operation=operation[1:]
            print_op(operation[0])
            if(operation[0]==13 or operation[0]==14):
                key=0
            elif(operation[0]==19 or operation[0]==20):
                key=1
            
    break
    
while (1):#白綠
    
    operation=[]
    
    if(initial_color[0][7]==2 and initial_color[1][1]==20):
        operation=[19]
    elif(initial_color[1][1]==2 and initial_color[0][7]==20):
        operation=[7,14,2,13,19]
    elif(initial_color[3][3]==2 and initial_color[1][5]==20):
        operation=[8,19]
    elif(initial_color[1][5]==2 and initial_color[3][3]==20):
        operation=[14,2,13,19]
    elif(initial_color[4][5]==2 and initial_color[1][3]==20):
        operation=[7,19]
    elif(initial_color[1][3]==2 and initial_color[4][5]==20):
        operation=[13,4,14,19]
    elif(initial_color[5][1]==2 and initial_color[1][7]==20):
        operation=[7,7,19]
    elif(initial_color[1][7]==2 and initial_color[5][1]==20):
        operation=[7,13,4,14,19]
    elif(initial_color[0][5]==2 and initial_color[3][1]==20):
        operation=[1,14,2,13,19]
    elif(initial_color[3][1]==2 and initial_color[0][5]==20):
        operation=[1,8,19]#
    elif(initial_color[2][3]==2 and initial_color[3][5]==20):
        operation=[19,14,8,13,20,19]
    elif(initial_color[3][5]==2 and initial_color[2][3]==20):
        operation=[19,14,14,2,13,13,20,19]#
    elif(initial_color[5][5]==2 and initial_color[3][7]==20):
        operation=[19,14,7,7,13,20,19]
    elif(initial_color[3][7]==2 and initial_color[5][5]==20):
        operation=[19,7,4,20,19]#
    elif(initial_color[2][5]==2 and initial_color[4][3]==20):
        operation=[20,13,7,14,19,19]
    elif(initial_color[4][3]==2 and initial_color[2][5]==20):
        operation=[20,13,13,4,14,14,19,19]
    elif(initial_color[5][3]==2 and initial_color[4][7]==20):
        operation=[20,13,7,7,14,19,19]
    elif(initial_color[4][7]==2 and initial_color[5][3]==20):
        operation=[20,13,8,14,2,19,19]
    elif(initial_color[5][7]==2 and initial_color[2][7]==20):
        operation=[20,20,14,14,7,7,14,14,19,19,19]
    elif(initial_color[2][7]==2 and initial_color[5][7]==20):
        operation=[20,20,14,7,4,13,19,19,19]
        
        
    print_op(operation[0])
    
    if(operation[0]==13 or operation[0]==14):
        key=0
    elif(operation[0]==19 or operation[0]==20):
        key=1
    
    while(len(operation)!=0):
        change_flag=read_image_and_detect_change()
        
        if(change_flag==operation[0] and len(operation)==1):
            operation=[]
            break
        elif(change_flag==operation[0]):
            operation=operation[1:]
            print_op(operation[0])
            if(operation[0]==13 or operation[0]==14):
                key=0
            elif(operation[0]==19 or operation[0]==20):
                key=1
            
    break
    
while (1):#白紅
    
    operation=[]
    
    if(initial_color[0][7]==4 and initial_color[1][1]==38):
        operation=[19]
    elif(initial_color[1][1]==4 and initial_color[0][7]==38):
        operation=[7,14,2,13,19]
    elif(initial_color[3][3]==4 and initial_color[1][5]==38):
        operation=[8,19]
    elif(initial_color[1][5]==4 and initial_color[3][3]==38):
        operation=[14,2,13,19]
    elif(initial_color[4][5]==4 and initial_color[1][3]==38):
        operation=[7,19]
    elif(initial_color[1][3]==4 and initial_color[4][5]==38):
        operation=[13,4,14,19]
    elif(initial_color[5][1]==4 and initial_color[1][7]==38):
        operation=[7,7,19]
    elif(initial_color[1][7]==4 and initial_color[5][1]==38):
        operation=[7,13,4,14,19]
    elif(initial_color[2][3]==4 and initial_color[3][5]==38):
        operation=[19,14,8,13,20,19]
    elif(initial_color[3][5]==4 and initial_color[2][3]==38):
        operation=[19,14,14,2,13,13,20,19]#
    elif(initial_color[5][5]==4 and initial_color[3][7]==38):
        operation=[19,14,7,7,13,20,19]
    elif(initial_color[3][7]==4 and initial_color[5][5]==38):
        operation=[19,14,7,13,4,20,19]#
    elif(initial_color[2][5]==4 and initial_color[4][3]==38):
        operation=[20,13,7,14,19,19]
    elif(initial_color[4][3]==4 and initial_color[2][5]==38):
        operation=[20,13,13,4,14,14,19,19]
    elif(initial_color[5][3]==4 and initial_color[4][7]==38):
        operation=[20,13,7,7,14,19,19]
    elif(initial_color[4][7]==4 and initial_color[5][3]==38):
        operation=[20,13,8,14,2,19,19]
    elif(initial_color[5][7]==4 and initial_color[2][7]==38):
        operation=[20,20,14,14,7,7,14,14,19,19,19]
    elif(initial_color[2][7]==4 and initial_color[5][7]==38):
        operation=[20,20,14,14,7,13,4,13,19,19,19]
    
        
    print_op(operation[0])
    
    if(operation[0]==13 or operation[0]==14):
        key=0
    elif(operation[0]==19 or operation[0]==20):
        key=1
    
    while(len(operation)!=0):
        change_flag=read_image_and_detect_change()
        
        if(change_flag==operation[0] and len(operation)==1):
            operation=[]
            break
        elif(change_flag==operation[0]):
            operation=operation[1:]
            print_op(operation[0])
            if(operation[0]==13 or operation[0]==14):
                key=0
            elif(operation[0]==19 or operation[0]==20):
                key=1
            
    break

while (1):#白藍橘
    
    operation=[]
    
    if(initial_color[0][8]==9):
        operation=[19]
    elif(initial_color[1][2]==9):
        operation=[2,8,1,7,2,8,1,7,19]
    elif(initial_color[3][0]==9):
        operation=[19,4,7,3,8,4,7,3,8,20,19]
    elif(initial_color[1][8]==9):
        operation=[2,8,1,7,19]
    elif(initial_color[5][2]==9):
        operation=[2,8,1,7,2,8,1,7,2,8,1,7,19]
    elif(initial_color[3][6]==9):
        operation=[19,4,7,3,8,20,19]
        
    elif(initial_color[0][6]==9):
        operation=[4,7,3,8,20,13,2,8,1,7,14,19,19]
    elif(initial_color[1][0]==9):
        operation=[4,7,3,8,13,4,7,3,8,14,19]
    elif(initial_color[4][2]==9):
        operation=[20,2,8,1,7,13,2,8,1,7,14,19,19]#
    elif(initial_color[1][6]==9):
        operation=[13,4,7,3,8,14,19]
    elif(initial_color[5][0]==9):
        operation=[13,4,7,3,8,4,7,3,8,4,7,3,8,14,19]
    elif(initial_color[4][8]==9):
        operation=[20,13,2,8,1,7,14,19,19]#
        
    elif(initial_color[0][0]==9):
        operation=[20,20,2,8,1,7,19,13,13,4,7,3,8,14,14,19,19]
    elif(initial_color[2][2]==9):
        operation=[20,20,2,8,1,7,13,13,2,8,1,7,14,14,19,19,19]
    elif(initial_color[4][0]==9):
        operation=[20,4,7,3,8,13,13,4,7,3,8,14,14,19,19]
    elif(initial_color[2][8]==9):
        operation=[20,20,13,13,2,8,1,7,14,14,19,19,19]
    elif(initial_color[5][6]==9):
        operation=[20,20,13,13,2,8,1,7,2,8,1,7,2,8,1,7,14,14,19,19,19]
    elif(initial_color[4][6]==9):
        operation=[20,13,13,4,7,3,8,14,14,19,19]
        
    elif(initial_color[0][2]==9):
        operation=[19,19,4,7,3,8,20,14,2,8,1,7,13,20,19]
    elif(initial_color[2][0]==9):
        operation=[19,19,4,7,3,8,14,4,7,3,8,13,20,20,19]
    elif(initial_color[3][2]==9):
        operation=[19,2,8,1,7,14,2,8,1,7,13,20,19]
    elif(initial_color[2][6]==9):
        operation=[19,19,14,4,7,3,8,13,20,20,19]
    elif(initial_color[5][8]==9):
        operation=[19,19,14,4,7,3,8,4,7,3,8,4,7,3,8,13,20,20,19]
    elif(initial_color[3][8]==9):
        operation=[19,14,2,8,1,7,13,20,19]
    
        
    print_op(operation[0])
    
    if(operation[0]==13 or operation[0]==14):
        key=0
    elif(operation[0]==19 or operation[0]==20):
        key=1
    
    while(len(operation)!=0):
        change_flag=read_image_and_detect_change()
        
        if(change_flag==operation[0] and len(operation)==1):
            operation=[]
            break
        elif(change_flag==operation[0]):
            operation=operation[1:]
            print_op(operation[0])
            if(operation[0]==13 or operation[0]==14):
                key=0
            elif(operation[0]==19 or operation[0]==20):
                key=1
            
    break

while (1):#白橘綠
    
    operation=[]
    
    if(initial_color[0][8]==3):
        operation=[19]
    elif(initial_color[1][2]==3):
        operation=[2,8,1,7,2,8,1,7,19]
    elif(initial_color[3][0]==3):
        operation=[19,4,7,3,8,4,7,3,8,20,19]
    elif(initial_color[1][8]==3):
        operation=[2,8,1,7,19]
    elif(initial_color[5][2]==3):
        operation=[2,8,1,7,2,8,1,7,2,8,1,7,19]
    elif(initial_color[3][6]==3):
        operation=[19,4,7,3,8,20,19]
        
    elif(initial_color[0][6]==3):
        operation=[4,7,3,8,20,13,2,8,1,7,14,19,19]
    elif(initial_color[1][0]==3):
        operation=[4,7,3,8,13,4,7,3,8,14,19]
    elif(initial_color[4][2]==3):
        operation=[20,2,8,1,7,13,2,8,1,7,14,19,19]#
    elif(initial_color[1][6]==3):
        operation=[13,4,7,3,8,14,19]
    elif(initial_color[5][0]==3):
        operation=[13,4,7,3,8,4,7,3,8,4,7,3,8,14,19]
    elif(initial_color[4][8]==3):
        operation=[20,13,2,8,1,7,14,19,19]#
        
    elif(initial_color[0][0]==3):
        operation=[20,20,2,8,1,7,19,13,13,4,7,3,8,14,14,19,19]
    elif(initial_color[2][2]==3):
        operation=[20,20,2,8,1,7,13,13,2,8,1,7,14,14,19,19,19]
    elif(initial_color[4][0]==3):
        operation=[20,4,7,3,8,13,13,4,7,3,8,14,14,19,19]
    elif(initial_color[2][8]==3):
        operation=[20,20,13,13,2,8,1,7,14,14,19,19,19]
    elif(initial_color[5][6]==3):
        operation=[20,20,13,13,2,8,1,7,2,8,1,7,2,8,1,7,14,14,19,19,19]
    elif(initial_color[4][6]==3):
        operation=[20,13,13,4,7,3,8,14,14,19,19]
        
    elif(initial_color[0][2]==3):
        operation=[19,19,4,7,3,8,20,14,2,8,1,7,13,20,19]
    elif(initial_color[2][0]==3):
        operation=[19,19,4,7,3,8,14,4,7,3,8,13,20,20,19]
    elif(initial_color[3][2]==3):
        operation=[19,2,8,1,7,14,2,8,1,7,13,20,19]
    elif(initial_color[2][6]==3):
        operation=[19,19,14,4,7,3,8,13,20,20,19]
    elif(initial_color[5][8]==3):
        operation=[19,19,14,4,7,3,8,4,7,3,8,4,7,3,8,13,20,20,19]
    elif(initial_color[3][8]==3):
        operation=[19,14,2,8,1,7,13,20,19]
    
        
    print_op(operation[0])
    
    if(operation[0]==13 or operation[0]==14):
        key=0
    elif(operation[0]==19 or operation[0]==20):
        key=1
    
    while(len(operation)!=0):
        change_flag=read_image_and_detect_change()
        
        if(change_flag==operation[0] and len(operation)==1):
            operation=[]
            break
        elif(change_flag==operation[0]):
            operation=operation[1:]
            print_op(operation[0])
            if(operation[0]==13 or operation[0]==14):
                key=0
            elif(operation[0]==19 or operation[0]==20):
                key=1
            
    break

while (1):#白綠紅
    
    operation=[]
    
    if(initial_color[0][8]==1):
        operation=[19]
    elif(initial_color[1][2]==1):
        operation=[2,8,1,7,2,8,1,7,19]
    elif(initial_color[3][0]==1):
        operation=[19,4,7,3,8,4,7,3,8,20,19]
    elif(initial_color[1][8]==1):
        operation=[2,8,1,7,19]
    elif(initial_color[5][2]==1):
        operation=[2,8,1,7,2,8,1,7,2,8,1,7,19]
    elif(initial_color[3][6]==1):
        operation=[19,4,7,3,8,20,19]
        
    elif(initial_color[0][6]==1):
        operation=[4,7,3,8,20,13,2,8,1,7,14,19,19]
    elif(initial_color[1][0]==1):
        operation=[4,7,3,8,13,4,7,3,8,14,19]
    elif(initial_color[4][2]==1):
        operation=[20,2,8,1,7,13,2,8,1,7,14,19,19]#
    elif(initial_color[1][6]==1):
        operation=[13,4,7,3,8,14,19]
    elif(initial_color[5][0]==1):
        operation=[13,4,7,3,8,4,7,3,8,4,7,3,8,14,19]
    elif(initial_color[4][8]==1):
        operation=[20,13,2,8,1,7,14,19,19]#
        
    elif(initial_color[0][0]==1):
        operation=[20,20,2,8,1,7,19,13,13,4,7,3,8,14,14,19,19]
    elif(initial_color[2][2]==1):
        operation=[20,20,2,8,1,7,13,13,2,8,1,7,14,14,19,19,19]
    elif(initial_color[4][0]==1):
        operation=[20,4,7,3,8,13,13,4,7,3,8,14,14,19,19]
    elif(initial_color[2][8]==1):
        operation=[20,20,13,13,2,8,1,7,14,14,19,19,19]
    elif(initial_color[5][6]==1):
        operation=[20,20,13,13,2,8,1,7,2,8,1,7,2,8,1,7,14,14,19,19,19]
    elif(initial_color[4][6]==1):
        operation=[20,13,13,4,7,3,8,14,14,19,19]
        
    elif(initial_color[0][2]==1):
        operation=[19,19,4,7,3,8,20,14,2,8,1,7,13,20,19]
    elif(initial_color[2][0]==1):
        operation=[19,19,4,7,3,8,14,4,7,3,8,13,20,20,19]
    elif(initial_color[3][2]==1):
        operation=[19,2,8,1,7,14,2,8,1,7,13,20,19]
    elif(initial_color[2][6]==1):
        operation=[19,19,14,4,7,3,8,13,20,20,19]
    elif(initial_color[5][8]==1):
        operation=[19,19,14,4,7,3,8,4,7,3,8,4,7,3,8,13,20,20,19]
    elif(initial_color[3][8]==1):
        operation=[19,14,2,8,1,7,13,20,19]
    
        
    print_op(operation[0])
    
    if(operation[0]==13 or operation[0]==14):
        key=0
    elif(operation[0]==19 or operation[0]==20):
        key=1
    
    while(len(operation)!=0):
        change_flag=read_image_and_detect_change()
        
        if(change_flag==operation[0] and len(operation)==1):
            operation=[]
            break
        elif(change_flag==operation[0]):
            operation=operation[1:]
            print_op(operation[0])
            if(operation[0]==13 or operation[0]==14):
                key=0
            elif(operation[0]==19 or operation[0]==20):
                key=1
            
    break

while (1):#白紅藍
    
    operation=[]
    
    if(initial_color[0][8]==7):
        operation=[19]
    elif(initial_color[1][2]==7):
        operation=[2,8,1,7,2,8,1,7,19]
    elif(initial_color[3][0]==7):
        operation=[19,4,7,3,8,4,7,3,8,20,19]
    elif(initial_color[1][8]==7):
        operation=[2,8,1,7,19]
    elif(initial_color[5][2]==7):
        operation=[2,8,1,7,2,8,1,7,2,8,1,7,19]
    elif(initial_color[3][6]==7):
        operation=[19,4,7,3,8,20,19]
        
    elif(initial_color[0][6]==7):
        operation=[4,7,3,8,20,13,2,8,1,7,14,19,19]
    elif(initial_color[1][0]==7):
        operation=[4,7,3,8,13,4,7,3,8,14,19]
    elif(initial_color[4][2]==7):
        operation=[20,2,8,1,7,13,2,8,1,7,14,19,19]#
    elif(initial_color[1][6]==7):
        operation=[13,4,7,3,8,14,19]
    elif(initial_color[5][0]==7):
        operation=[13,4,7,3,8,4,7,3,8,4,7,3,8,14,19]
    elif(initial_color[4][8]==7):
        operation=[20,13,2,8,1,7,14,19,19]#
        
    elif(initial_color[0][0]==7):
        operation=[20,20,2,8,1,7,19,13,13,4,7,3,8,14,14,19,19]
    elif(initial_color[2][2]==7):
        operation=[20,20,2,8,1,7,13,13,2,8,1,7,14,14,19,19,19]
    elif(initial_color[4][0]==7):
        operation=[20,4,7,3,8,13,13,4,7,3,8,14,14,19,19]
    elif(initial_color[2][8]==7):
        operation=[20,20,13,13,2,8,1,7,14,14,19,19,19]
    elif(initial_color[5][6]==7):
        operation=[20,20,13,13,2,8,1,7,2,8,1,7,2,8,1,7,14,14,19,19,19]
    elif(initial_color[4][6]==7):
        operation=[20,13,13,4,7,3,8,14,14,19,19]
    
    elif(initial_color[0][2]==7):
        operation=[19,19,4,7,3,8,20,14,2,8,1,7,13,20,19]
    elif(initial_color[2][0]==7):
        operation=[19,19,4,7,3,8,14,4,7,3,8,13,20,20,19]
    elif(initial_color[3][2]==7):
        operation=[19,2,8,1,7,14,2,8,1,7,13,20,19]
    elif(initial_color[2][6]==7):
        operation=[19,19,14,4,7,3,8,13,20,20,19]
    elif(initial_color[5][8]==7):
        operation=[19,19,14,4,7,3,8,4,7,3,8,4,7,3,8,13,20,20,19]
    elif(initial_color[3][8]==7):
        operation=[19,14,2,8,1,7,13,20,19]
    
        
    print_op(operation[0])
    
    if(operation[0]==13 or operation[0]==14):
        key=0
    elif(operation[0]==19 or operation[0]==20):
        key=1
    
    while(len(operation)!=0):
        change_flag=read_image_and_detect_change()
        
        if(change_flag==operation[0] and len(operation)==1):
            operation=[]
            break
        elif(change_flag==operation[0]):
            operation=operation[1:]
            print_op(operation[0])
            if(operation[0]==13 or operation[0]==14):
                key=0
            elif(operation[0]==19 or operation[0]==20):
                key=1
            
    break

while (1):#翻到底部
    
    operation=[15,15]
    
        
    print_op(operation[0])
    
    if(operation[0]==13 or operation[0]==14):
        key=0
    elif(operation[0]==19 or operation[0]==20):
        key=1
    
    while(len(operation)!=0):
        change_flag=read_image_and_detect_change()
        
        if(change_flag==operation[0] and len(operation)==1):
            operation=[]
            break
        elif(change_flag==operation[0]):
            operation=operation[1:]
            print_op(operation[0])
            if(operation[0]==13 or operation[0]==14):
                key=0
            elif(operation[0]==19 or operation[0]==20):
                key=1
            
    break

while (1):#藍紅
    
    operation=[]
    
    if(initial_color[1][1]==13):
        operation=[13,2,14,1,14,8,13,7,19]
    elif(initial_color[4][1]==13):
        operation=[14,13,2,14,1,14,8,13,7,19]
    elif(initial_color[2][1]==13):
        operation=[14,14,13,2,14,1,14,8,13,7,19]
    elif(initial_color[3][1]==13):
        operation=[13,13,2,14,1,14,8,13,7,19]
        
    elif(initial_color[0][7]==13):
        operation=[19,14,14,4,13,3,13,7,14,8,20,19]
    elif(initial_color[0][5]==13):
        operation=[19,14,4,13,3,13,7,14,8,20,19]
    elif(initial_color[0][1]==13):
        operation=[19,13,14,4,13,3,13,7,14,8,20,19]
    elif(initial_color[0][3]==13):
        operation=[19,13,13,14,4,13,3,13,7,14,8,20,19]
        
    elif(initial_color[1][5]==13):
        operation=[19]
    elif(initial_color[3][5]==13):
        operation=[19,2,14,1,14,8,13,7,13,13,14,4,13,3,13,7,14,8,20,19]
    elif(initial_color[2][5]==13):
        operation=[19,19,2,14,1,14,8,13,7,20,14,14,4,13,3,13,7,14,8,20,19]
    elif(initial_color[4][5]==13):
        operation=[20,2,14,1,14,8,13,7,19,19,14,4,13,3,13,7,14,8,20,19]
        
    elif(initial_color[3][3]==13):
        operation=[2,14,1,14,8,13,7,13,13,13,2,14,1,14,8,13,7,19]
    elif(initial_color[2][3]==13):
        operation=[19,2,14,1,14,8,13,7,20,14,13,2,14,1,14,8,13,7,19]
    elif(initial_color[4][3]==13):
        operation=[19,19,2,14,1,14,8,13,7,20,20,13,2,14,1,14,8,13,7,19]
    elif(initial_color[1][3]==13):
        operation=[20,2,14,1,14,8,13,7,19,13,13,2,14,1,14,8,13,7,19]
    
    
        
    print_op(operation[0])
    
    if(operation[0]==13 or operation[0]==14):
        key=0
    elif(operation[0]==19 or operation[0]==20):
        key=1
    
    while(len(operation)!=0):
        change_flag=read_image_and_detect_change()
        
        if(change_flag==operation[0] and len(operation)==1):
            operation=[]
            break
        elif(change_flag==operation[0]):
            operation=operation[1:]
            print_op(operation[0])
            if(operation[0]==13 or operation[0]==14):
                key=0
            elif(operation[0]==19 or operation[0]==20):
                key=1
            
    break

while (1):#紅綠
    
    operation=[]
    
    if(initial_color[1][1]==40):
        operation=[13,2,14,1,14,8,13,7,19]
    elif(initial_color[4][1]==40):
        operation=[14,13,2,14,1,14,8,13,7,19]
    elif(initial_color[2][1]==40):
        operation=[14,14,13,2,14,1,14,8,13,7,19]
    elif(initial_color[3][1]==40):
        operation=[13,13,2,14,1,14,8,13,7,19]
        
    elif(initial_color[0][7]==40):
        operation=[19,14,14,4,13,3,13,7,14,8,20,19]
    elif(initial_color[0][5]==40):
        operation=[19,14,4,13,3,13,7,14,8,20,19]
    elif(initial_color[0][1]==40):
        operation=[19,13,14,4,13,3,13,7,14,8,20,19]
    elif(initial_color[0][3]==40):
        operation=[19,13,13,14,4,13,3,13,7,14,8,20,19]
        
    elif(initial_color[1][5]==40):
        operation=[19]
    elif(initial_color[3][5]==40):
        operation=[19,2,14,1,14,8,13,7,13,13,14,4,13,3,13,7,14,8,20,19]
    elif(initial_color[2][5]==40):
        operation=[19,19,2,14,1,14,8,13,7,20,14,14,4,13,3,13,7,14,8,20,19]
    elif(initial_color[4][5]==40):
        operation=[20,2,14,1,14,8,13,7,19,19,14,4,13,3,13,7,14,8,20,19]
        
    elif(initial_color[3][3]==40):
        operation=[2,14,1,14,8,13,7,13,13,13,2,14,1,14,8,13,7,19]
    elif(initial_color[2][3]==40):
        operation=[19,2,14,1,14,8,13,7,20,14,13,2,14,1,14,8,13,7,19]
    elif(initial_color[4][3]==40):
        operation=[19,19,2,14,1,14,8,13,7,20,20,13,2,14,1,14,8,13,7,19]
    elif(initial_color[1][3]==40):
        operation=[20,2,14,1,14,8,13,7,19,13,13,2,14,1,14,8,13,7,19]
    
    
        
    print_op(operation[0])
    
    if(operation[0]==13 or operation[0]==14):
        key=0
    elif(operation[0]==19 or operation[0]==20):
        key=1
    
    while(len(operation)!=0):
        change_flag=read_image_and_detect_change()
        
        if(change_flag==operation[0] and len(operation)==1):
            operation=[]
            break
        elif(change_flag==operation[0]):
            operation=operation[1:]
            print_op(operation[0])
            if(operation[0]==13 or operation[0]==14):
                key=0
            elif(operation[0]==19 or operation[0]==20):
                key=1
            
    break

while (1):#綠橘
    
    operation=[]
    
    if(initial_color[1][1]==22):
        operation=[13,2,14,1,14,8,13,7,19]
    elif(initial_color[4][1]==22):
        operation=[14,13,2,14,1,14,8,13,7,19]
    elif(initial_color[2][1]==22):
        operation=[14,14,13,2,14,1,14,8,13,7,19]
    elif(initial_color[3][1]==22):
        operation=[13,13,2,14,1,14,8,13,7,19]
        
    elif(initial_color[0][7]==22):
        operation=[19,14,14,4,13,3,13,7,14,8,20,19]
    elif(initial_color[0][5]==22):
        operation=[19,14,4,13,3,13,7,14,8,20,19]
    elif(initial_color[0][1]==22):
        operation=[19,13,14,4,13,3,13,7,14,8,20,19]
    elif(initial_color[0][3]==22):
        operation=[19,13,13,14,4,13,3,13,7,14,8,20,19]
        
    elif(initial_color[1][5]==22):
        operation=[19]
    elif(initial_color[3][5]==22):
        operation=[19,2,14,1,14,8,13,7,13,13,14,4,13,3,13,7,14,8,20,19]
    elif(initial_color[2][5]==22):
        operation=[19,19,2,14,1,14,8,13,7,20,14,14,4,13,3,13,7,14,8,20,19]
    elif(initial_color[4][5]==22):
        operation=[20,2,14,1,14,8,13,7,19,19,14,4,13,3,13,7,14,8,20,19]
        
    elif(initial_color[3][3]==22):
        operation=[2,14,1,14,8,13,7,13,13,13,2,14,1,14,8,13,7,19]
    elif(initial_color[2][3]==22):
        operation=[19,2,14,1,14,8,13,7,20,14,13,2,14,1,14,8,13,7,19]
    elif(initial_color[4][3]==22):
        operation=[19,19,2,14,1,14,8,13,7,20,20,13,2,14,1,14,8,13,7,19]
    elif(initial_color[1][3]==22):
        operation=[20,2,14,1,14,8,13,7,19,13,13,2,14,1,14,8,13,7,19]
    
    
        
    print_op(operation[0])
    
    if(operation[0]==13 or operation[0]==14):
        key=0
    elif(operation[0]==19 or operation[0]==20):
        key=1
    
    while(len(operation)!=0):
        change_flag=read_image_and_detect_change()
        
        if(change_flag==operation[0] and len(operation)==1):
            operation=[]
            break
        elif(change_flag==operation[0]):
            operation=operation[1:]
            print_op(operation[0])
            if(operation[0]==13 or operation[0]==14):
                key=0
            elif(operation[0]==19 or operation[0]==20):
                key=1
            
    break

while (1):#橘藍
    
    operation=[]
    
    if(initial_color[1][1]==31):
        operation=[13,2,14,1,14,8,13,7,19]
    elif(initial_color[4][1]==31):
        operation=[14,13,2,14,1,14,8,13,7,19]
    elif(initial_color[2][1]==31):
        operation=[14,14,13,2,14,1,14,8,13,7,19]
    elif(initial_color[3][1]==31):
        operation=[13,13,2,14,1,14,8,13,7,19]
        
    elif(initial_color[0][7]==31):
        operation=[19,14,14,4,13,3,13,7,14,8,20,19]
    elif(initial_color[0][5]==31):
        operation=[19,14,4,13,3,13,7,14,8,20,19]
    elif(initial_color[0][1]==31):
        operation=[19,13,14,4,13,3,13,7,14,8,20,19]
    elif(initial_color[0][3]==31):
        operation=[19,13,13,14,4,13,3,13,7,14,8,20,19]
        
    elif(initial_color[1][5]==31):
        operation=[19]
    elif(initial_color[3][5]==31):
        operation=[19,2,14,1,14,8,13,7,13,13,14,4,13,3,13,7,14,8,20,19]
    elif(initial_color[2][5]==31):
        operation=[19,19,2,14,1,14,8,13,7,20,14,14,4,13,3,13,7,14,8,20,19]
    elif(initial_color[4][5]==31):
        operation=[20,2,14,1,14,8,13,7,19,19,14,4,13,3,13,7,14,8,20,19]
        
    elif(initial_color[3][3]==31):
        operation=[2,14,1,14,8,13,7,13,13,13,2,14,1,14,8,13,7,19]
    elif(initial_color[2][3]==31):
        operation=[19,2,14,1,14,8,13,7,20,14,13,2,14,1,14,8,13,7,19]
    elif(initial_color[4][3]==31):
        operation=[19,19,2,14,1,14,8,13,7,20,20,13,2,14,1,14,8,13,7,19]
    elif(initial_color[1][3]==31):
        operation=[20,2,14,1,14,8,13,7,19,13,13,2,14,1,14,8,13,7,19]
    
    
        
    print_op(operation[0])
    
    if(operation[0]==13 or operation[0]==14):
        key=0
    elif(operation[0]==19 or operation[0]==20):
        key=1
    
    while(len(operation)!=0):
        change_flag=read_image_and_detect_change()
        
        if(change_flag==operation[0] and len(operation)==1):
            operation=[]
            break
        elif(change_flag==operation[0]):
            operation=operation[1:]
            print_op(operation[0])
            if(operation[0]==13 or operation[0]==14):
                key=0
            elif(operation[0]==19 or operation[0]==20):
                key=1
            
    break

while (1):#頂面邊塊都不是橘色
    
    operation=[]
    
    check_yellow_flag=0
    
    if(check_if_yellow_edge(initial_color[0][1])==0 and check_if_yellow_edge(initial_color[0][3])==0
      and check_if_yellow_edge(initial_color[0][5])==0 and check_if_yellow_edge(initial_color[0][7])==0):
        check_yellow_flag=1
    
    if check_yellow_flag==0:
        break
    
    operation=[1,14,8,13,7,2]
    
    
        
    print_op(operation[0])
    
    if(operation[0]==13 or operation[0]==14):
        key=0
    elif(operation[0]==19 or operation[0]==20):
        key=1
    
    while(len(operation)!=0):
        change_flag=read_image_and_detect_change()
        
        if(change_flag==operation[0] and len(operation)==1):
            operation=[]
            break
        elif(change_flag==operation[0]):
            operation=operation[1:]
            print_op(operation[0])
            if(operation[0]==13 or operation[0]==14):
                key=0
            elif(operation[0]==19 or operation[0]==20):
                key=1
            
    break

while (1):#頂面邊塊兩個黃色
    
    operation=[]
    
    check_yellow_flag=0
    
    if(check_if_yellow_edge(initial_color[0][1])==1 and check_if_yellow_edge(initial_color[0][3])==0
      and check_if_yellow_edge(initial_color[0][5])==0 and check_if_yellow_edge(initial_color[0][7])==1):#直線
        check_yellow_flag=1
        operation=[1,14,8,13,7,2]
    elif(check_if_yellow_edge(initial_color[0][1])==0 and check_if_yellow_edge(initial_color[0][3])==1
      and check_if_yellow_edge(initial_color[0][5])==1 and check_if_yellow_edge(initial_color[0][7])==0):#橫線
        check_yellow_flag=1
        operation=[13]
    elif(check_if_yellow_edge(initial_color[0][1])==1 and check_if_yellow_edge(initial_color[0][3])==0
      and check_if_yellow_edge(initial_color[0][5])==1 and check_if_yellow_edge(initial_color[0][7])==0):#上右
        check_yellow_flag=1
        operation=[14]
    elif(check_if_yellow_edge(initial_color[0][1])==1 and check_if_yellow_edge(initial_color[0][3])==1
      and check_if_yellow_edge(initial_color[0][5])==0 and check_if_yellow_edge(initial_color[0][7])==0):#上左
        check_yellow_flag=1
        operation=[1,14,8,13,7,2]
    elif(check_if_yellow_edge(initial_color[0][1])==0 and check_if_yellow_edge(initial_color[0][3])==0
      and check_if_yellow_edge(initial_color[0][5])==1 and check_if_yellow_edge(initial_color[0][7])==1):#下右
        check_yellow_flag=1
        operation=[13,13]
    elif(check_if_yellow_edge(initial_color[0][1])==0 and check_if_yellow_edge(initial_color[0][3])==1
      and check_if_yellow_edge(initial_color[0][5])==0 and check_if_yellow_edge(initial_color[0][7])==1):#下左
        check_yellow_flag=1
        operation=[13]
    
    if check_yellow_flag==0:
        break
        
    print_op(operation[0])
    
    if(operation[0]==13 or operation[0]==14):
        key=0
    elif(operation[0]==19 or operation[0]==20):
        key=1
    
    while(len(operation)!=0):
        change_flag=read_image_and_detect_change()
        
        if(change_flag==operation[0] and len(operation)==1):
            operation=[]
            break
        elif(change_flag==operation[0]):
            operation=operation[1:]
            print_op(operation[0])
            if(operation[0]==13 or operation[0]==14):
                key=0
            elif(operation[0]==19 or operation[0]==20):
                key=1
                
while (1):#頂面邊塊都是黃色
    
    operation=[]
    
    check_yellow_flag=0
    
    if(check_if_yellow_edge(initial_color[1][0])==1 and check_if_yellow_edge(initial_color[1][2])==1
      and check_if_yellow_edge(initial_color[2][0])==1 and check_if_yellow_edge(initial_color[2][2])==1):#十字
        check_yellow_flag=1
        operation=[13]
    elif(check_if_yellow_edge(initial_color[3][0])==1 and check_if_yellow_edge(initial_color[3][2])==1
      and check_if_yellow_edge(initial_color[4][0])==1 and check_if_yellow_edge(initial_color[4][2])==1):#十字
        check_yellow_flag=1
        operation=[2,14,4,13,1,14,3]
    elif(check_if_yellow_edge(initial_color[1][0])==1 and check_if_yellow_edge(initial_color[1][2])==1
      and check_if_yellow_edge(initial_color[3][2])==1 and check_if_yellow_edge(initial_color[4][0])==1):#十字
        check_yellow_flag=1
        operation=[13]
    elif(check_if_yellow_edge(initial_color[1][2])==1 and check_if_yellow_edge(initial_color[2][0])==1
      and check_if_yellow_edge(initial_color[4][0])==1 and check_if_yellow_edge(initial_color[4][2])==1):#十字
        check_yellow_flag=1
        operation=[2,14,4,13,1,14,3]
    elif(check_if_yellow_edge(initial_color[3][0])==1 and check_if_yellow_edge(initial_color[3][2])==1
      and check_if_yellow_edge(initial_color[1][0])==1 and check_if_yellow_edge(initial_color[2][2])==1):#十字
        check_yellow_flag=1
        operation=[14,14]
    elif(check_if_yellow_edge(initial_color[2][0])==1 and check_if_yellow_edge(initial_color[2][2])==1
      and check_if_yellow_edge(initial_color[3][0])==1 and check_if_yellow_edge(initial_color[4][2])==1):#十字
        check_yellow_flag=1
        operation=[14]
        
    elif(check_if_yellow_edge(initial_color[0][0])==1 and check_if_yellow_edge(initial_color[0][8])==1
      and check_if_yellow_edge(initial_color[1][0])==1 and check_if_yellow_edge(initial_color[3][2])==1):#對角
        check_yellow_flag=1
        operation=[2,14,4,13,1,14,3]
    elif(check_if_yellow_edge(initial_color[0][2])==1 and check_if_yellow_edge(initial_color[0][6])==1
      and check_if_yellow_edge(initial_color[1][2])==1 and check_if_yellow_edge(initial_color[4][0])==1):#對角
        check_yellow_flag=1
        operation=[14]
    elif(check_if_yellow_edge(initial_color[0][0])==1 and check_if_yellow_edge(initial_color[0][8])==1
      and check_if_yellow_edge(initial_color[2][0])==1 and check_if_yellow_edge(initial_color[4][2])==1):#對角
        check_yellow_flag=1
        operation=[14,14]
    elif(check_if_yellow_edge(initial_color[0][2])==1 and check_if_yellow_edge(initial_color[0][6])==1
      and check_if_yellow_edge(initial_color[2][2])==1 and check_if_yellow_edge(initial_color[3][0])==1):#對角
        check_yellow_flag=1
        operation=[13]
        
    elif(check_if_yellow_edge(initial_color[0][0])==1 and check_if_yellow_edge(initial_color[0][2])==1
      and check_if_yellow_edge(initial_color[1][0])==1 and check_if_yellow_edge(initial_color[1][2])==1):#凸型1
        check_yellow_flag=1
        operation=[2,14,4,13,1,14,3]
    elif(check_if_yellow_edge(initial_color[0][2])==1 and check_if_yellow_edge(initial_color[0][8])==1
      and check_if_yellow_edge(initial_color[4][0])==1 and check_if_yellow_edge(initial_color[4][2])==1):#凸型1
        check_yellow_flag=1
        operation=[14]
    elif(check_if_yellow_edge(initial_color[0][6])==1 and check_if_yellow_edge(initial_color[0][8])==1
      and check_if_yellow_edge(initial_color[2][0])==1 and check_if_yellow_edge(initial_color[2][2])==1):#凸型1
        check_yellow_flag=1
        operation=[14,14]
    elif(check_if_yellow_edge(initial_color[0][0])==1 and check_if_yellow_edge(initial_color[0][6])==1
      and check_if_yellow_edge(initial_color[3][0])==1 and check_if_yellow_edge(initial_color[3][2])==1):#凸型1
        check_yellow_flag=1
        operation=[13]
        
    elif(check_if_yellow_edge(initial_color[0][0])==1 and check_if_yellow_edge(initial_color[0][2])==1
      and check_if_yellow_edge(initial_color[3][0])==1 and check_if_yellow_edge(initial_color[4][2])==1):#凸型2
        check_yellow_flag=1
        operation=[13]
    elif(check_if_yellow_edge(initial_color[0][2])==1 and check_if_yellow_edge(initial_color[0][8])==1
      and check_if_yellow_edge(initial_color[1][0])==1 and check_if_yellow_edge(initial_color[2][2])==1):#凸型2
        check_yellow_flag=1
        operation=[2,14,4,13,1,14,3]
    elif(check_if_yellow_edge(initial_color[0][6])==1 and check_if_yellow_edge(initial_color[0][8])==1
      and check_if_yellow_edge(initial_color[3][2])==1 and check_if_yellow_edge(initial_color[4][0])==1):#凸型2
        check_yellow_flag=1
        operation=[14]
    elif(check_if_yellow_edge(initial_color[0][0])==1 and check_if_yellow_edge(initial_color[0][6])==1
      and check_if_yellow_edge(initial_color[1][2])==1 and check_if_yellow_edge(initial_color[2][0])==1):#凸型2
        check_yellow_flag=1
        operation=[13,13]
        
    elif(check_if_yellow_edge(initial_color[0][6])==1 and check_if_yellow_edge(initial_color[2][0])==1
      and check_if_yellow_edge(initial_color[3][0])==1 and check_if_yellow_edge(initial_color[4][0])==1):#右魚1
        check_yellow_flag=1
        operation=[2,14,4,13,1,14,3]
    elif(check_if_yellow_edge(initial_color[0][8])==1 and check_if_yellow_edge(initial_color[1][0])==1
      and check_if_yellow_edge(initial_color[2][0])==1 and check_if_yellow_edge(initial_color[4][0])==1):#右魚1
        check_yellow_flag=1
        operation=[13]
    elif(check_if_yellow_edge(initial_color[0][2])==1 and check_if_yellow_edge(initial_color[1][0])==1
      and check_if_yellow_edge(initial_color[3][0])==1 and check_if_yellow_edge(initial_color[4][0])==1):#右魚1
        check_yellow_flag=1
        operation=[14,14]
    elif(check_if_yellow_edge(initial_color[0][0])==1 and check_if_yellow_edge(initial_color[1][0])==1
      and check_if_yellow_edge(initial_color[2][0])==1 and check_if_yellow_edge(initial_color[3][0])==1):#右魚1
        check_yellow_flag=1
        operation=[14]
        
    elif(check_if_yellow_edge(initial_color[0][6])==1 and check_if_yellow_edge(initial_color[1][2])==1
      and check_if_yellow_edge(initial_color[2][2])==1 and check_if_yellow_edge(initial_color[3][2])==1):#右魚
        check_yellow_flag=1
        operation=[2,14,4,13,1,14,3]
    elif(check_if_yellow_edge(initial_color[0][8])==1 and check_if_yellow_edge(initial_color[2][2])==1
      and check_if_yellow_edge(initial_color[3][2])==1 and check_if_yellow_edge(initial_color[4][2])==1):#右魚
        check_yellow_flag=1
        operation=[13]
    elif(check_if_yellow_edge(initial_color[0][2])==1 and check_if_yellow_edge(initial_color[1][2])==1
      and check_if_yellow_edge(initial_color[2][2])==1 and check_if_yellow_edge(initial_color[4][2])==1):#右魚
        check_yellow_flag=1
        operation=[14,14]
    elif(check_if_yellow_edge(initial_color[0][0])==1 and check_if_yellow_edge(initial_color[1][2])==1
      and check_if_yellow_edge(initial_color[3][2])==1 and check_if_yellow_edge(initial_color[4][2])==1):#右魚
        check_yellow_flag=1
        operation=[14]

    
    if check_yellow_flag==0:
        break
        
    print_op(operation[0])
    
    if(operation[0]==13 or operation[0]==14):
        key=0
    elif(operation[0]==19 or operation[0]==20):
        key=1
    
    while(len(operation)!=0):
        change_flag=read_image_and_detect_change()
        
        if(change_flag==operation[0] and len(operation)==1):
            operation=[]
            break
        elif(change_flag==operation[0]):
            operation=operation[1:]
            print_op(operation[0])
            if(operation[0]==13 or operation[0]==14):
                key=0
            elif(operation[0]==19 or operation[0]==20):
                key=1
                
print('display:')
for i in range(0,6):
    print('\n')
    for j in range(0,3):
        print(print_color(initial_color[i][3*j]),
              print_color(initial_color[i][3*j+1]),
              print_color(initial_color[i][3*j+2]),'\n')
