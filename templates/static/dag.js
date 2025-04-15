const dagContainer = document.getElementById("dag");
const nodes = [
    { id: "node1", label: "Create Pet", x: 50, y: 100 },
    { id: "node2", label: "Get Pet", x: 250, y: 100 },
    { id: "node3", label: "Update Pet", x: 450, y: 100 }
];
nodes.forEach(node => {
    const div = document.createElement("div");
    div.className = "dag-node";
    div.textContent = node.label;
    div.style.position = "absolute";
    div.style.left = node.x + "px";
    div.style.top = node.y + "px";
    dagContainer.appendChild(div);
});
