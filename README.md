# ROS-Python Communication Examples

This project demonstrates different methods of communication between ROS and Python applications using various API protocols.

## Project Structure
```
ros_python_communication/
├── rest_api/
│   ├── ros_rest_publisher/       # ROS node that publishes data via REST API
│   └── python_rest_client/       # Python FastAPI client that receives data
├── grpc_api/
│   ├── protos/                  # Protocol buffer definitions
│   ├── ros_grpc_publisher/      # ROS node that publishes data via gRPC
│   └── python_grpc_client/      # Python gRPC client that receives data
```

## Protocols Implemented
1. RESTful API using FastAPI
2. gRPC

## Prerequisites
- Python 3.8+
- FastAPI
- gRPC tools
- Protocol Buffers

## Installation
```bash
pip install fastapi uvicorn grpcio grpcio-tools protobuf
```

## Usage
Each protocol implementation has its own README with specific instructions.

1. REST API Example:
   - Simple HTTP-based communication
   - Easy to understand and implement
   - Good for basic data transfer

2. gRPC Example:
   - High-performance RPC framework
   - Strongly typed contracts using Protocol Buffers
   - Efficient for streaming data
   - Good for complex data transfer

## Key Features
- Multiple protocol implementations
- Support for different data types
- Bidirectional communication
- Example implementations for both server and client sides
