# Flask API Server

This Flask API server is designed to handle requests from a frontend application, manage JWT authentication, and handle errors gracefully. It supports **Cross-Origin Resource Sharing (CORS)**, allowing secure communication between the backend and an Angular frontend.

## Features

- **Flask-based API**  
- **JWT Authentication** for secure access  
- **CORS Configuration** to allow specific frontend access  
- **Blueprint Routing** for modularity  
- **Custom Error Handling** for better debugging  
- **User Input for Host and Port Configuration**  

## Installation

### Prerequisites

Ensure you have **Python 3** installed along with `pip`. Then, install the required dependencies:

```bash
pip install flask flask-jwt-extended flask-cors termcolor
