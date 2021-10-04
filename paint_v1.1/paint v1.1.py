import cv2

import numpy as np





color= ['Red','Green','Blue']

circle_center=[]

rectangle_coordinates=[] 

drawing= None


smart_line_coordinates=[]

line_coordinates=[]

red_green_blue_puta=0

x1,y1=-1,-1

def nothing(x):
    pass



def makeRGB(winname):
    for i in range(3):
        cv2.createTrackbar(color[i],winname,0,255,nothing)




def returnRGB(winname):

  red = cv2.getTrackbarPos(color[0],winname)
  green = cv2.getTrackbarPos(color[1],winname)
  blue =  cv2.getTrackbarPos(color[2],winname)

  return red,green,blue

def Thickness(winname):

    thickness=cv2.getTrackbarPos("Thickness:",winname)

    thickness=-1 if thickness==0 else thickness

    return thickness


def Done(shape__):
    cv2.setTrackbarPos("Done:",shape__,0)
    cv2.destroyWindow(shape__)

    cv2.setTrackbarPos(shape__,"Shapes",0)


def Delete(shape__):
    cv2.setTrackbarPos("Delete:",shape__,0)
    cv2.destroyWindow(shape__)

    cv2.setTrackbarPos(shape__,"Shapes",0)


def Shapes(event,x,y,flags,params):

    global circle_center,rectangle_coordinates,line_coordinates


    global drawing

    if cv2.getTrackbarPos("Brush",shapes) == 1 and event==cv2.EVENT_LBUTTONDOWN: 


        makeRGB("Brush")


        cv2.createTrackbar("Thickness:","Brush",0,100,nothing)
        cv2.createTrackbar("Done:","Brush",0,1,nothing)

        if event==cv2.EVENT_LBUTTONDOWN: 
            drawing=True
            

        elif event==cv2.EVENT_MOUSEMOVE:    
            if drawing:

                brush_red,brush_green,brush_blue=returnRGB("Brush")
            
                brush_thickness=cv2.getTrackbarPos("Thickness:","Brush")

                cv2.circle(blank_img,(x,y),brush_thickness,(brush_blue,brush_green,brush_red),-1)
               
            
        elif event==cv2.EVENT_LBUTTONUP:
            drawing=False 
            

    if  event==cv2.EVENT_LBUTTONDOWN and cv2.getTrackbarPos("Circle",shapes) == 1:


        circle_center.clear()


        circle_center.append((x,y))
     
        makeRGB("Circle")

        
        cv2.createTrackbar("Radius:","Circle",0,100,nothing)

        cv2.createTrackbar("Thickness:","Circle",0,100,nothing)



        cv2.createTrackbar("Done:","Circle",0,1,nothing)


        cv2.createTrackbar("Delete:","Circle",0,1,nothing)
        
        


    elif event==cv2.EVENT_LBUTTONDOWN and cv2.getTrackbarPos("Rectangle",shapes) == 1: 


    
        rectangle_coordinates.append((x,y))
            

        makeRGB("Rectangle")

        cv2.createTrackbar("Thickness:","Rectangle",0,100,nothing)

        cv2.createTrackbar("Done:","Rectangle",0,1,nothing)

        cv2.createTrackbar("Delete:","Rectangle",0,1,nothing)


    elif  event==cv2.EVENT_LBUTTONDOWN and cv2.getTrackbarPos("Line",shapes) == 1:

        line_coordinates.append((x,y))

        makeRGB("Line")

        cv2.createTrackbar("Thickness:","Line",0,100,nothing)

        cv2.createTrackbar("Done:","Line",0,1,nothing)

        cv2.createTrackbar("Delete:","Line",0,1,nothing)




def main():

    global circle_center,rectangle_coordinates,line_coordinates

 

    global image_name,shapes,blank_img


    preview  =None

    save  =None

    height =int(input("Input height: "))
    width =int (input("Input width: "))


    color_img = np.zeros((height,width,3),np.uint8)

    blank_img = np.zeros((height,width,3),np.uint8)



    image_name=input("Input image name: ")


    cv2.namedWindow(image_name)

    for i in range(3):
        cv2.createTrackbar(color[i],image_name,0,255,nothing)
    

    cv2.createTrackbar("Preview",image_name,0,1,nothing)

    cv2.createTrackbar("Save",image_name,0,1,nothing)


    shapes="Shapes"

    cv2.namedWindow(shapes)

    cv2.createTrackbar("Brush",shapes,0,1,nothing)
    cv2.createTrackbar("Circle",shapes,0,1,nothing)
    cv2.createTrackbar("Rectangle",shapes,0,1,nothing)
    cv2.createTrackbar("Line",shapes,0,1,nothing)    


    cv2.setMouseCallback(image_name,Shapes)
    
    while True:

        


        background_red,background_green,background_blue=returnRGB(image_name)

        color_img[:]=[background_blue,background_green,background_red]

        background_img = cv2.bitwise_xor(color_img,blank_img)
        


        cv2.imshow(image_name,background_img)

        if  cv2.getTrackbarPos("Preview",image_name) == 1:
            preview = True

        else:
            preview  =False

        if cv2.getTrackbarPos("Save",image_name) ==1:
            save = True
        else:
            save= False

        if preview:
            cv2.imshow("Preview",background_img)
        else:
            cv2.destroyWindow("Preview")


        


        if cv2.getTrackbarPos("Circle",shapes)==1:
            
            cv2.namedWindow("Circle")
            circle_img=np.zeros((height,width,3),np.uint8)
            
            if len(circle_center)>0:

                done=False
                xy=circle_center[-1]

                circle_red,circle_green,circle_blue=returnRGB("Circle")

                circle_thickness=Thickness("Circle")

                circle_radius=cv2.getTrackbarPos("Radius:","Circle")

                cv2.circle(circle_img,xy,circle_radius,(circle_blue,circle_green,circle_red),circle_thickness)
           

                cv2.imshow(image_name,cv2.bitwise_xor(background_img  ,circle_img))


               

                done=cv2.getTrackbarPos("Done:","Circle")

            
                delete=cv2.getTrackbarPos("Delete:","Circle")

                if done==1 and delete==0:

                    cv2.circle(blank_img,xy,circle_radius,(circle_blue,circle_green,circle_red),circle_thickness)
                    
                    circle_center.clear()
                    Done("Circle")

                elif delete==1 and done==0:
                    Delete("Circle")
                    circle_center.clear()

        elif  cv2.getTrackbarPos("Rectangle",shapes)==1:


            rectangle_img=np.zeros((height,width,3),np.uint8)

            cv2.namedWindow("Rectangle")
            
            if len(rectangle_coordinates)>1:

                x1,y1=rectangle_coordinates[-1]
                
                x2,y2=rectangle_coordinates[-2]


                rectangle_red,rectangle_green,rectangle_blue=returnRGB("Rectangle")

                rectangle_thickness=Thickness("Rectangle")
            
                cv2.rectangle(rectangle_img,(x1,y1),(x2,y2),(rectangle_blue,rectangle_green,rectangle_red),rectangle_thickness)


                done=cv2.getTrackbarPos("Done:","Rectangle")
                delete=cv2.getTrackbarPos("Delete:","Rectangle")


                if done==1 and delete==0:

                   Done("Rectangle")
                   cv2.rectangle(blank_img,(x1,y1),(x2,y2),(rectangle_blue,rectangle_green,rectangle_red),rectangle_thickness)

                   rectangle_coordinates.clear()

                elif delete==1 and done==0:
                   
                    Delete("Rectangle")

                    rectangle_coordinates.clear()

            cv2.imshow(image_name,cv2.bitwise_xor(background_img,rectangle_img))

        elif cv2.getTrackbarPos("Line",shapes) == 1:

            line_img =np.zeros((height,width,3),np.uint8)

            cv2.namedWindow("Line")



            if len(line_coordinates) >1:

                x1,y1=line_coordinates[0]

                x2,y2=line_coordinates[1]


                line_red,line_green,line_blue=returnRGB("Line")

                line_thickness=cv2.getTrackbarPos("Thickness:","Line")


                
                line_thickness=1 if line_thickness==0 else line_thickness

                cv2.line(line_img,(x1,y1),(x2,y2),(line_blue,line_green,line_red),line_thickness)

                cv2.imshow(image_name,cv2.bitwise_xor(background_img,line_img))

                done=cv2.getTrackbarPos("Done:","Line")

                delete=cv2.getTrackbarPos("Delete:","Line")

                if done==1 and delete==0:
                    Done("Line")
                    cv2.line(blank_img,(x1,y1),(x2,y2),(line_blue,line_green,line_red),line_thickness)
                    line_coordinates.clear()


                elif delete==1 and done==0:
                    Delete("Line")
                    line_coordinates.clear()

        elif cv2.getTrackbarPos("Brush","Shapes")==1:
            


            cv2.namedWindow("Brush")
            
            
            if cv2.getTrackbarPos("Done:","Brush") == 1:
                Done("Brush")

            cv2.imshow(image_name,background_img)

        if save:
            path=input("Path for saving: ")

            print("Image name: ", image_name + ".jpg")

            image_name='/'+image_name+".jpg"
            path_and_name = path + image_name

            print(path_and_name)

            final_img = background_img
            
            status = cv2.imwrite(path_and_name, final_img)
                
            if status: 
                print("Image successfully saved!!!")
                break
            else:
                print("Image not successfully saved")
                break
        if cv2.waitKey(1) == ord('q'): 
    
            cv2.destroyAllWindows()   
            break



if __name__=="__main__":
    main()

    cv2.waitKey(0)
    cv2.destroyAllWindows()

