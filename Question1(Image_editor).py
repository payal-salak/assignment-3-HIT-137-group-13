# GROUP NAME : CAS/DAN GROUP-13
# GROUP MEMBERS: 389249 PAYAL
#                391075 AMANPARTEEK SINGH
#                390786 ANSHUL
#                361253 ASHTON SEARLE
#                391273 KOMALPREET KAUR

# Importing Required Libraries
from tkinter import *
from tkinter import filedialog,ttk
import cv2
from PIL import ImageTk, Image

class ImageEditor:
    # Creating init method which will get executed at object creation time
    def __init__(self,root):
        self.root = root
        self.root.title("Python Image Editor - CAS/DAN Group = 15")
        self.root.geometry("1200x800")

        self.original_image = None
        self.modified_image = None
        self.filename = None

        # We will use two stacks for Undo / Redo functionality
        self.undo_stack = []
        self.redo_stack = []

        # Attributes for cropping Function
        self.crop_mode = None
        self.crop_start_x = None
        self.crop_start_y = None
        self.crop_id = None

        self.main_ui()

    def main_ui(self):

        # Top container will hold two canvas for original and modified images
        self.canvas_frame = Frame(self.root)
        self.canvas_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Canvas to show original Image
        self.canvas_original = Canvas(self.canvas_frame, width=350, height=350, bg="gray")
        self.canvas_original.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)

        # Canvas to show modified Image
        self.canvas_modified = Canvas(self.canvas_frame, width=350, height=350, bg="gray")
        self.canvas_modified.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)

        # Creating Frame for buttons and slider
        self.button_frame = Frame(self.root,padx=20, pady=10)
        self.button_frame.pack(fill=X)

        # Adding Buttons and Slider
        select_image_button = Button(self.button_frame, text="Select Image", command=self.select_image)
        select_image_button.pack(side=LEFT, padx=5)
        crop_button = Button(self.button_frame, text="Crop", command=self.crop)
        crop_button.pack(side=LEFT, padx=5)
        grayscale_button = Button(self.button_frame, text="Grayscale", command=self.grayscale)
        grayscale_button.pack(side=LEFT, padx=5)
        rotate_button = Button(self.button_frame, text="Rotate", command=self.rotate)
        rotate_button.pack(side=LEFT, padx=5)
        undo_button = Button(self.button_frame, text="Undo", command=self.undo)
        undo_button.pack(side=LEFT, padx=5)
        redo_button = Button(self.button_frame, text="Redo", command=self.redo)
        redo_button.pack(side=LEFT, padx=5)
        self.zoom_slider = Scale(self.button_frame, label="Zoom Image", from_=25, to=125, orient=HORIZONTAL, length=300, command=self.slider)
        self.zoom_slider.set(75)
        self.zoom_slider.pack(side=LEFT, padx=10)
        save_image_button = Button(self.button_frame, text="Save Image", command=self.save_image)
        save_image_button.pack(side=LEFT, padx=5)

        instructions = Label(self.root, text=
            '''Instructions:                                                                                                                                Shortcuts:
            1. Select image to edit.                                                                                                            Select Image = Control + O      Undo = Control + Z
            2. View the original image on left and make changes to right image.                                 Crop = Control + C                    Redo = Control + Y
            3. Use functionality like Crop, Grayscale, or Rotate to edit image.                                     Grayscale = Control + G            Save Image = Control + S
            4. Use Undo/Redo, Zoom, and save your image.                                                                  Rotate = Control + R
            5. Use keyboard shortcuts for faster operations!''',
            justify=LEFT,
            padx=10
        )
        instructions.pack(pady=10)

        # Adding Keyboard Shortcuts
        self.root.bind("<Control-o>", lambda event: self.select_image())
        self.root.bind("<Control-c>", lambda event: self.crop())
        self.root.bind("<Control-g>", lambda event: self.grayscale())
        self.root.bind("<Control-r>", lambda event: self.rotate())
        self.root.bind("<Control-z>", lambda event: self.undo())
        self.root.bind("<Control-y>", lambda event: self.redo())
        self.root.bind("<Control-s>", lambda event: self.save_image())

    def select_image(self):
        # Opens file manager to select a File
        self.filename = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png *.jpg *.jpeg")],
        )
        if not self.filename:
            return

        # Loading the image using OpenCV
        self.original_image = cv2.imread(self.filename)
        if self.original_image is None:
            print("Error! Image not Loaded!")
            return

        # Remove previous image and clear undo/redo Stacks
        self.modified_image = None
        self.undo_stack.clear()
        self.redo_stack.clear()

        # Display the selected image
        self.display_image()

    def display_image(self):
        if self.original_image is None:
            print("Error! Image not Loaded!")
            return

        # Set Slider Value
        slider_value = self.zoom_slider.get() if hasattr(self, "zoom_slider") else 100
        factor = slider_value / 100

        # Display Original Image
        original_image_rgb = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
        original_height, original_width, original_channels = original_image_rgb.shape

        # We try to resize image so that it fits in canvas of size 600x600
        original_scale = min(600/original_width, 600/original_height, 1)
        original_preview_scale = original_scale * factor
        preview_original_width = int(original_width * original_preview_scale)
        preview_modified_height = int(original_height * original_preview_scale)
        preview_original_image = cv2.resize(original_image_rgb, (preview_original_width, preview_modified_height), interpolation=cv2.INTER_AREA)

        # Display Original Image in left Canvas
        self.tk_original_image = ImageTk.PhotoImage(image=Image.fromarray(preview_original_image))
        self.canvas_original.config(width=preview_original_width, height=preview_modified_height)
        self.canvas_original.delete("all")
        self.canvas_original.create_image(preview_original_width // 2, preview_modified_height // 2, image=self.tk_original_image)      # It places image in the center of canvas

        # Loading Modified Image
        if self.modified_image is None:
            image_to_show = self.original_image
        else:
            image_to_show = self.modified_image
        modified_image_rgb = cv2.cvtColor(image_to_show, cv2.COLOR_BGR2RGB)

        # We try to resize image so that it fits in canvas of size 600x600
        modified_height, modified_width, modified_channels = modified_image_rgb.shape
        modified_scale = min(600/modified_width, 600/modified_height, 1)
        modified_preview_scale = modified_scale * factor
        preview_modified_width = int(modified_width * modified_preview_scale)
        preview_modified_height = int(modified_height * modified_preview_scale)
        preview_modified_image = cv2.resize(modified_image_rgb, (preview_modified_width, preview_modified_height), interpolation=cv2.INTER_AREA)

        # Display Modified Image in Right Canvas
        self.tk_modified_image = ImageTk.PhotoImage(Image.fromarray(preview_modified_image))
        self.canvas_modified.config(width=preview_modified_width, height=preview_modified_height)
        self.canvas_modified.delete("all")
        self.canvas_modified.create_image(preview_modified_width // 2, preview_modified_height // 2, image=self.tk_modified_image)      # It places Image in center of canvas

        # Saving the preview dimensions
        self.preview_dimensions = (preview_modified_width, preview_modified_height)
        self.ratio = modified_width / preview_modified_width if preview_modified_width != 0 else 1

    def crop(self):
        if self.original_image is None and self.modified_image is None:
            print("Error! No Image available to Crop!")
            return
        self.crop_mode = True

        # Binding mouse clicks for crop action on right canvas
        self.canvas_modified.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas_modified.bind("<B1-Motion>", self.on_mouse_move)
        self.canvas_modified.bind("<ButtonRelease-1>", self.on_button_release)
        print("Crop mode activated. Click and drag on Right canvas to select the area.")

    def on_button_press(self, event):
        # Record the starting position for Crop action
        self.crop_start_x = event.x
        self.crop_start_y = event.y
        if self.crop_id:
            self.canvas_modified.delete(self.crop_id)
            self.crop_id = None

    def on_mouse_move(self, event):
        # Updating the crop rectangle as the mouse is dragged
        if not self.crop_mode:
            return
        current_x, current_y = event.x, event.y
        if self.crop_id is None:
            self.crop_id = self.canvas_modified.create_rectangle(self.crop_start_x, self.crop_start_y, current_x, current_y, outline="red", width=2)
        else:
            self.canvas_modified.coords(self.crop_id, self.crop_start_x, self.crop_start_y, current_x, current_y)

    def on_button_release(self, event):
        # Record the final position for crop action
        if not self.crop_mode:
            return
        crop_end_x, crop_end_y = event.x, event.y

        # Unbinding crop related events from right side canvas
        self.canvas_modified.unbind("<ButtonPress-1>")
        self.canvas_modified.unbind("<B1-Motion>")
        self.canvas_modified.unbind("<ButtonRelease-1>")
        self.crop_mode = False

        # Showing cropped image in right canvas
        canvas_width = self.canvas_modified.winfo_width()
        canvas_height = self.canvas_modified.winfo_height()
        x1 = min(self.crop_start_x, canvas_width)
        y1 = min(self.crop_start_y, canvas_height)
        x2 = min(crop_end_x, canvas_width)
        y2 = min(crop_end_y, canvas_height)
        x1, x2 = sorted([x1, x2])
        y1, y2 = sorted([y1, y2])

        # If the selected rectangle is too small
        if x2-x1 < 5 or y2-y1 < 5:
            print("Selected Area is too small to crop!")
            if self.crop_id:
                self.canvas_modified.delete(self.crop_id)
                self.crop_id = None
            return

        # Use the cropped image for further editing
        if self.modified_image is None:
            current_image = self.original_image
        else:
            current_image = self.modified_image

        if current_image is None:
            print("Error! No Image available to Edit!")

        # Converting canvas coordinates to image coordinates
        x1_image = int(x1 * self.ratio)
        y1_image = int(y1 * self.ratio)
        x2_image = int(x2 * self.ratio)
        y2_image = int(y2 * self.ratio)

        # Ensuring that the coordinates are within the boundary
        original_height, original_width = current_image.shape[:2]
        x1_image = min(original_width, x1_image)
        y1_image = min(original_height, y1_image)
        x2_image = min(original_width, x2_image)
        y2_image = min(original_height, y2_image)

        if x2_image - x1_image < 1 or y2_image - y1_image < 1:
            print("Crop coordinates out of boundary!!")
            return

        # Saving current state
        self.save_state()
        cropped_image = current_image[y1_image:y2_image, x1_image:x2_image].copy()
        self.modified_image = cropped_image

        if self.crop_id:
            self.canvas_modified.delete(self.crop_id)
            self.crop_id = None

        self.display_image()
        print("Image Cropped Successfully!")

    def save_state(self):
        # This saves the current state into undo stack and clears redo stack
        if self.modified_image is None:
            current_image = self.original_image
        else:
            current_image = self.modified_image

        self.undo_stack.append(current_image.copy())
        self.redo_stack.clear()

    def grayscale(self):
        # Converts Colour image to Grayscale
        if self.modified_image is None:
            current_image = self.original_image
        else:
            current_image = self.modified_image

        if current_image is None:
            print("Error! No Image available to Grayscale!")
            return

        self.save_state()
        gray_image = cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY)
        gray_bgr_image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)
        self.modified_image = gray_bgr_image
        self.display_image()
        print("Grayscale Successfully!")


    def rotate(self):
        # Rotates image to 90 degrees clockwise
        if self.modified_image is None:
            current_image = self.original_image
        else:
            current_image = self.modified_image

        if current_image is None:
            print("Error! No Image available to Rotate!")
            return

        self.save_state()
        rotated_image = cv2.rotate(current_image, cv2.ROTATE_90_CLOCKWISE)
        self.modified_image = rotated_image
        self.display_image()
        print("Rotated Successfully!")

    def undo(self):
        # This will undo last modified action
        if not self.undo_stack:
            print("Error! Nothing available to undo!")
            return

        if self.modified_image is None:
            current_image = self.original_image
        else:
            current_image = self.modified_image

        if current_image is not None:
            self.redo_stack.append(current_image.copy())
        previous_image = self.undo_stack.pop()
        self.modified_image = previous_image
        self.display_image()
        print("Image Undo Successfully!")

    def redo(self):
        # Redo last undone modification
        if not self.redo_stack:
            print("Error! Nothing available to redo!")
            return

        if self.modified_image is None:
            current_image = self.original_image
        else:
            current_image = self.modified_image

        if current_image is not None:
            self.undo_stack.append(current_image.copy())
        next_image = self.redo_stack.pop()
        self.modified_image = next_image
        self.display_image()
        print("Image Redo Successfully!")

    def slider(self, value):
        if self.original_image is None:
            return
        self.display_image()

    def save_image(self):
        # This saves the current state of modified image
        if self.modified_image is None:
            image_to_save = self.original_image
        else:
            image_to_save = self.modified_image

        if image_to_save is None:
            print("Error! No Image available to save!")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=(("JPG files", ".jpg"),("PNG files", ".png"),("JPEG files", ".jpeg")))

        if save_path is None:
            return

        if self.preview_dimensions is not None:
            new_width, new_height = self.preview_dimensions
            resized_image = cv2.resize(image_to_save, (new_width, new_height),interpolation=cv2.INTER_AREA)
        else:
            resized_image = image_to_save

        cv2.imwrite(save_path, resized_image)
        print(f"Image Saved to {save_path}")


def main():
    root = Tk()
    app = ImageEditor(root)
    root.mainloop()

main()
