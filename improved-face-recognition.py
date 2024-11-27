import streamlit as st
import cv2
from simple_facerec import SimpleFacerec
from Attendance import AttendanceSystem
import numpy as np
import pandas as pd
import time
import tempfile
import os

class EnhancedFaceRecognition(SimpleFacerec):
    def __init__(self, confidence_threshold=0.6):
        super().__init__()
        self.confidence_threshold = confidence_threshold
    
    def detect_known_faces(self, frame):
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        
        face_names = []
        face_confidences = []
        
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            
            if len(face_distances) > 0:
                confidence = 1 - min(face_distances)  # Convert distance to confidence
                best_match_index = np.argmin(face_distances)
                
                if confidence >= self.confidence_threshold and matches[best_match_index]:
                    name = self.known_face_names[best_match_index]
                else:
                    name = "Unknown"
                    
                face_names.append(name)
                face_confidences.append(confidence)
            
        return face_locations, face_names, face_confidences

def draw_face_info(frame, face_loc, name, confidence, is_marked):
    y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
    
    # Determine color based on recognition status and marking
    if name == "Unknown":
        color = (0, 0, 255)  # Red
    elif is_marked:
        color = (0, 255, 0)  # Green for marked attendance
    else:
        # Yellow for recognized but not marked
        color = (0, 255, 255)
    
    # Draw rectangle around face
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 4)
    
    # Create info text with name and confidence
    if name != "Unknown":
        status_text = "✓" if is_marked else "..."
        info_text = f"{name} ({confidence:.1%}) {status_text}"
    else:
        info_text = "Unknown"
    
    # Add background for text
    text_size = cv2.getTextSize(info_text, cv2.FONT_HERSHEY_DUPLEX, 0.8, 2)[0]
    cv2.rectangle(frame, (x1, y1 - text_size[1] - 10), (x1 + text_size[0], y1), color, -1)
    
    # Draw text
    cv2.putText(frame, info_text, (x1, y1 - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 2)

def draw_emoji(frame, x1, y1, x2, y2, emoji_type):
    emoji_size = min(x2 - x1, y2 - y1) // 2
    emoji_x = x1 + (x2 - x1) // 2 - emoji_size // 2
    emoji_y = y1 - emoji_size - 10

    if emoji_type == 'success':
        cv2.line(frame, (emoji_x, emoji_y + emoji_size // 2), 
                 (emoji_x + emoji_size // 3, emoji_y + emoji_size), 
                 (0, 255, 0), 3)
        cv2.line(frame, (emoji_x + emoji_size // 3, emoji_y + emoji_size), 
                 (emoji_x + emoji_size, emoji_y), 
                 (0, 255, 0), 3)
    elif emoji_type == 'waiting':
        cv2.circle(frame, (emoji_x + emoji_size // 2, emoji_y + emoji_size // 2), 
                  emoji_size // 3, (0, 255, 255), 2)

def main():
    st.title("🔍 Enhanced Face Recognition Attendance System")
    st.sidebar.header("System Configuration")
    
    # Configuration options
    image_path = st.sidebar.text_input("Path to Face Images", r"C:\Users\MBR\Downloads\faceee\images")
    camera_index = st.sidebar.selectbox("Select Camera", [0, 1, 2], index=0)
    attendance_interval = st.sidebar.slider("Attendance Interval (seconds)", min_value=10, max_value=120, value=30)
    confidence_threshold = st.sidebar.slider("Recognition Confidence Threshold", min_value=0.4, max_value=0.9, value=0.6)
    
    # Initialize system
    if 'attendance_system' not in st.session_state:
        st.session_state.attendance_system = AttendanceSystem()
        st.session_state.attendance_status = {}
    
    # UI elements
    start_camera = st.sidebar.button("Start Attendance")
    stop_camera = st.sidebar.button("Stop Attendance")
    frame_placeholder = st.empty()
    attendance_placeholder = st.empty()
    
    if start_camera:
        # Initialize enhanced face recognition
        sfr = EnhancedFaceRecognition(confidence_threshold=confidence_threshold)
        sfr.load_encoding_images(image_path)
        
        cap = cv2.VideoCapture(camera_index)
        
        while start_camera and not stop_camera:
            ret, frame = cap.read()
            if not ret:
                st.warning("Failed to capture frame")
                break
            
            current_time = time.time()
            face_locations, face_names, face_confidences = sfr.detect_known_faces(frame)
            
            for face_loc, name, confidence in zip(face_locations, face_names, face_confidences):
                is_marked = False
                can_mark = False
                
                if name != "Unknown":
                    # Initialize status for new faces
                    if name not in st.session_state.attendance_status:
                        st.session_state.attendance_status[name] = {
                            "marked": False,
                            "last_time": 0,
                            "wait_start": current_time
                        }
                    
                    status = st.session_state.attendance_status[name]
                    time_since_last = current_time - status["last_time"]
                    
                    # Check if attendance can be marked
                    if not status["marked"] or time_since_last >= attendance_interval:
                        can_mark = True
                    
                    # Mark attendance if enough time has passed
                    if can_mark:
                        st.session_state.attendance_system.mark_attendance(name)
                        status["marked"] = True
                        status["last_time"] = current_time
                        status["wait_start"] = current_time
                        is_marked = True
                    elif time_since_last < attendance_interval:
                        is_marked = True  # Show as marked if within interval
                
                # Draw face information
                draw_face_info(frame, face_loc, name, confidence, is_marked)
                
                # Draw emoji based on status
                if name != "Unknown":
                    if is_marked and (current_time - status["wait_start"]) < 2:
                        draw_emoji(frame, face_loc[3], face_loc[0], face_loc[1], face_loc[2], 'success')
                    elif can_mark:
                        draw_emoji(frame, face_loc[3], face_loc[0], face_loc[1], face_loc[2], 'waiting')
            
            # Display frame and attendance
            frame_placeholder.image(frame, channels="BGR", use_column_width=True)
            if st.session_state.attendance_system.attendance_data:
                attendance_df = pd.DataFrame(st.session_state.attendance_system.attendance_data)
                attendance_placeholder.dataframe(attendance_df)
        
        if 'cap' in locals():
            cap.release()
    
    # Download attendance data
    if st.sidebar.button("Download Attendance CSV"):
        if st.session_state.attendance_system.attendance_data:
            df = pd.DataFrame(st.session_state.attendance_system.attendance_data)
            csv = df.to_csv(index=False)
            st.sidebar.download_button(
                label="Click to Download Attendance",
                data=csv,
                file_name="attendance_record.csv",
                mime="text/csv",
            )
        else:
            st.sidebar.warning("No attendance data available")

if __name__ == "__main__":
    main()
