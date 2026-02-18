import cv2
import numpy as np
from collections import deque


VIDEO_SOURCE = "ENTER_YOUR_VIDEO_PATH"
SMOOTHING_WINDOW = 15
OFFSET_THRESHOLD = 25
ANGLE_THRESHOLD = 3

center_buffer = deque(maxlen=SMOOTHING_WINDOW)
angle_buffer = deque(maxlen=SMOOTHING_WINDOW)


def region_of_interest(img):
    height, width = img.shape
    mask = np.zeros_like(img)

    polygon = np.array([[
        (0, height),
        (width, height),
        (width, int(height * 0.6)),
        (0, int(height * 0.6))
    ]], np.int32)

    cv2.fillPoly(mask, polygon, 255)
    return cv2.bitwise_and(img, mask)


def classify_lines(lines):
    left, right = [], []

    for line in lines:
        x1, y1, x2, y2 = line[0]

        if abs(x2 - x1) < 5:
            continue

        slope = (y2 - y1) / (x2 - x1)

        if slope < -0.4:
            left.append((x1, y1, x2, y2, slope))
        elif slope > 0.4:
            right.append((x1, y1, x2, y2, slope))

    return left, right


def average_line(lines):
    if not lines:
        return None, None

    x_vals = []
    slopes = []

    for x1, y1, x2, y2, slope in lines:
        x_vals.extend([x1, x2])
        slopes.append(slope)

    return int(np.mean(x_vals)), np.mean(slopes)



cap = cv2.VideoCapture(VIDEO_SOURCE)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (900, 600))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    edges = cv2.Canny(blur, 50, 150)
    roi = region_of_interest(edges)

    lines = cv2.HoughLinesP(
        roi,
        1,
        np.pi / 180,
        threshold=120,
        minLineLength=120,
        maxLineGap=40
    )

    frame_center = frame.shape[1] // 2

    if lines is not None:
        left_lines, right_lines = classify_lines(lines)

        left_x, left_slope = average_line(left_lines)
        right_x, right_slope = average_line(right_lines)

        if left_x and right_x:

           
            height = frame.shape[0]

            cv2.line(frame,
                     (left_x, height),
                     (left_x, int(height * 0.6)),
                     (0, 255, 255), 2)   # thinner line

            cv2.line(frame,
                     (right_x, height),
                     (right_x, int(height * 0.6)),
                     (0, 255, 255), 2)   # thinner line

            runway_center = (left_x + right_x) // 2
            avg_slope = (left_slope + right_slope) / 2
            angle = np.degrees(np.arctan(avg_slope))

            center_buffer.append(runway_center)
            angle_buffer.append(angle)

            smoothed_center = int(np.mean(center_buffer))
            smoothed_angle = np.mean(angle_buffer)

            deviation = smoothed_center - frame_center

           
            if abs(deviation) < OFFSET_THRESHOLD and abs(smoothed_angle) < ANGLE_THRESHOLD:
                status = "ALIGNED"
                color = (0, 255, 0)
            elif deviation > OFFSET_THRESHOLD:
                status = "SLIGHT RIGHT"
                color = (0, 0, 255)
            elif deviation < -OFFSET_THRESHOLD:
                status = "SLIGHT LEFT"
                color = (0, 0, 255)
            else:
                status = "MISALIGNED"
                color = (0, 0, 255)

            cv2.line(frame,
                     (smoothed_center, 0),
                     (smoothed_center, height),
                     (255, 0, 0), 1)

            cv2.line(frame,
                     (frame_center, 0),
                     (frame_center, height),
                     (0, 0, 255), 1)

            cv2.putText(frame,
                        f"Deviation: {int(deviation)} px",
                        (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (0, 0, 255), 2)

            cv2.putText(frame,
                        f"Angle: {smoothed_angle:.2f} deg",
                        (20, 80),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (0, 0, 255), 2)

            cv2.putText(frame,
                        status,
                        (20, 130),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.2, color, 3)

    cv2.imshow("Runway Alignment Decision System", frame)
    cv2.imshow("Edges", roi)

    if cv2.waitKey(30) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
