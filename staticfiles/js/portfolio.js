document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('uploadForm');
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent the default form submission

            const formData = new FormData(form);
            const folderSelect = form.querySelector('select[name="folder"]');
            const selectedFolderName = folderSelect.options[folderSelect.selectedIndex].text; // Get the selected folder's name

            fetch(form.action, {
                method: form.method,
                body: formData,
                headers: {
                    'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
                }
            }).then(response => {
                if (response.ok) {
                    alert(`Image uploaded to the "${selectedFolderName}" folder.`);
                    window.location.href = form.dataset.redirectUrl; // Redirect after successful upload
                } else {
                    alert('There was an error uploading the image.');
                }
            }).catch(error => {
                alert('There was an error uploading the image.');
                console.error('Error:', error);
            });
        });
    }
});
