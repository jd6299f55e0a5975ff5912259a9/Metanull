# **META NULL**

Meta Null is a professional tool designed to completely remove all identifiable metadata from images and disrupt steganography patterns. It keeps your images private and untraceable, even against advanced forensic analysis.

---

## **How to Use**

### 1. **Install Python**
   - Download and install Python (version 3.8 or higher) from [python.org](https://www.python.org/).

### 2. **Install Required Dependencies**
   - Open a terminal or command prompt and run:
     ```bash
     pip install pillow piexif PyQt6
     ```
     This will install:
     - **Pillow**: For image processing  
     - **Piexif**: For metadata handling  
     - **PyQt6**: For the graphical user interface  

### 3. **Clone the Repository**
   - In your terminal, run:
     ```bash
     git clone https://github.com/jd6299f55e0a5975ff5912259a9/metanull
     cd metanull
     ```

### 4. **Run the Application**
   - Start the app with:
     ```bash
     python metanull.py
     ```

### 5. **Using the Application**
   - Click **Select Image** to load an image file.  
   - Click **Forensic Analysis** to inspect existing metadata.  
   - Configure sanitization options:  
     - Choose output format (JPEG, WebP, PNG)  
     - Adjust quality level  
     - Enable pixel alteration and timestamp randomization if desired  
   - Click **SANITIZE IMAGE** to create a clean version of the image.  
   - Save the sanitized image to your desired location.  

---

## **Features**
- Complete removal of metadata: EXIF, GPS, XMP, IPTC, ICC profiles, thumbnails  
- Pixel-level image reconstruction (new image created from raw pixels)  
- Anti-forensic methods including random pixel alteration and timestamp randomization  
- Supports saving images as JPEG, WebP, or PNG  
- Quality settings adjustable for compression  
- Forensic metadata inspection before cleaning  

---

## **Important Notes**
- This tool is intended for legitimate privacy protection.  
- Use responsibly and in compliance with local laws.  
- Always keep backups of your original images before sanitizing.  

---

## **Credits**
If you have any questions or need further assistance, feel free to ask me on my Discord: 
- **Discord Username**: jd6299f55e0a5975ff5912259a9
- **Discord ID**: 1068729811578650754
