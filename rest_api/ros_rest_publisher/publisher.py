import requests
import json
import base64
import time
from typing import Dict, Any

class ROSRestPublisher:
    def __init__(self, api_url: str = "http://localhost:8000"):
        self.api_url = api_url

    def publish_sensor_data(self, sensor_id: str, value: float, unit: str) -> Dict[str, Any]:
        """Publish sensor data to REST API"""
        data = {
            "sensor_id": sensor_id,
            "value": value,
            "unit": unit
        }
        response = requests.post(f"{self.api_url}/sensor_data", json=data)
        return response.json()

    def publish_robot_pose(self, x: float, y: float, z: float, orientation: float) -> Dict[str, Any]:
        """Publish robot pose to REST API"""
        data = {
            "x": x,
            "y": y,
            "z": z,
            "orientation": orientation
        }
        response = requests.post(f"{self.api_url}/robot_pose", json=data)
        return response.json()

    def publish_image_data(self, width: int, height: int, encoding: str, raw_data: bytes) -> Dict[str, Any]:
        """Publish image data to REST API"""
        data = {
            "width": width,
            "height": height,
            "encoding": encoding,
            "data": base64.b64encode(raw_data).decode('utf-8')
        }
        response = requests.post(f"{self.api_url}/image_data", json=data)
        return response.json()

def main():
    publisher = ROSRestPublisher()
    
    # Example: Publishing different types of data
    try:
        # Publish sensor data
        result = publisher.publish_sensor_data("temperature_1", 25.5, "celsius")
        print("Published sensor data:", result)

        # Publish robot pose
        result = publisher.publish_robot_pose(1.0, 2.0, 0.0, 90.0)
        print("Published robot pose:", result)

        # Publish dummy image data
        dummy_image = b"dummy_image_data"
        result = publisher.publish_image_data(640, 480, "rgb8", dummy_image)
        print("Published image data:", result)

    except requests.exceptions.RequestException as e:
        print(f"Error publishing data: {e}")

if __name__ == "__main__":
    main()
