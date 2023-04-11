import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import PyPDF2
import os
import pyttsx3


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("PDF to MP3 Converter")
        self.configure(bg="#3b3b3b")
        self.resizable(False, False)
        icon = tk.PhotoImage(file="icon.png")
        self.wm_iconphoto(True, icon)
        
        # Import button
        self.import_button = ctk.CTkButton(self, text="Import PDF", command=self.import_pdf)
        self.import_button.grid(row=0, column=0, padx=5, pady=5)
        self.imported_file = ctk.CTkLabel(self, text="No file imported")
        self.imported_file.grid(row=0, column=1, padx=5, pady=5)
        
        # Slider for speech speed
        self.speed_label = ctk.CTkLabel(self, text="Speech Speed:")
        self.speed_label.grid(row=1, column=0, padx=5, pady=5)
        self.speed_slider = ctk.CTkSlider(self, from_=0.5, to=4, command=lambda value: self.speed_value.configure(text=f"x{float(value):.1f}"))
        self.speed_slider.set(1.5)
        self.speed_slider.grid(row=1, column=1, padx=5, pady=5)
        self.speed_value = ctk.CTkLabel(self, text="x" + str(self.speed_slider.get()))
        self.speed_value.grid(row=1, column=2, padx=5, pady=5)
        
        # Slider for volume
        self.volume_label = ctk.CTkLabel(self, text="Volume:")
        self.volume_label.grid(row=2, column=0, padx=5, pady=5)
        self.volume_slider = ctk.CTkSlider(self, from_=0, to=100, command=lambda value: self.volume_value.configure(text=str(int(value)) + "%"))
        self.volume_slider.set(100)
        self.volume_slider.grid(row=2, column=1, padx=5, pady=5)
        self.volume_value = ctk.CTkLabel(self, text=str(self.volume_slider.get()) + "%")
        self.volume_value.grid(row=2, column=2, padx=5, pady=5)

        # Radio button for male/female voice
        self.voice_label = ctk.CTkLabel(self, text="Voice:")
        self.voice_label.grid(row=3, column=0, padx=5, pady=5)
        self.voice_var = tk.IntVar(value=0)
        self.voice_male = ctk.CTkRadioButton(self, text="1", variable=self.voice_var, value=0)
        self.voice_female = ctk.CTkRadioButton(self, text="2", variable=self.voice_var, value=1)
        self.voice_male.grid(row=3, column=1, padx=5, pady=5)
        self.voice_female.grid(row=3, column=2, padx=5, pady=5)
        
        # Entry box for start page
        self.start_label = ctk.CTkLabel(self, text="Start Page:")
        self.start_label.grid(row=4, column=0, padx=5, pady=5)
        self.start_entry = ctk.CTkEntry(self)
        self.start_entry.grid(row=4, column=1, padx=5, pady=5)
        
        # Entry box for end page
        self.end_label = ctk.CTkLabel(self, text="End Page:")
        self.end_label.grid(row=5, column=0, padx=5, pady=5)
        self.end_entry = ctk.CTkEntry(self)
        self.end_entry.grid(row=5, column=1, padx=5, pady=5)
        
        # Test button
        self.test_button = ctk.CTkButton(self, text="Test", command=self.test_speech)
        self.test_button.grid(row=6, column=0, padx=5, pady=5)
        
        # Save button
        self.save_button = ctk.CTkButton(self, text="Save MP3", command=self.save_mp3)
        self.save_button.grid(row=6, column=1, padx=5, pady=5)
        
        # PDF file path
        self.pdf_path = None

        # Slider update function
        def slider_event(slider, value):
            if slider == "speed":
                value.speed_value.configure(text=int(value.speed_slider.get()))
            elif slider == "volume":
                value.volume_value.configure(text=str(int(value.volume_slider.get())) + "%")


    def import_pdf(self):
        self.pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if self.pdf_path != "":
            self.imported_file.configure(text=os.path.basename(self.pdf_path))

    # Test the current voice settings
    def test_speech(self):
        try:
            engine = pyttsx3.init()
            apply_settings(self, engine)
            engine.say("Hey. This is the current voice.")
            engine.runAndWait()
            engine.stop()

        except ValueError as e:
            messagebox.showerror("Error", str(e))


    # Save file with the current voice settings
    def save_mp3(self):
        if self.pdf_path is None:
            messagebox.showerror("Error", "Please import a PDF file.")
        else:
            try:
                pdf = PyPDF2.PdfReader(self.pdf_path)
                if self.start_entry.get() == "" or int(self.start_entry.get()) < 0:
                    start_page = 0
                else:
                    start_page = int(self.start_entry.get()) - 1
                if self.end_entry.get() == "" or int(self.end_entry.get()) > len(pdf.pages):
                    end_page = len(pdf.pages)
                else:
                    end_page = int(self.end_entry.get())
                engine = pyttsx3.init()
                apply_settings(self, engine)
                clean_text = ""
                for page in range(start_page, end_page):
                    text = pdf.pages[page].extract_text()
                    clean_text += text.strip().replace("\n", " ")
                
                save_path = filedialog.asksaveasfilename(defaultextension=".mp3")
                if save_path:
                    engine.save_to_file(clean_text, save_path)
                    engine.runAndWait()
                    engine.stop()
                    messagebox.showinfo("Save", "File saved successfully.")
                    
            except ValueError as e:
                messagebox.showerror("Error", str(e))


# Apply the current settings to the engine
def apply_settings(self, engine):
        engine.setProperty("rate", round(self.speed_slider.get(), 1) * 100)
        engine.setProperty("volume", self.volume_slider.get()/100)
        voices = engine.getProperty("voices")
        engine.setProperty("voice", voices[self.voice_var.get()].id)
        print(round(self.speed_slider.get(), 1) * 100)
        print(self.speed_slider.get() * 100)
    

if __name__ == "__main__":
    app = App()
    app.mainloop()