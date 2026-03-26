import cv2
import numpy as np
from typing import List, Dict, Any

class ShapeDetector:
    def __init__(self):
        pass

    def detect(self, points: List[Dict[str, float]]) -> Dict[str, Any]:
        """
        Takes a list of points and uses OpenCV contour approximation 
        to detect the shape.
        """
        if not points or len(points) < 2:
            return {"type": "unknown", "x": 0, "y": 0, "width": 0, "height": 0}

        # Convert to numpy array of shape (N, 1, 2)
        pts = np.array([[p["x"], p["y"]] for p in points], dtype=np.int32)
        cnt = pts.reshape((-1, 1, 2))

        # Get bounding box
        x, y, w, h = cv2.boundingRect(cnt)

        # Basic shape metrics
        perimeter = cv2.arcLength(cnt, True) # assume closed for shape approx
        
        # If open stroke, arcLength of straight line vs true len
        # We handle line separately
        start, end = pts[0], pts[-1]
        dist = np.linalg.norm(start - end)
        path_length = sum(np.linalg.norm(pts[i] - pts[i-1]) for i in range(1, len(pts)))
        
        if path_length > 0 and dist / path_length > 0.9:
            # It's an open straight line
            return {
                "type": "line",
                "x": float(x), "y": float(y),
                "width": float(w), "height": float(h)
            }

        # Approximate polygon
        approx = cv2.approxPolyDP(cnt, 0.04 * perimeter, True)
        vertices = len(approx)

        shape_type = "unknown"

        if vertices == 3:
            shape_type = "triangle"
        elif vertices == 4:
            # Compute aspect ratio to differentiate diamond/square/rect
            # Actually, compute angle to check if diamond
            # For simplicity, we just classify as rectangle unless w/h is 1
            aspect_ratio = w / float(h) if h != 0 else 0
            # To detect diamond, check if corners are aligned with centers of bounding box
            # But the requirements just say "rectangle", "diamond"
            # It's a heuristic for this stage:
            rect_area = w * h
            contour_area = cv2.contourArea(cnt)
            if rect_area > 0 and (contour_area / rect_area) < 0.6:
                shape_type = "diamond"
            else:
                shape_type = "rectangle"

        elif vertices > 4:
            # Check circularity
            area = cv2.contourArea(cnt)
            if perimeter > 0:
                circularity = 4 * np.pi * (area / (perimeter * perimeter))
                if circularity > 0.7:
                    shape_type = "circle"
                else:
                    shape_type = "unknown"

        return {
            "type": shape_type,
            "x": float(x),
            "y": float(y),
            "width": float(w),
            "height": float(h)
        }
