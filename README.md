# PDF-To-MP3-Converter
This is a program where you can convert your pdf files to mp3 files. It makes it easy to listen to your favourite pdf books, while you are on the move.

# Windows:

I included a .exe file for easy use
- Just launch the program
- Choose your pdf file
- Adjust voice settings to your preferance, use the test button to listen to the voice
- Set start and end pages if you don't want the entire pdf. If you don't give a start, it will simply start from the beginning, and if you don't give an end, it will run to the end of the file.
- Click Save and choose where to save it and its name. The name can include .mp3, but it is not necessary.
- **Note**: The file creation can take some time, depending on the size of the file.
- **Note**: If the input is too large, the program will run for a long time, but there seem to be an error while making the mp3 file. I have successfully made mp3 files up to 250MB, this is equivalent of about 1.5 hours of audio.
- **Note**: I recommend to do each chapter on its own, or a couple of chapters depending on the length.


# Linux and Mac

As the program is written in python and python is included for both linux and mac. You can therefore run the program as is, though you might need some of the dependencies: 
- customtkinter 5.1.2
- PyPDF2 3.0.1
- pyttsx3 2.90<br>

Then it should work the same way as it does for windows
