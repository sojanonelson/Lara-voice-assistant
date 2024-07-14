import cv2
import face_recognition
import numpy as np
import os

def capture_and_save_image(video_capture, save_path):
    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to grab frame.")
            break

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('c'):
            # Save the captured image
            cv2.imwrite(save_path, frame)
            print(f"Face captured and saved as {save_path}")
            break

    cv2.destroyAllWindows()

def face_capture_and_recognition():
    # Initialize video capture
    video_capture = cv2.VideoCapture(0)

    if not video_capture.isOpened():
        print("Error: Could not open video device.")
        return

    # Define the path to save the captured image
    save_path = "data/security/face_lock/face.jpg"

    # Ensure the directory exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # Capture and save an image
    capture_and_save_image(video_capture, save_path)

    # Load known faces and their names
    known_face_encodings = []
    known_face_names = []

    try:
        # Load the known face image
        known_image = face_recognition.load_image_file(save_path)
        known_encoding = face_recognition.face_encodings(known_image)[0]
        known_face_encodings.append(known_encoding)
        known_face_names.append("Your Name")  # Replace with the actual name
    except IndexError:
        print("No face found in the captured image.")
        return
    except FileNotFoundError:
        print("Captured face image file not found.")
        return

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to grab frame.")
            break

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = frame[:, :, ::-1]

        # Find all face locations and face encodings in the current frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        message = "No face found"
        if face_encodings:
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # Compare the face with known faces
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # Find the best match
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                # Draw rectangle around the face and display the name
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

                message = "Face found"
        else:
            message = "No face found"

        # Display the message on the frame
        cv2.putText(frame, message, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # Display the resulting frame
        cv2.imshow('Video', frame)

        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture and close windows
    video_capture.release()
    cv2.destroyAllWindows()

# Call the function to start face capture and recognition
face_capture_and_recognition()
