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
