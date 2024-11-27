# Face Recognition Attendance System 🔍
A modern, real-time attendance tracking system using facial recognition technology, built with **Streamlit** and **OpenCV**. This system allows for automated attendance marking through webcam face detection and recognition.

## 📸 Application Screenshot
Here is a preview of the application interface:

![Attendance System Screenshot](https://github.com/mahmouddbelo/Attendance_system_using_face_recognition/blob/main/test%20%C2%B7%20Streamlit%20-%20Google%20Chrome%2011_26_2024%2011_51_46%20PM.png)


## 🌟 Features
- Real-time face detection and recognition
- Automatic attendance marking with customizable intervals
- Visual feedback with emoji indicators
- Downloadable attendance records in CSV format
- Support for multiple camera inputs
- User-friendly interface with **Streamlit**
- Configurable attendance marking intervals
- Status indicators for successful recognition

## 🛠️ Installation

### 1. Clone the repository:
```bash
git clone https://github.com/mahmoudbelo/attendance_system_using_face_recognition.git
cd attendance_system_using_face_recognition
```
### 2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```
### 3. Install required system packages (Linux/Ubuntu):
```bash
sudo apt-get update
sudo apt-get install build-essential cmake libopenblas-dev liblapack-dev libx11-dev libgl1-mesa-glx

```
### 4. Install Python dependencies:
```bash
pip install -r requirements.txt
```
📁 Project Structure
```bash
attendance_system_using_face_recognition/
├── test.py                     # Main Streamlit application
├── simple_facerec.py          # Face recognition utility class
├── Attendance.py              # Attendance system class
├── requirements.txt           # Python dependencies
├── images                    # Directory for face images
└── README.md                  # Project documentation
```
## 🚀 Usage
### 1. Add face images:
Create an images directory in the project root
Add clear, front-facing photos of individuals
Name the images with the person's name (e.g., john_doe.jpg)

### 2. Run the application:
```bash
streamlit run test.py
```
### 3. In the application:
Set the path to your images directory
Select your camera device
Set the attendance interval
Click "Start Attendance" to begin recognition
Download attendance records using the "Download Attendance CSV" button
## ⚙️Configuration
The system offers several configurable parameters through the Streamlit sidebar:
Image Path: Directory containing face images
Camera Selection: Choose between available cameras (0, 1, 2)
Attendance Interval: Set the time between attendance marks (10-120 seconds)
## 📊 Attendance Records
The system generates attendance records with the following information:
Name of the person
Timestamp of recognition
Attendance status
Download option in CSV format
## 🌈 Status Indicators
The system uses visual indicators to show recognition status:

🟢 Green: Successful recognition and attendance marked
⚪ White: Known face, waiting for interval
🔴 Red: Unknown face
## 🔧 Dependencies
#### Main requirements:
```bash
streamlit
opencv-python
numpy
pandas
face-recognition
dlib
```
See requirements.txt for the complete list.

## 🐛 Troubleshooting
Common issues and solutions:
Camera not working:

Check camera index (try 0, 1, or 2)
Verify camera permissions
Face not recognized:

Ensure good lighting
Use clear, front-facing photos
Check image path configuration
Installation issues:

Install system dependencies first
Use a virtual environment
Check Python version compatibility
## 🤝 Contributing
We welcome contributions to improve this project! Please follow these steps to contribute:

## Fork the repository
Create your feature branch: git checkout -b feature/YourFeature
Commit your changes: git commit -m 'Add YourFeature'
Push to the branch: git push origin feature/YourFeature
Open a Pull Request to the main repository
## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments
OpenCV team for computer vision capabilities
Streamlit team for the amazing web framework
Face Recognition library developers




