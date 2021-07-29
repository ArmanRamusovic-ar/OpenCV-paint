import cv2
import numpy as np




circle_center = []

rectangle_coordinates=[] #rectangle

brush= None

brush_click =[]

smart_line_coordinates=[]

normal_line_coordinates=[]


color = ['Red','Green','Blue']



def nothing(x):
    pass


def ShapesAndObjects(event,x,y,flags,params):
    
    global brush

    if  event == cv2.EVENT_MBUTTONDOWN    and   (flags & cv2.EVENT_FLAG_ALTKEY ) :
        normal_line_coordinates.append((x,y))
    
    
    elif event == cv2.EVENT_MBUTTONDOWN  and (flags & cv2.EVENT_FLAG_CTRLKEY):
        circle_center.append((x,y))

    elif event == cv2.EVENT_MBUTTONDOWN and (flags & cv2.EVENT_FLAG_SHIFTKEY):
        rectangle_coordinates.append((x,y))

    if event == cv2.EVENT_LBUTTONDOWN:
        brush = True
        
        brush_click.append(len(brush_click)+int(1))

        if len(brush_click) > 1 and len(brush_click) < 3:
          smart_line_coordinates.append((x,y))

    elif event ==cv2.EVENT_MOUSEMOVE:

        if brush:
            thickness = cv2.getTrackbarPos('Thickness: ', 'Brush')
            
            free_line_red,free_line_green,free_line_blue = RGB('Brush') 

            cv2.circle(blank_img,(x,y),thickness,(free_line_blue,free_line_green,free_line_red),-1)

    elif event == cv2.EVENT_LBUTTONUP:
        brush= False
        thickness = cv2.getTrackbarPos('Thickness: ', 'Brush')
        free_line_red,free_line_green,free_line_blue = RGB('Brush')

        if len(brush_click) > 1:
            cv2.circle(blank_img,(x,y),thickness,(free_line_blue,free_line_green,free_line_red),-1)
            smart_line_coordinates.append((x,y))


def RGB(winname):
  for i in range(3):
     cv2.createTrackbar(color[i],winname,0,255,nothing)

  red = cv2.getTrackbarPos(color[0],winname)
  green = cv2.getTrackbarPos(color[1],winname)
  blue =  cv2.getTrackbarPos(color[2],winname)
  return red,green,blue


def DoneDelete(winname):

    cv2.createTrackbar('Done: ',winname,0,1,nothing)
    cv2.createTrackbar('Delete: ',winname,0,1,nothing)
    
    return bool(cv2.getTrackbarPos('Done: ',winname)),  bool(cv2.getTrackbarPos('Delete: ',winname))
        
def Thickness(winname):
    cv2.createTrackbar('Thickness: ', winname,0,100,nothing)

    thickness = cv2.getTrackbarPos('Thickness: ', winname)

    if thickness==0:
        thickness=-1
        return thickness
    else:
        return thickness




print('1. Blank image')

choice = 1



if choice ==1:

    height =int(input("Input height: "))
    width =int (input("Input width: "))

    

    blank_img = np.zeros((height,width,3),np.uint8)
    color_img = np.zeros((height,width,3),np.uint8)


    
    image_name=input('Enter the image name: ')
 
       
     
    cv2.namedWindow(image_name)
        
    


    for i in range(3):
     cv2.createTrackbar(color[i],image_name,0,255,nothing)
     
    cv2.createTrackbar('Preview',image_name,0,1,nothing)
    cv2.createTrackbar('Save', image_name,0,1,nothing)
    

    while True:
        preview = None
        save = None


        background_red,background_green,background_blue = RGB(image_name)    
       
        
        color_img[:] = [background_blue,background_green,background_red]
        

        background_img = cv2.bitwise_xor(color_img,blank_img)

        cv2.imshow(image_name,background_img)


        cv2.setMouseCallback(image_name,ShapesAndObjects)
        

        if  cv2.getTrackbarPos('Preview',image_name) == 1:
            preview = True
        else: 
            preview = False
    
        if cv2.getTrackbarPos('Save',image_name) ==1:
            save = True
        else:
            save = False

        if preview:
            cv2.imshow('Preview', background_img)
        else:
            cv2.destroyWindow('Preview')



        if len(circle_center) == 1:

            circle=np.zeros((height,width,3),np.uint8)

            
            cv2.namedWindow('Circle')
  
            circle_red,circle_green, circle_blue = RGB('Circle')  


            cv2.createTrackbar('Radius: ', 'Circle', 0 , 255, nothing)


            circle_thickness=Thickness('Circle')

            radius = cv2.getTrackbarPos('Radius: ','Circle')
        
            done, delete = DoneDelete('Circle')


            cv2.circle(circle,circle_center[0],radius,(circle_blue,circle_green,circle_red),circle_thickness)


            if done:

                cv2.circle(blank_img,circle_center[0],radius,(circle_blue,circle_green,circle_red),circle_thickness)

                circle_center.clear()
                cv2.setTrackbarPos('Done: ','Circle',0)
                cv2.destroyWindow('Circle')
    

            elif delete and done==False:
                circle_center.clear()
                cv2.destroyWindow('Circle')


            cv2.imshow(image_name,cv2.bitwise_xor(background_img,circle))


        elif len(rectangle_coordinates) ==2:

            rectangle=np.zeros((height,width,3),np.uint8)

            cv2.namedWindow('Rectangle')

            rectangle_red, rectangle_green, rectangle_blue =RGB('Rectangle')

           
            rectangle_thickness=Thickness('Rectangle')
    
            done,delete=DoneDelete('Rectangle')



            cv2.rectangle(rectangle,rectangle_coordinates[-1],rectangle_coordinates[-2],(rectangle_blue,rectangle_green,rectangle_red),rectangle_thickness)

  
            if done: 
                cv2.rectangle(blank_img,rectangle_coordinates[-1],rectangle_coordinates[-2],(rectangle_blue,rectangle_green,rectangle_red),rectangle_thickness)
                cv2.setTrackbarPos('Done: ','Rectangle',0)
                rectangle_coordinates.clear()
                cv2.destroyWindow('Rectangle')  
    

            elif delete and done==False:
                rectangle_coordinates.clear()
                cv2.destroyWindow('Rectangle')


            cv2.imshow(image_name,cv2.bitwise_xor(background_img,rectangle))

       
        
        if len(brush_click)>0:
            show_smart_line = None

            cv2.namedWindow('Brush')

            for i in range(3):
                cv2.createTrackbar(color[i],'Brush',0,255,nothing)


            cv2.createTrackbar('Thickness: ','Brush',0,180,nothing )



            cv2.createTrackbar('Smart line','Brush',0,1,nothing)
            cv2.createTrackbar('Done: ','Brush',0,1,nothing)
    

            if cv2.getTrackbarPos('Smart line','Brush') == 1:
                show_smart_line=True
            else:
                show_smart_line=False


            if show_smart_line:
                
                smart_line_img = np.zeros((height,width,3),np.uint8)

                
                cv2.cvtColor(smart_line_img,cv2.COLOR_BGR2RGB)

                for i in range(3):
                    cv2.createTrackbar('Smart line ' + color[i],'Brush',0,255,nothing)


                cv2.createTrackbar('Smartline thickness: ','Brush',0,100,nothing)


                smart_line_thickness = cv2.getTrackbarPos('Smartline thickness: ','Brush')
                smart_line_thickness = 2 if smart_line_thickness==0 else smart_line_thickness


                smart_line_red= cv2.getTrackbarPos('Smart line ' + color[0],'Brush')
                smart_line_green = cv2.getTrackbarPos('Smart line ' + color[1],'Brush')
                smart_line_blue = cv2.getTrackbarPos('Smart line ' + color[2],'Brush')




                cv2.line(smart_line_img,smart_line_coordinates[-2],smart_line_coordinates[-1],(smart_line_blue,smart_line_green,smart_line_red,0),smart_line_thickness)

                cv2.imshow(image_name,cv2.bitwise_xor(smart_line_img,background_img))

            else:
                cv2.imshow(image_name,background_img)


            if cv2.getTrackbarPos('Done: ','Brush') == 1 and  show_smart_line==False:


                cv2.setTrackbarPos('Done: ','Brush',0)
                cv2.setTrackbarPos('Smart line','Brush',0)
                cv2.destroyWindow('Brush')
                brush_click.clear()

            elif cv2.getTrackbarPos('Done: ','Brush') == 1 and  show_smart_line==True:

                cv2.line(blank_img,smart_line_coordinates[-2],smart_line_coordinates[-1],(smart_line_blue,smart_line_green,smart_line_red),smart_line_thickness)

                cv2.imshow(image_name,background_img)


                cv2.setTrackbarPos('Done: ','Brush',0)
                cv2.setTrackbarPos('Smart line','Brush',0)
                cv2.destroyWindow('Brush')
                brush_click.clear()   

        if len(normal_line_coordinates) >=2:
          
            cv2.namedWindow('Line')
            normal_line_img=np.zeros((height,width,3),np.uint8)


            normal_line_red,normal_line_green,normal_line_blue =RGB('Line')
            
            cv2.createTrackbar('Thickness: ','Line',0,100,nothing)

            normal_line_thickness = cv2.getTrackbarPos('Thickness: ','Line')
            
            normal_line_thickness=1 if normal_line_thickness==0 else normal_line_thickness

            
            done,delete=DoneDelete('Line')

            cv2.line(normal_line_img,normal_line_coordinates[-2],normal_line_coordinates[-1],(normal_line_blue,normal_line_green,normal_line_red),normal_line_thickness)


            if done: 
                cv2.line(blank_img,normal_line_coordinates[-2],normal_line_coordinates[-1],(normal_line_blue,normal_line_green,normal_line_red),normal_line_thickness)
                cv2.setTrackbarPos('Done: ','Line',0)
                normal_line_coordinates.clear()
                cv2.destroyWindow('Line')
            
            elif delete and done==False:
                normal_line_coordinates.clear()
                cv2.destroyWindow('Line')

            cv2.imshow(image_name,cv2.bitwise_xor(background_img,normal_line_img))



        if save: 
            path=input('Path for saving: ')

            print('Image name: ', image_name + '.jpg')
            image_name='/'+image_name+'.jpg'
            path_and_name = path + image_name

            print(path_and_name)

            final_img = background_img
            
            status = cv2.imwrite(path_and_name, final_img)
                
            if status: 
                print('Image successfully saved!!!')
                break
            else:
                print('Image not saved successfully')
                break
        
        if cv2.waitKey(1)==ord('q'):
            cv2.destroyAllWindows()
            break
    


