from PIL import Image
import tkinter as tk
from tkinter import filedialog as fd 
from datetime import datetime
import os

ASCII_CHARS = ['.', ',', ':', ';', '+', '*', '?', '%', 'S', '#', '@']
ASCII_CHARS = ASCII_CHARS[::-1]


def resize(image, new_width=100):
    (old_width, old_height) = image.size
    aspect_ratio = float(old_height)/float(old_width)
    new_height = int(aspect_ratio * new_width)
    new_dim = (new_width, new_height)
    new_image = image.resize(new_dim)
    return new_image


def grayscalify(image):
    return image.convert('L')


def modify(image, buckets=25):
    initial_pixels = list(image.getdata())
    new_pixels = [ASCII_CHARS[pixel_value//buckets]
                  for pixel_value in initial_pixels]
    return ''.join(new_pixels)


def do(image, new_width=100):
    image = resize(image)
    image = grayscalify(image)

    pixels = modify(image)
    len_pixels = len(pixels)

    # Construct the image from the character list
    new_image = [pixels[index:index+new_width]
                 for index in range(0, len_pixels, new_width)]

    return '\n'.join(new_image)


def gui():
    window = tk.Tk()
    window.geometry("600x100")
    window.title("ASCII Image Converter")
    window.iconbitmap("icon.ico")
    instructions = tk.Label(window, text="Insert path for the image you want to convert here:", font=("Arial", 15))
    instructions.grid(column=0, row=0)

    entry = tk.Entry(window, font=("Arial", 9), width=50)
    entry.grid(row=1, column=0)

    def browse_path():
        os.startfile("Pictures")

    def browse():
        path = fd.askopenfilename(filetypes=(("jpg file", "*.jpg"),("png file", "*.png")))
        entry.insert(tk.END, path)
    browse_button = tk.Button(window, text="BROWSE", command=browse, width=12)
    browse_button.grid(column=1, row=1)

    openPath = tk.Button(window, text="OPEN RESULTS", command=browse_path, width=12)

    def convert():
        path = entry.get()
        print(path)
        runner(path)
        openPath.grid(row=3, column=1)

    convert_button = tk.Button(window, text="CONVERT", command=convert)
    convert_button.grid(row=3, column=0)

    
    def runner(path):
        datetime_ = datetime.now()
        time_ = datetime_.strftime("%y-%m-%d-%M-%S")
        image = None
        try:
            image = Image.open(path)
        except Exception:
            print("Unable to find image in", path)
                # print(e)
            return
        image = do(image)

        # To print on console

        # Else, to write into a file
        # Note: This text file will be created by default under
        #       the same directory as this python file,
        #       NOT in the directory from where the image is pulled.
        f = open('Pictures/img-' +"-"+ str(time_)  +'.txt', 'w')
        f.write(image)
        f.close()   

    window.mainloop()


if __name__ == '__main__':
    gui()
