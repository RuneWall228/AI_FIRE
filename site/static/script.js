
document.getElementById('toggle-model').addEventListener('click', async () => {
    const currentModel = document.getElementById('model-info').textContent.split(': ')[1];
    const newModel = currentModel === 'YOLO8n' ? 'YOLO11s' : 'YOLO8n';

    const response = await fetch('/switch_model', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ model: newModel })
    });

    if (response.ok) {
        const result = await response.json();
        document.getElementById('model-info').textContent = `Current Model: ${newModel}`;
        alert(result.message);
    } else {
        const error = await response.json();
        alert(`Error: ${error.error}`);
    }
});
