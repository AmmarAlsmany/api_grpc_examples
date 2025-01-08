import grpc
import ros_messages_pb2
import ros_messages_pb2_grpc
from concurrent import futures
import time
import logging
from typing import Iterator, Optional
import threading

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GRPCClient:
    """
    gRPC client for communicating with the ROS bridge server.
    Provides methods to send and receive different types of data.
    """

    def __init__(self, address: str = "localhost:50051"):
        self.channel = grpc.insecure_channel(address)
        self.stub = ros_messages_pb2_grpc.ROSBridgeStub(self.channel)
        self.running = False
        logger.info(f"Connected to gRPC server at {address}")

    def start_streaming(self) -> None:
        """Start all data streaming services"""
        self.running = True
        
        # Start each stream in a separate thread
        threads = [
            threading.Thread(target=self.stream_sensor_data),
            threading.Thread(target=self.stream_robot_pose),
            threading.Thread(target=self.stream_image_data)
        ]
        
        for thread in threads:
            thread.daemon = True
            thread.start()
        
        logger.info("All streaming services started")

    def stop_streaming(self) -> None:
        """Stop all streaming services"""
        self.running = False
        logger.info("Stopping all streaming services...")

    def stream_sensor_data(self) -> None:
        """Stream sensor data to the server"""
        try:
            while self.running:
                # Create sample sensor data
                sensor_data = ros_messages_pb2.SensorData(
                    sensor_id="temp_sensor_1",
                    value=25.5,
                    unit="celsius",
                    timestamp=int(time.time() * 1000)
                )
                
                # Stream the data and get responses
                responses = self.stub.StreamSensorData(self._generate_sensor_data(sensor_data))
                for response in responses:
                    if not self.running:
                        break
                    logger.info(f"Sensor data response: {response.message}")
                
        except grpc.RpcError as e:
            logger.error(f"Error in sensor data stream: {e.details()}")
        except Exception as e:
            logger.error(f"Unexpected error in sensor data stream: {str(e)}")

    def stream_robot_pose(self) -> None:
        """Stream robot pose data to the server"""
        try:
            while self.running:
                # Create sample robot pose
                pose = ros_messages_pb2.RobotPose(
                    x=1.0,
                    y=2.0,
                    z=0.0,
                    orientation=90.0,
                    timestamp=int(time.time() * 1000)
                )
                
                # Stream the data and get responses
                responses = self.stub.StreamRobotPose(self._generate_robot_pose(pose))
                for response in responses:
                    if not self.running:
                        break
                    logger.info(f"Robot pose response: {response.message}")
                
        except grpc.RpcError as e:
            logger.error(f"Error in robot pose stream: {e.details()}")
        except Exception as e:
            logger.error(f"Unexpected error in robot pose stream: {str(e)}")

    def stream_image_data(self) -> None:
        """Stream image data to the server"""
        try:
            while self.running:
                # Create sample image data
                image = ros_messages_pb2.ImageData(
                    width=640,
                    height=480,
                    encoding="rgb8",
                    data=b"sample_image_data",
                    timestamp=int(time.time() * 1000)
                )
                
                # Stream the data and get responses
                responses = self.stub.StreamImageData(self._generate_image_data(image))
                for response in responses:
                    if not self.running:
                        break
                    logger.info(f"Image data response: {response.message}")
                
        except grpc.RpcError as e:
            logger.error(f"Error in image data stream: {e.details()}")
        except Exception as e:
            logger.error(f"Unexpected error in image data stream: {str(e)}")

    def _generate_sensor_data(self, sample_data: ros_messages_pb2.SensorData) -> Iterator[ros_messages_pb2.SensorData]:
        """Generate a stream of sensor data"""
        while self.running:
            yield sample_data
            time.sleep(1)  # Send data every second

    def _generate_robot_pose(self, sample_pose: ros_messages_pb2.RobotPose) -> Iterator[ros_messages_pb2.RobotPose]:
        """Generate a stream of robot pose data"""
        while self.running:
            yield sample_pose
            time.sleep(0.1)  # Send pose every 100ms

    def _generate_image_data(self, sample_image: ros_messages_pb2.ImageData) -> Iterator[ros_messages_pb2.ImageData]:
        """Generate a stream of image data"""
        while self.running:
            yield sample_image
            time.sleep(0.033)  # Send images at ~30 FPS

def main():
    client = GRPCClient()
    
    try:
        logger.info("Starting gRPC client...")
        client.start_streaming()
        
        # Keep the main thread running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Shutting down client...")
        client.stop_streaming()

if __name__ == "__main__":
    main()
