import cv2
import mediapipe as mp
import numpy as np
import time

# --- CONFIGURATION ---
SLOUCH_THRESHOLD = 35  # Degrees
SLOUCH_TOLERANCE = 15  # Frames to wait before fogging

# --- 1. THE MATH BRAIN ---
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle > 180.0:
        angle = 360-angle
        
    return angle

# --- 2. MAIN LOOP ---
def main():
    # Setup AI
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    mp_drawing = mp.solutions.drawing_utils
    
    # Setup Camera
    cap = cv2.VideoCapture(0)
    
    # Get screen size (for the fog)
    # We will just make the fog huge to cover everything
    
    slouch_frames = 0 
    fog_active = False

    print("VerteBro Started! Press 'q' to quit.")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break

        # 1. Process Image
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        current_status = "GOOD"
        color = (0, 255, 0) # Green
        
        # 2. Check Posture
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            h, w, _ = frame.shape
            
            # Coordinates
            shoulder = [landmarks[11].x * w, landmarks[11].y * h]
            ear = [landmarks[7].x * w, landmarks[7].y * h]
            vertical_point = [shoulder[0], shoulder[1] - 100]
            
            # Math
            angle = calculate_angle(vertical_point, shoulder, ear)
            
            # Logic
            if angle > SLOUCH_THRESHOLD:
                slouch_frames += 1
                color = (0, 0, 255) # Red
                current_status = f"SLOUCHING ({int(angle)}d)"
            else:
                slouch_frames = 0
                current_status = "GOOD"
                
            # Draw Skeleton
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            cv2.putText(image, str(int(angle)), tuple(np.array(shoulder).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        # 3. THE FOG LOGIC (Mac Safe Version)
        if slouch_frames > SLOUCH_TOLERANCE:
            # Create a giant grey image
            fog_image = np.zeros((1080, 1920, 3), np.uint8) + 50 # Dark Grey
            
            # Add Text
            cv2.putText(fog_image, "DON'T BE A SHRIMP!", (200, 400), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 5)
            cv2.putText(fog_image, "SIT UP TO CONTINUE", (300, 550), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
            
            # Show Fullscreen Fog
            cv2.namedWindow('FOG', cv2.WINDOW_NORMAL)
            cv2.setWindowProperty('FOG', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.imshow('FOG', fog_image)
            fog_active = True
        else:
            # Close the fog window if it's open
            if fog_active:
                try:
                    cv2.destroyWindow('FOG')
                    fog_active = False
                except:
                    pass

        # Show Normal Camera
        cv2.putText(image, f"Status: {current_status}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        cv2.imshow('VerteBro Cam', image)
        
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()