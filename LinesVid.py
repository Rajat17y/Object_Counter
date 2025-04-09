import cv2

def get_line_coordinates(video_path=None):
    """
    Launches an OpenCV window to draw a line on a video or webcam.
    
    Parameters:
        video_path (str or int): File path of the video or webcam index (default is 0 for webcam).
    
    Returns:
        list: Coordinates [x1, y1, x2, y2] of the drawn line when Enter is pressed.
              Returns [] if exited without drawing.
    """
    drawing = False
    paused = False
    start_point = (-1, -1)
    end_point = (-1, -1)
    current_mouse_pos = (-1, -1)
    lines = []

    def draw_line(event, x, y, flags, param):
        nonlocal drawing, start_point, current_mouse_pos, end_point

        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            start_point = (x, y)

        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing:
                current_mouse_pos = (x, y)

        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            end_point = (x, y)
            lines.append((start_point, end_point))
            print(f"Line drawn from {start_point} to {end_point}")

    if video_path is None:
        video_path = 0  # Default to webcam

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error opening video source.")
        return []

    cv2.namedWindow("Video")
    cv2.setMouseCallback("Video", draw_line)

    frame = None

    while cap.isOpened():
        if not paused:
            ret, frame = cap.read()
            if not ret:
                break

        temp_frame = frame.copy()

        # Draw stored lines
        for line in lines:
            cv2.line(temp_frame, line[0], line[1], (0, 0, 255), 2)

        # Draw current preview line
        if drawing and start_point != (-1, -1):
            cv2.line(temp_frame, start_point, current_mouse_pos, (0, 255, 0), 1)

        cv2.imshow("Video", temp_frame)

        key = cv2.waitKey(30) & 0xFF
        if key == 27 or key == ord('q'):
            break
        elif key == 32:  # Space to pause
            paused = not paused
        elif key == 13:  # Enter key
            cap.release()
            cv2.destroyAllWindows()
            if lines:
                last_line = lines[-1]
                return [last_line[0][0], last_line[0][1], last_line[1][0], last_line[1][1]]
            else:
                return []

    cap.release()
    cv2.destroyAllWindows()
    return []
