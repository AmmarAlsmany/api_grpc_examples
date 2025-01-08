import grpc
import ros_messages_pb2
import ros_messages_pb2_grpc
from concurrent import futures
import time
import logging
from typing import Iterator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ROSGRPCPublisher(ros_messages_pb2_grpc.ROSBridgeServicer):
    """
    gRPC server that simulates a ROS node publishing data.
    Implements streaming endpoints for different types of data.
    """
    
    def StreamSensorData(self, request_iterator: Iterator[ros_messages_pb2.SensorData], 
                        context) -> Iterator[ros_messages_pb2.StatusResponse]:
        """Handle streaming sensor data"""
        try:
            for request in request_iterator:
                logger.info(f"Received sensor data from {request.sensor_id}: {request.value} {request.unit}")
                
                # Process the sensor data (in a real ROS node, this would publish to a ROS topic)
                # Here we just acknowledge receipt
                yield ros_messages_pb2.StatusResponse(
                    success=True,
                    message=f"Processed sensor data from {request.sensor_id}"
                )
        except Exception as e:
            logger.error(f"Error processing sensor data: {str(e)}")
            context.abort(grpc.StatusCode.INTERNAL, f"Internal error: {str(e)}")

    def StreamRobotPose(self, request_iterator: Iterator[ros_messages_pb2.RobotPose], 
                       context) -> Iterator[ros_messages_pb2.StatusResponse]:
        """Handle streaming robot pose data"""
        try:
            for request in request_iterator:
                logger.info(f"Received robot pose: x={request.x}, y={request.y}, z={request.z}, "
                          f"orientation={request.orientation}")
                
                # Process the robot pose (in a real ROS node, this would publish to a ROS topic)
                yield ros_messages_pb2.StatusResponse(
                    success=True,
                    message="Processed robot pose data"
                )
        except Exception as e:
            logger.error(f"Error processing robot pose: {str(e)}")
            context.abort(grpc.StatusCode.INTERNAL, f"Internal error: {str(e)}")

    def StreamImageData(self, request_iterator: Iterator[ros_messages_pb2.ImageData], 
                       context) -> Iterator[ros_messages_pb2.StatusResponse]:
        """Handle streaming image data"""
        try:
            for request in request_iterator:
                logger.info(f"Received image: {request.width}x{request.height}, "
                          f"encoding={request.encoding}")
                
                # Process the image data (in a real ROS node, this would publish to a ROS topic)
                yield ros_messages_pb2.StatusResponse(
                    success=True,
                    message="Processed image data"
                )
        except Exception as e:
            logger.error(f"Error processing image data: {str(e)}")
            context.abort(grpc.StatusCode.INTERNAL, f"Internal error: {str(e)}")

def generate_sample_data():
    """Generate sample data for testing"""
    # Sensor data
    sensor_data = ros_messages_pb2.SensorData(
        sensor_id="temp_sensor_1",
        value=25.5,
        unit="celsius",
        timestamp=int(time.time())
    )
    
    # Robot pose
    robot_pose = ros_messages_pb2.RobotPose(
        x=1.0,
        y=2.0,
        z=0.0,
        orientation=90.0,
        timestamp=int(time.time())
    )
    
    # Image data
    image_data = ros_messages_pb2.ImageData(
        width=640,
        height=480,
        encoding="rgb8",
        data=b"dummy_image_data",
        timestamp=int(time.time())
    )
    
    return sensor_data, robot_pose, image_data

def serve(port: int = 50051, max_workers: int = 10) -> None:
    """Start the gRPC server"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    ros_messages_pb2_grpc.add_ROSBridgeServicer_to_server(ROSGRPCPublisher(), server)
    
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    
    logger.info(f"gRPC server started on port {port}")
    logger.info("Available services:")
    logger.info("1. StreamSensorData - For streaming sensor readings")
    logger.info("2. StreamRobotPose - For streaming robot position and orientation")
    logger.info("3. StreamImageData - For streaming image data")
    
    try:
        while True:
            time.sleep(86400)  # One day in seconds
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        server.stop(0)

if __name__ == '__main__':
    serve()
