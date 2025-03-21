import customtkinter as ctk

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')

root = ctk.CTk()
root.title("Degree Project")
root.geometry("900x506+0+0")
root.resizable(width=False, height=False)
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

layoutFrame = ctk.CTkFrame(master=root)
layoutFrame.grid(row=0,column=0, sticky='nsew')
layoutFrame.grid_columnconfigure(0, weight=1)
layoutFrame.grid_rowconfigure(1, weight=1)

headerLabel = ctk.CTkLabel(master=layoutFrame, text="Aesthetic Recognition System",font=("",30))
headerLabel.grid(row=0, column=0, padx=5, pady=15, sticky='w')

# Two cols layout
twoColsFrame = ctk.CTkFrame(master=layoutFrame)
twoColsFrame.grid(row=1, column=0, padx=5, pady=5,sticky='nsew')
twoColsFrame.grid_columnconfigure(0, weight=3)
twoColsFrame.grid_columnconfigure(1, weight=1)
twoColsFrame.grid_rowconfigure(0, weight=1)

# Left col frame
leftColFrame = ctk.CTkFrame(master=twoColsFrame)
leftColFrame.grid(row=0,column=0, padx=5, pady=5, sticky='nsew')
leftColFrame.grid_rowconfigure(0, weight=1)
leftColFrame.grid_columnconfigure(0,weight=1)

# placeholder Left
phLeft = ctk.CTkLabel(master=leftColFrame, text="CAMERA INPUT", font=("",25))
phLeft.grid(row=0, column=0, padx=5, pady=5,sticky='nsew')



# Left col END

rightColFrame = ctk.CTkFrame(master=twoColsFrame)
rightColFrame.grid(row=0,column=1,padx=5, pady=5, sticky='nsew')
rightColFrame.grid_columnconfigure(0, weight=1)
rightColFrame.grid_rowconfigure(0, weight=2)

lastPictureFrame = ctk.CTkFrame(master=rightColFrame)
lastPictureFrame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
lastPictureFrame.grid_rowconfigure(0, weight=1)
lastPictureFrame.grid_columnconfigure(0,weight=1)

#placeholder last picture
phLastPicture = ctk.CTkLabel(master=lastPictureFrame, text="Last Picture", font=("", 20))
phLastPicture.grid(row=0, column=0, sticky='nsew')

analysisLabel = ctk.CTkLabel(master=rightColFrame, text="Analysis summary", font=("", 16))
analysisLabel.grid(row=1,column=0, padx=5, pady=5, sticky='w')

analysisPh = ctk.CTkTextbox(master=rightColFrame, font=("",12), height=100)
analysisPh.insert('0.0', "Lorem ipsum its just a placeholder for visualization of text inside applications, journals, reports and others.")
analysisPh.configure(state='disabled')

analysisPh.grid(row=2,column=0, padx=5, pady=5,sticky='nsew')
# Two cols END

# Buttons Row
btnRow = ctk.CTkFrame(master=layoutFrame)
btnRow.grid(row=2, column=0, padx=5, pady=5, sticky='we')
btnRow.grid_columnconfigure((0,1,2), weight=1)

btnMakePic = ctk.CTkButton(master=btnRow, text="take picture", command=lambda x: x)
btnMakePic.grid(row=0, column=0, padx=5, pady=5)

btnClear = ctk.CTkButton(master=btnRow, text="clear", command=lambda x: x)
btnClear.grid(row=0, column=1, padx=5, pady=5)

btnSave = ctk.CTkButton(master=btnRow, text="save results", command=lambda x: x)
btnSave.grid(row=0, column=2, padx=5, pady=15)

root.protocol("WM_WINDOW_DELETE", lambda x: root.destroy())

root.mainloop()