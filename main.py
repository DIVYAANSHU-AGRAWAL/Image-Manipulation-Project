from tkinter import *
from tkinter import filedialog, colorchooser, messagebox
from PIL import Image, ImageTk, ImageOps, ImageFilter, ImageGrab, ImageEnhance

# Main Window Setup
root = Tk()
root.geometry("1200x700")
root.title("Divyaanshu's Image Editing Tool")
root.config(bg="White")

# Global Variables
file_path = None
pen_color = "Black"
pen_size = 5
image = None

# Function to Add an Image
def addimage():
    global file_path, image
    file_path = filedialog.askopenfilename()  # Open file dialog to select an image
    if not file_path:
        return
    image = Image.open(file_path)
    width, height = int(image.width / 2), int(image.height / 2)
    image = image.resize((width, height))  # Resize image for better display
    my_canvas.config(width=image.width, height=image.height)
    image = ImageTk.PhotoImage(image)
    my_canvas.image = image
    my_canvas.create_image(0, 0, image=image, anchor="nw")

# Function to Save the Edited Image
def save_image():
    x = root.winfo_rootx() + my_canvas.winfo_x()
    y = root.winfo_rooty() + my_canvas.winfo_y()
    x1 = x + my_canvas.winfo_width()
    y1 = y + my_canvas.winfo_height()
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
    if save_path:
        ImageGrab.grab(bbox=(x, y, x1, y1)).save(save_path)
        messagebox.showinfo("Image Saved", "Image saved successfully!")

# Function to Flip or Rotate the Image
def flip_or_rotate(option):
    global image
    if not file_path:
        messagebox.showerror("Error", "No image loaded to flip or rotate!")
        return
    img = Image.open(file_path)
    if option == "Flip Horizontal":
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    elif option == "Flip Vertical":
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
    elif option == "Rotate 90°":
        img = img.rotate(-90, expand=True)
    elif option == "Rotate 180°":
        img = img.rotate(180, expand=True)
    elif option == "Rotate 270°":
        img = img.rotate(90, expand=True)
    width, height = int(img.width / 2), int(img.height / 2)
    img = img.resize((width, height))
    image = ImageTk.PhotoImage(img)
    my_canvas.image = image
    my_canvas.create_image(0, 0, image=image, anchor="nw")

# Drawing Functionality
def drawfunc(event):
    x1, y1 = (event.x - pen_size), (event.y - pen_size)
    x2, y2 = (event.x + pen_size), (event.y + pen_size)
    my_canvas.create_oval(x1, y1, x2, y2, fill=pen_color, outline="")

# Change Pen Color
def choosecolor():
    global pen_color
    pen_color = colorchooser.askcolor(title="Choose Color of Pen!")[1]

# Change Pen Size
def changesize(size):
    global pen_size
    pen_size = size

# Clear Canvas
def clearcanvas():
    my_canvas.delete("all")

# Apply Filters
def apply_filter(options_var):
    if not file_path:
        messagebox.showerror("Error", "No image loaded to apply filters!")
        return
    img = Image.open(file_path)
    width, height = int(img.width / 2), int(img.height / 2)
    img = img.resize((width, height))
    if options_var == "Black and White":
        img = ImageOps.grayscale(img)
    elif options_var == "Blur":
        img = img.filter(ImageFilter.BLUR)
    elif options_var == "Sharpen":
        img = img.filter(ImageFilter.SHARPEN)
    elif options_var == "Smooth":
        img = img.filter(ImageFilter.SMOOTH)
    elif options_var == "Emboss":
        img = img.filter(ImageFilter.EMBOSS)
    img = ImageTk.PhotoImage(img)
    my_canvas.image = img
    my_canvas.create_image(0, 0, image=img, anchor="nw")

# Brightness Adjustment
def Brightnessfunc():
    if not file_path:
        messagebox.showerror("Error", "No image loaded to adjust brightness!")
        return
    img = Image.open(file_path)
    width, height = int(img.width / 2), int(img.height / 2)
    img = img.resize((width, height))
    enhancer = ImageEnhance.Brightness(img)
    factor = my_slider.get()
    img = enhancer.enhance(factor)
    img = ImageTk.PhotoImage(img)
    my_canvas.image = img
    my_canvas.create_image(0, 0, image=img, anchor="nw")

# UI Setup
left_frame = Frame(root, width=600, height=800, bg="Grey", relief=SUNKEN, borderwidth=6)
left_frame.pack(side="left", fill=Y)

add_image_button = Button(left_frame, text="Add Image", bg="White", font=20, command=addimage)
add_image_button.pack(pady=15, padx=5)

Pen_color_button = Button(left_frame, text="Change Pen Color", font=("comicsansms", 15), command=choosecolor, relief=GROOVE, borderwidth=4)
Pen_color_button.pack(pady=10)

r = IntVar()
Radiobutton(left_frame, text="Small", font=15, variable=r, value=5, command=lambda: changesize(5)).pack(pady=5)
Radiobutton(left_frame, text="Medium", font=15, variable=r, value=10, command=lambda: changesize(10)).pack(pady=5)
Radiobutton(left_frame, text="Large", font=15, variable=r, value=18, command=lambda: changesize(18)).pack(pady=5)

clear_button = Button(left_frame, text="Clear Drawing", font=("Red", 15), bg="Red", command=clearcanvas).pack(pady=30)

# Brightness Control
text_label = Label(left_frame, text="Brightness Controller", font=15).pack(pady=4)
my_slider = Scale(left_frame, from_=1, to_=5, orient=HORIZONTAL)
my_slider.pack(pady=5)
setbrightnessbutton = Button(left_frame, text="Set Brightness", command=Brightnessfunc).pack(pady=5)

# Filters
options = ["Black and White", "Emboss", "Sharpen", "Blur", "Smooth"]
options_var = StringVar()
drop = OptionMenu(left_frame, options_var, *options)
drop.pack(pady=5)
apply_filter_button = Button(left_frame, text="Apply Filter", command=lambda: apply_filter(options_var.get())).pack(pady=5)

# Flip and Rotate
flip_options = ["Flip Horizontal", "Flip Vertical", "Rotate 90°", "Rotate 180°", "Rotate 270°"]
flip_var = StringVar()
flip_menu = OptionMenu(left_frame, flip_var, *flip_options)
flip_menu.pack(pady=5)
apply_flip_button = Button(left_frame, text="Flip/Rotate", command=lambda: flip_or_rotate(flip_var.get())).pack(pady=5)

# Save Image
save_button = Button(left_frame, text="Save Image", command=save_image, bg="Green", font=15).pack(pady=10)

Exit_button = Button(root, text="EXIT", font=("comicsansms", 15, "bold"), bg="Yellow", command=root.quit, relief=GROOVE)
Exit_button.pack(side=BOTTOM, anchor=CENTER)

my_canvas = Canvas(root, width=850, height=550, relief=SUNKEN, borderwidth=10)
my_canvas.pack(pady=20)

my_canvas.bind("<B1-Motion>", drawfunc)

root.mainloop()
