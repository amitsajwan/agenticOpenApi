# Agentic OpenAPI Tester

This project provides an intelligent, agentic API testing framework built using LangGraph and OpenAPI. It automates API execution, analyzes dependencies, generates payloads, handles retries, and supports dynamic API sequence adjustments. The framework integrates real-time communication using WebSockets and provides a drag-and-drop interface for API execution flows.

---

## Features

- **LangGraph-based API flow**: Dynamically plans and executes API calls in the optimal order based on dependencies.
- **Intelligent Payload Generation**: Uses LLM (e.g., GPT) to generate realistic payloads from OpenAPI schemas, with support for nested objects and IDs.
- **Real-time Chat Interface**: Allows users to interact with the agent, adjust the API execution sequence, and view real-time progress.
- **Interactive DAG**: A drag-and-drop interface for managing API execution order, allowing users to modify the execution flow.
- **Retry Mechanism**: Automatically retries failed API calls, re-plans execution if necessary.
- **Load Testing Support**: After finalizing the API execution sequence, you can run load tests without further user intervention.

---

## Directory Structure

agentic_openapi_tester/ 
├── main.py # FastAPI + WebSocket backend 
├── websocket_manager.py # WebSocket message dispatcher 
├── openapi_parser.py # Parses OpenAPI YAML -> schema map 
├── payload_generator.py # Uses LLM to create payloads intelligently from schema 
├── api_executor.py # Executes APIs sequentially/parallel, manages dependencies and retries ├── agentic_api_planner.py # LangGraph agent determines API execution order ├── state.py # Keeps state (created IDs, responses, etc) 
├── templates/ 
│ └── index.html # Chat + DAG UI frontend 
├── static/ 
│ ├── dag.js # Interactive drag-drop DAG 
│ └── style.css # Styling 
├── specs/ 
│ └── petstore.yaml # OpenAPI specs to load from 
├── utils.py # General utilities (caching, logging, etc) 
├── requirements.txt 
└── README.md

yaml
Copy
Edit

---

## Getting Started

### Prerequisites

Ensure you have Python 3.7+ installed. You will also need to install the dependencies listed in the `requirements.txt` file.

```bash
pip install -r requirements.txt
Running the Application
Start the FastAPI server:

This will start both the WebSocket server and the API execution logic.

bash
Copy
Edit
uvicorn main:app --reload
Navigate to the UI:

Open a web browser and go to http://localhost:8000 to interact with the system.