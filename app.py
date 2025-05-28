import tkinter as tk





window = tk.Tk()
window.title("Simple GUI Application")

frame = tk.Frame(window)
frame.pack()


# saving user information
user_info_frame = tk.LabelFrame(frame, text="User Information")
user_info_frame.grid(row = 0 , column = 0)

first_name_label = tk.Label(user_info_frame, text="First Name:")
first_name_label.grid(row=0, column=0)
last_name_label = tk.Label(user_info_frame, text="Last Name:")
last_name_label.grid(row=0, column=1)


window.mainloop()