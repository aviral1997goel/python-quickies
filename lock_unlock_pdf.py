import os
from PyPDF2 import PdfReader, PdfWriter

# Function to unlock a PDF file
def unlock_pdf(locked_path, unlocked_path, password):
    with open(locked_path, "rb") as locked_file:
        reader = PdfReader(locked_file)
        
        if reader.is_encrypted:
            try:
                reader.decrypt(password)
                
                writer = PdfWriter()
                for page_num in range(len(reader.pages)):
                    writer.add_page(reader.pages[page_num])

                with open(unlocked_path, "wb") as unlocked_file:
                    writer.write(unlocked_file)

                print(f"Unlocked PDF saved as: {unlocked_path}")
            except Exception as e:
                print(f"Failed to unlock {locked_path}: {e}")
        else:
            print(f"{locked_path} is not encrypted.")

# Get input and output directories from the user
locked_dir = input("Enter the path for the locked PDF files: ")
unlocked_dir = input("Enter the path for the unlocked PDF files: ")

# Ensure the output directory exists
os.makedirs(unlocked_dir, exist_ok=True)

# Ask if all files have the same password
same_password = input("Do all PDF files have the same password? (yes/no): ").strip().lower()

# If all files have the same password, ask for it once
if same_password == "yes":
    password = input("Enter the password for the PDF files: ")

# Process each PDF in the locked directory
for filename in os.listdir(locked_dir):
    if filename.endswith(".pdf") or filename.endswith(".PDF"):
        locked_path = os.path.join(locked_dir, filename)
        unlocked_path = os.path.join(unlocked_dir, filename)

        if same_password == "yes":
            unlock_pdf(locked_path, unlocked_path, password)
        else:
            password = input(f"Enter the password for {filename}: ")
            unlock_pdf(locked_path, unlocked_path, password)

print("All PDFs processed.")