from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Union, List
import uvicorn

app = FastAPI(
    title="ROS-Python Communication Bridge",
    description="A bridge for communication between ROS and Python applications using REST API",
    version="1.0.0"
)

# Data models for different types
class SensorData(BaseModel):
    sensor_id: str
    value: float
    unit: str

class RobotPose(BaseModel):
    x: float
    y: float
    z: float
    orientation: float

class ImageData(BaseModel):
    width: int
    height: int
    encoding: str
    data: str  # Base64 encoded image data

# Store for different data types
sensor_data_store = []
robot_poses = []
image_data_store = []

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ROS-Python Communication Bridge</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                line-height: 1.6;
            }
            .container {
                background-color: #f5f5f5;
                border-radius: 8px;
                padding: 20px;
                margin: 20px 0;
            }
            h1 {
                color: #2c3e50;
                border-bottom: 2px solid #3498db;
                padding-bottom: 10px;
            }
            h2 {
                color: #3498db;
            }
            .endpoint {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 15px;
                margin: 10px 0;
            }
            .method {
                display: inline-block;
                padding: 5px 10px;
                border-radius: 4px;
                font-weight: bold;
                margin-right: 10px;
            }
            .get {
                background-color: #2ecc71;
                color: white;
            }
            .post {
                background-color: #3498db;
                color: white;
            }
            code {
                background-color: #f8f9fa;
                padding: 2px 5px;
                border-radius: 3px;
                font-family: monospace;
            }
            .links {
                margin-top: 20px;
            }
            .button {
                display: inline-block;
                padding: 10px 20px;
                background-color: #3498db;
                color: white;
                text-decoration: none;
                border-radius: 4px;
                margin-right: 10px;
            }
            .button:hover {
                background-color: #2980b9;
            }
        </style>
    </head>
    <body>
        <h1>ROS-Python Communication Bridge</h1>
        
        <div class="container">
            <h2>About</h2>
            <p>This project demonstrates communication between ROS and Python applications using REST API. 
            It supports multiple data types and provides bidirectional communication capabilities.</p>
        </div>

        <div class="container">
            <h2>Available Endpoints</h2>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <span class="method post">POST</span>
                <code>/sensor_data</code>
                <p>Handle sensor data with numerical values and units</p>
                <p>Example data structure:</p>
                <pre>{
    "sensor_id": "temperature_1",
    "value": 25.5,
    "unit": "celsius"
}</pre>
            </div>

            <div class="endpoint">
                <span class="method get">GET</span>
                <span class="method post">POST</span>
                <code>/robot_pose</code>
                <p>Handle robot position and orientation data</p>
                <p>Example data structure:</p>
                <pre>{
    "x": 1.0,
    "y": 2.0,
    "z": 0.0,
    "orientation": 90.0
}</pre>
            </div>

            <div class="endpoint">
                <span class="method get">GET</span>
                <span class="method post">POST</span>
                <code>/image_data</code>
                <p>Handle image data with metadata</p>
                <p>Example data structure:</p>
                <pre>{
    "width": 640,
    "height": 480,
    "encoding": "rgb8",
    "data": "base64_encoded_image_data"
}</pre>
            </div>
        </div>

        <div class="container">
            <h2>Quick Links</h2>
            <div class="links">
                <a href="/docs" class="button">Interactive API Documentation</a>
                <a href="/redoc" class="button">ReDoc Documentation</a>
            </div>
        </div>
    </body>
    </html>
    """

@app.post("/sensor_data")
async def receive_sensor_data(data: SensorData):
    sensor_data_store.append(data)
    return {"status": "success", "message": f"Received sensor data from {data.sensor_id}"}

@app.post("/robot_pose")
async def receive_robot_pose(pose: RobotPose):
    robot_poses.append(pose)
    return {"status": "success", "message": "Received robot pose"}

@app.post("/image_data")
async def receive_image(image: ImageData):
    image_data_store.append(image)
    return {"status": "success", "message": "Received image data"}

@app.get("/sensor_data")
async def get_sensor_data():
    return sensor_data_store

@app.get("/robot_pose")
async def get_robot_pose():
    return robot_poses

@app.get("/image_data")
async def get_image_data():
    return image_data_store

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
