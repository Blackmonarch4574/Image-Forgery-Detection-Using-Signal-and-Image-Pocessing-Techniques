from tkinter import *
from tkinter import filedialog, ttk, messagebox
from PIL import ImageTk, Image
from ForgeryDetection import Detect

class CopyMoveForgeryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Copy-Move Detector")
        self.root.iconbitmap('images/favicon.ico')
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.state("zoomed")

        self.IMG_WIDTH = 400
        self.IMG_HEIGHT = 400
        self.uploaded_image = None

        # Set ttkthemes style
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Create GUI components
        self.create_widgets()

    def create_widgets(self):
        # Label for the results of scan
        result_label = Label(self.root, text="IMAGE FORGERY DETECTOR", font=("Courier", 30))
        result_label.grid(row=0, column=0, columnspan=3, pady=(20, 10))

        # Get the blank image
        input_img = self.get_image("images/input.png")
        middle_img = self.get_image("images/middle.png")
        output_img = self.get_image("images/output.png")

        # Displays the input image
        self.image_panel = Label(self.root, image=input_img)
        self.image_panel.image = input_img
        self.image_panel.grid(row=1, column=0, padx=5)

        # Label to display the middle image
        middle_label = Label(self.root, image=middle_img)
        middle_label.image = middle_img
        middle_label.grid(row=1, column=1, padx=5)

        # Label to display the output image
        self.result_panel = Label(self.root, image=output_img)
        self.result_panel.image = output_img
        self.result_panel.grid(row=1, column=2, padx=5)

        # Label to display the path of the input image
        self.file_label = Label(self.root, text="No file selected", fg="grey", font=("Helvetica", 12))
        self.file_label.grid(row=2, column=1, pady=10)

        # Progress bar
        self.progress_bar = ttk.Progressbar(self.root, length=500, mode='determinate')
        self.progress_bar.grid(row=3, column=1, pady=10)

        # Button to upload images
        upload_button = ttk.Button(self.root, text="Upload Image", command=self.browse_file)
        upload_button.grid(row=4, column=1, pady=10)

        # Button to run the Copy-Move detection algorithm
        copy_move_button = ttk.Button(self.root, text="Copy-Move", command=self.copy_move_forgery)
        copy_move_button.grid(row=5, column=1, pady=20)

        # Button to exit the program
        quit_button = ttk.Button(self.root, text="Exit program", command=self.on_close)
        quit_button.grid(row=6, column=2, pady=10)

    def get_image(self, path):
        img = Image.open(path)
        img = img.resize((self.IMG_WIDTH, self.IMG_HEIGHT), Image.LANCZOS)
        return ImageTk.PhotoImage(img)

    def browse_file(self):
        filename = filedialog.askopenfilename(title="Select an image",
                                              filetypes=[("image files", "*.jpg;*.jpeg;*.png")])

        if filename:
            self.uploaded_image = filename
            self.progress_bar['value'] = 0
            self.file_label.configure(text=filename)

            img = self.get_image(filename)
            self.image_panel.configure(image=img)
            self.image_panel.image = img

            blank_img = self.get_image("images/output.png")
            self.result_panel.configure(image=blank_img)
            self.result_panel.image = blank_img

    def copy_move_forgery(self):
        path = self.uploaded_image
        eps = 60
        min_samples = 2

        if path is None:
            messagebox.showerror('Error', "Please select image")
            return

        detect = Detect(path)
        key_points, descriptors = detect.siftDetector()
        forgery = detect.locateForgery(eps, min_samples)

        self.progress_bar['value'] = 100

        if forgery is None:
            img = self.get_image("images/no_copy_move.png")
            self.result_panel.configure(image=img)
            self.result_panel.image = img
            self.file_label.configure(text="ORIGINAL IMAGE", foreground="green")
        else:
            img = self.get_image("images/copy_move.png")
            self.result_panel.configure(image=img)
            self.result_panel.image = img
            self.file_label.configure(text="Image Forged", foreground="red")

    def on_close(self):
        self.root.destroy()

if __name__ == "__main__":
    root = Tk()
    app = CopyMoveForgeryApp(root)
    root.mainloop()
