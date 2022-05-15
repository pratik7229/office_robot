from tkinter import *
from PIL import ImageTk, Image
import rospy
from std_msgs.msg import Bool

lock = rospy.Publisher('/lock', Bool, queue_size=10)
loc = False
def ConfWindow():
    global lock, loc, counter
    # Destroy old frames to start a new UI
    # frame.destroy()
    root = Tk()
    root.attributes('-fullscreen', True)
    initial_frame = LabelFrame(root, text="Confirmation")
    initial_frame.grid(row=0, column=0)
    conf_img = ImageTk.PhotoImage(Image.open("/home/pratik/office_rbt_ws/src/user_interface/scripts/dark-blue-wallpaper-hd-3.jpg"))
    conf_label = Label(initial_frame, image=conf_img)
    conf_label.grid(row=0, column=0)
    conf_frame = LabelFrame(root)#, padx=50, pady=50, background="dark-blue-wallpaper-hd-3.jpg")
    conf_frame.grid(row=0, column=0)
    conf_pickup = Button(conf_frame, text="Confirm Pickup Delivery", width=50, height=10, command=lambda: printfn(root))  # ok is a variable but temporarily considered as a string
    conf_pickup.grid(row=0, column=0, padx=10, pady=10)
    locker_button = Button(conf_frame, text="Open Locker", width=50, height=5, command=lambda: lockerfn(root))
    locker_button.grid(row=1, column=0, padx=10, pady=10)
    root.mainloop()
    return True

def printfn(root):
    #print("ok")
    root.destroy()

def lockerfn(root, counter=None):
    loc = True
    # print("lock open")
    lock.publish(loc)
    rospy.sleep(2)
    loc = False
    lock.publish(loc)



# ConfWindow()