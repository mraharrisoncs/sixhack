document.getElementById('sandbox-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const code = document.getElementById('code-input').value;

    const response = await fetch('/sandbox', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code })
    });

    const data = await response.json();
    document.getElementById('output').textContent = JSON.stringify(data, null, 2);
});