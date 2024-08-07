## File_management

### Objective
This Python script automatically organizes downloaded files in your Downloads folder, moving them to designated subfolders based on their file type. It utilizes the watchdog library to monitor the Downloads folder for changes and triggers file movement upon detection.

### Skills Learned
* File system manipulation with Python (os module, shutil module)
* File extension identification for sorting
* Working with file paths and directories
* Event-driven programming using the watchdog library
* Basic logging for tracking file movement

### Tools Used
* Python
* os module
* shutil module
* watchdog library
* logging module

You can install them using pip:

```bash
pip install watchdog logging
```
### Steps

#### 1) Create Destination Folders:
   - Create one folder for each one of the next:
     - Sound
     - Music
     - Video
     - Image
     - Excels
     - PDF
     - Word
     - add more if needed

#### 2) Change folder paths in the code
  ```python
  source_dir = r"Change this path to your Downloads folder"
  dest_dir_sfx = r"Change this path to your desired Sound folder"
  dest_dir_music = r"Change this path to your desired Music folder"
  dest_dir_video = r"Change this path to your desired Video folder"
  dest_dir_image = r"Change this path to your desired Image folder"
  dest_dir_excel = r"Change this path to your desired Excel folder"
  dest_dir_pdf = r"Change this path to your desired PDF folder"
  dest_dir_word = r"Change this path to your desired Word folder"
  ```

#### 2) Run the script:
   - Execute the Python script
   - The script will start monitoring your Downloads folder
   - As new files are added or modified, the script will automatically move them to the appropriate   destination folder based on their file type.
   
