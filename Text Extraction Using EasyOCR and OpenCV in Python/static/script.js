document.getElementById('chooseImageButton').addEventListener('click', function() {
    document.getElementById('imageInput').click();
});

document.getElementById('uploadForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const formData = new FormData();
    formData.append('image', document.getElementById('imageInput').files[0]);

    const uploadButton = document.getElementById('uploadButton');
    const loadingAnimation = document.getElementById('loadingAnimation');
    loadingAnimation.style.display = 'inline-block';

    try {
        const response = await fetch('/extract_text', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const data = await response.json();
            displayTextResults(data.text);
            displayProcessedImage(data.image);
        } else {
            console.error('Error extracting text:', response.statusText);
        }
    } catch (error) {
        console.error('Error extracting text:', error.message);
    } finally {
        loadingAnimation.style.display = 'none';
    }
});

function displayTextResults(text) {
    const textResultsDiv = document.getElementById('textResults');
    textResultsDiv.textContent = `Extracted Text: ${text}`;
}

function displayProcessedImage(imageData) {
    const imageContainer = document.getElementById('imageContainer');
    imageContainer.innerHTML = `<img src="data:image/png;base64,${imageData}" alt="Processed Image">`;

    const downloadButton = document.getElementById('downloadButton');
    downloadButton.style.display = 'block';
    downloadButton.onclick = function() {
        const link = document.createElement('a');
        link.href = `data:image/png;base64,${imageData}`;
        link.download = 'processed_image.png';
        link.click();
    };
}

document.getElementById('imageInput').addEventListener('change', function(event) {
    const uploadButton = document.getElementById('uploadButton');
    const file = event.target.files[0];

    document.getElementById('selectedImageName').textContent = file.name;
    uploadButton.removeAttribute('disabled');
});
