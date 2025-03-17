const preview = document.getElementById('preview');
const imageInput = document.getElementById('image');
const previewContainer = document.getElementById('preview-container');
const predictionDiv = document.getElementById('prediction');

imageInput.addEventListener('change', () => {
    const file = imageInput.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            preview.src = e.target.result;
            previewContainer.style.display = 'block';
        };
        reader.readAsDataURL(file);
    } else {
        preview.src = '#';
        previewContainer.style.display = 'none';
    }
    predictionDiv.textContent = ''; 
});


const form = document.getElementById('upload-form');
form.addEventListener('submit', (e) => {
    e.preventDefault();
    const formData = new FormData(form);
    predictionDiv.textContent = 'Detecting...';

    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const prediction = data.signature;
        predictionDiv.textContent = `Detected Sign: ${prediction}`;
    })
    .catch(error => {
        console.error('Error:', error);
        predictionDiv.textContent = 'Error detecting sign. Please try again.';
    });
});