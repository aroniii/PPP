import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
import shutil
from PIL import Image, ImageTk

class PhotoAlbumApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Photo Album App")
        
        self.loginForm = tk.Frame(root)
        self.loginForm.pack(pady=20)

        self.labelUsername = tk.Label(self.loginForm, text="Username: ")
        self.labelUsername.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.entryUsername = tk.Entry(self.loginForm)
        self.entryUsername.grid(row=0, column=1, padx=10, pady=10)

        self.labelPassword = tk.Label(self.loginForm, text="Password: ")
        self.labelPassword.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.entryPassword = tk.Entry(self.loginForm, show="*")
        self.entryPassword.grid(row=1, column=1, padx=10, pady=10)

        self.login_button = tk.Button(self.loginForm, text="Login", command=self.login)
        self.login_button.grid(row=2, column=1, pady=10)



    def login(self):
        
        username = self.entryUsername.get()
        password = self.entryPassword.get()

       
        if username == "user" and password == "password":
            self.show_options_page()
        else:
            messagebox.showerror("Invalid username or password")



    def show_options_page(self):
        
        self.loginForm.destroy()

        
        self.options_frame = tk.Frame(self.root)
        self.options_frame.pack(pady=20)

        self.add_button = tk.Button(self.options_frame, text="Add Photos", command=self.add_photos)
        self.add_button.grid(row=0, column=0, padx=10, pady=10)

        self.view_button = tk.Button(self.options_frame, text="View Photos", command=self.view_photos)
        self.view_button.grid(row=0, column=1, padx=10, pady=10)



    def add_photos(self):
        
        file_paths = filedialog.askopenfilenames(title="Select Photos", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

        if file_paths:
            
            album_folder = 'albumi'
            os.makedirs(album_folder, exist_ok=True)

            for file_path in file_paths:
                
                file_name = os.path.basename(file_path)

               
                destination_path = os.path.join(album_folder, file_name)
                shutil.copyfile(file_path, destination_path)

            messagebox.showinfo("Photos added to the album sucsessfully!")



    def view_photos(self):

        try:
            album_folder = 'albumi'
            file_paths = [os.path.join(album_folder, file) for file in os.listdir(album_folder) if file.lower().endswith(('.png', '.jpg', '.jpeg'))]

            if file_paths:

                view_window = tk.Toplevel(self.root)
                view_window.title("View Photos")

                canvas = tk.Canvas(view_window)
                canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

                scrollbar = tk.Scrollbar(view_window, command=canvas.yview)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

                frame = tk.Frame(canvas)
                canvas.create_window((0, 0), window=frame, anchor=tk.NW)

                canvas.configure(yscrollcommand=scrollbar.set, scrollregion=canvas.bbox(tk.ALL))

                for i, file_path in enumerate(file_paths):

                    image = Image.open(file_path)
                    image = image.resize((150, 150), resample=Image.LANCZOS)
                    photo = ImageTk.PhotoImage(image)

                    label = tk.Label(frame, image=photo)
                    label.photo = photo
                    label.grid(row=i // 8, column=i % 8, padx=20, pady=20)



                def on_canvas_configure(event):
                    canvas.configure(scrollregion=canvas.bbox(tk.ALL))

                frame.bind("<Configure>", on_canvas_configure)
            else:
                messagebox.showinfo("Info", "No photos in the album.")
        except FileNotFoundError:
            messagebox.showinfo("Info", "No album folder found.")

root = tk.Tk()
app = PhotoAlbumApp(root)
root.mainloop()
