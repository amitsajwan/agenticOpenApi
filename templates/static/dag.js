const dagContainer = document.getElementById("dag");

// Example DAG structure
const nodes = [
    { id: "api-1", label: "Create Pet", x: 100, y: 150 },
    { id: "api-2", label: "Get Pet", x: 300, y: 150 },
    { id: "api-3", label: "Update Pet", x: 500, y: 150 }
];

// Render nodes (this can be dynamic based on the LangGraph execution flow)
nodes.forEach(node => {
    const nodeElement = document.createElement("div");
    nodeElement.classList.add("dag-node");
    nodeElement.textContent = node.label;
    nodeElement.style.left = `${node.x}px`;
    nodeElement.style.top = `${node.y}px`;

    // Make nodes draggable
    nodeElement.draggable = true;
    nodeElement.addEventListener("dragstart", (event) => {
        event.dataTransfer.setData("node-id", node.id);
    });

    dagContainer.appendChild(nodeElement);
});

// Add basic styling for nodes
const style = document.createElement('style');
style.innerHTML = `
    .dag-node {
        width: 120px;
        height: 50px;
        background-color: #007BFF;
        color: white;
        text-align: center;
        border-radius: 5px;
        position: absolute;
        cursor: move;
    }
`;
document.head.appendChild(style);
