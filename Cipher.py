import tkinter as tk
from tkinter import ttk, messagebox

class Cipher:
    def __init__(self, root):  # Corrected constructor
        self.root = root
        self.root.title("Secret Message Wizard")  
        self.root.state('zoomed')  # Start with the window maximized
        root.resizable(False, False)  # Prevent resizing 

        self.colors = {
            'wave': '#0047AB',        # Deep ocean blue for the background
            'foam': '#B0E0E6',        # Light sea foam for frames
            'sand': '#F5F5DC',        # Beige for text areas
            'sunset': '#FFA07A',      # Sunset orange for buttons
            'coral': '#FF6B6B'        # Coral red for hover effects
        }

        # Set the main window's background color
        self.root.config(bg=self.colors['wave'])
        
        # Create the main interface for the cipher
        self.create_cipher_canvas()
        
        # Initialize the characters we will use for encryption/decryption
        self.initialize_characters()
        
        # Show a welcome message to the user
        self.show_welcome()
        
    def initialize_characters(self):
        """Define the characters for our cipher (A-Z, a-z, 0-9)"""
        self.LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.digits = '0123456789'
        self.all_chars = self.LETTERS + self.LETTERS.lower() + self.digits

    def create_cipher_canvas(self):
        """Create the main layout for the cipher application"""
        
        # Main container 
        main_frame = tk.Frame(
            self.root,
            bg=self.colors['wave'],
            padx=20,
            pady=20
        )
        main_frame.pack(expand=True, fill='both')
        
        # Title label 
        title = tk.Label(
            main_frame,
            text="🔐 Secret Message Wizard",
            font=('Arial Black', 24),
            fg='white',
            bg=self.colors['wave']
        )
        title.pack(pady=(0, 20))

        # Frame for user message input
        msg_frame = tk.LabelFrame(
            main_frame,
            text=" Your Hidden Message ",
            font=('Arial', 12, 'italic'),
            bg=self.colors['wave'],
            fg='white',
            bd=3,
            relief='ridge'
        )
        msg_frame.pack(fill='x', pady=5)
        
        # Text box for message input 
        self.message_box = tk.Text(
            msg_frame,
            height=8,
            width=60,
            bg=self.colors['sand'],
            wrap='word',
            font=('Courier New', 12),
            padx=10,
            pady=10
        )
        self.message_box.pack(padx=10, pady=5)
        
        # Frame for input controls (shift value and buttons)
        control_frame = tk.Frame(
            main_frame,
            bg=self.colors['wave']
        )
        control_frame.pack(fill='x', pady=10)
        
        # Label for the shift value
        tk.Label(
            control_frame,
            text="Cipher Shift:",
            font=('Arial', 12),
            bg=self.colors['wave'],
            fg='white'
        ).pack(side='left', padx=5)
        
        # Entry box for the user to input the shift value
        self.shift_entry = ttk.Entry(
            control_frame,
            width=5,
            font=('Arial', 12)
        )
        self.shift_entry.pack(side='left', padx=5)
        self.shift_entry.insert(0, "3")  # Default shift value

        # Buttons for encrypting and decrypting messages
        self.encrypt_button = ttk.Button(
            control_frame,
            text="Encrypt",
            command=self.encrypt_message,
            style="TButton"
        )
        self.encrypt_button.pack(side='left', padx=5)

        self.decrypt_button = ttk.Button(
            control_frame,
            text="Decrypt",
            command=self.decrypt_message,
            style="TButton"
        )
        self.decrypt_button.pack(side='left', padx=5)

        # Style for the buttons
        s = ttk.Style()
        s.configure("TButton", background=self.colors['sunset'], foreground='white', font=('Arial', 12, 'bold'))
        s.map("TButton", background=[('active', self.colors['coral'])])

        # Frame for displaying results
        result_frame = tk.LabelFrame(
            main_frame,
            text=" Result ",
            font=('Arial', 12, 'italic'),
            bg=self.colors['wave'],
            fg='white',
            bd=3,
            relief='ridge'
        )
        result_frame.pack(fill='x', pady=5)

        # Text box for displaying the result 
        self.result_box = tk.Text(
            result_frame,
            height=8,
            width=60,
            bg=self.colors['sand'],
            wrap='word',
            font=('Courier New', 12),
            padx=10,
            pady=10,
            state=tk.DISABLED
        )
        self.result_box.pack(padx=10, pady=5)

    def encrypt_message(self):
        """Encrypt the message using the Caesar cipher"""
        message = self.message_box.get("1.0", tk.END).strip()  # Get the message from the text box
        shift = self.get_shift_value()  # Get the shift value from the entry box
        
        if message:  # Check if the message is not empty
            encrypted_message = self.caesar_cipher(message, shift, "encrypt")  # Encrypt the message
            self.display_result(encrypted_message)  # Show the result
        else:
            messagebox.showwarning("Input Required", "Please enter a message to encrypt.")  # Alert if empty

    def decrypt_message(self):
        """Decrypt the message using the Caesar cipher"""
        message = self.message_box.get("1.0", tk.END).strip()  # Get the message from the text box
        shift = self.get_shift_value()  # Get the shift value from the entry box
        
        if message:  # Check if the message is not empty
            decrypted_message = self.caesar_cipher(message, shift, "decrypt")  # Decrypt the message
            self.display_result(decrypted_message)  # Show the result
        else:
            messagebox.showwarning("Input Required", "Please enter a message to decrypt.")  # Alert if empty

    def get_shift_value(self):
        """Retrieve and validate the shift value from the entry box"""
        try:
            return int(self.shift_entry.get())  # Convert the shift value to an integer
        except ValueError:
            messagebox.showerror("Invalid Input", "Shift value must be an integer.")  # Alert if invalid
            return 0  # Default to 0 if invalid

    def caesar_cipher(self, text, shift, mode):
        """Perform the Caesar cipher encryption or decryption"""
        result = ""
        
        # Adjust shift for decryption
        if mode == "decrypt":
            shift = -shift

        for char in text:
            if char in self.all_chars:  # Check if the character is in our defined set
                # Find the new character after shifting
                new_index = (self.all_chars.index(char) + shift) % len(self.all_chars)
                result += self.all_chars[new_index]  # Append the new character to the result
            else:
                result += char  # Non-alphabetic characters remain unchanged
        return result

    def display_result(self, text):
        """Display the result in the result box"""
        self.result_box.config(state=tk.NORMAL)  # Enable editing to insert text
        self.result_box.delete(1.0, tk.END)  # Clear previous results
        self.result_box.insert(tk.END, text)  # Insert the new result
        self.result_box.config(state=tk.DISABLED)  # Disable editing again

    def show_welcome(self):
        """Display a welcome message to the user"""
        messagebox.showinfo("Welcome!", "Welcome to the Secret Message Wizard!\n"
                                          "Use this tool to encrypt and decrypt your messages with ease.")

if __name__ == "__main__":  # Corrected main check
    root = tk.Tk()
    app = Cipher(root)  
    root.mainloop()  # Start the Tkinter event loop
