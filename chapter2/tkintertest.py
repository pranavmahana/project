import tkinter as tk

def main():
    # Create the main window
    root = tk.Tk()

    # Set the title of the window
    root.title("My Tkinter Window")

    # Set the size of the window (width x height)
    root.geometry("400x300")

    # Create a label widget
    label = tk.Label(root, text="Hello, Tkinter!")

    # Pack the label widget into the window
    label.pack(pady=20)

    # Create a button widget
    button = tk.Button(root, text="Click Me", command=on_button_click)

    # Pack the button widget into the window
    button.pack()

    # Start the Tkinter event loop
    root.mainloop()

def on_button_click():
    print("Button clicked!")

if __name__ == "__main__":
    main()
