document.addEventListener('DOMContentLoaded', function() {
    console.log('Script loaded');
    const form = document.getElementById('uploadForm');
    if (form) {
        console.log('Form found:', form);

        form.addEventListener('submit', function(event) {
            event.preventDefault();
            console.log('Form submission triggered.');

            const folderSelect = form.querySelector('select[name="folder"]');
            if (folderSelect) {
                console.log('Folder select found:', folderSelect);
                const selectedFolderName = folderSelect.options[folderSelect.selectedIndex].text;
                console.log('Selected folder:', selectedFolderName);

                const formData = new FormData(form);
                console.log('FormData contents:', Array.from(formData.entries()));

                fetch(form.action, {
                    method: form.method,
                    body: formData,
                    headers: {
                        'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
                    }
                }).then(response => {
                    if (response.ok) {
                        alert(`Image uploaded to the "${selectedFolderName}" folder.`);
                        window.location.href = form.dataset.redirectUrl;
                    } else {
                        alert('There was an error uploading the image.');
                        console.log('Response status:', response.status);
                    }
                }).catch(error => {
                    alert('There was an error uploading the image.');
                    console.error('Error:', error);
                });
            } else {
                // Handle case where select element is not found
                console.error('Folder select element not found!');
                alert('Please select a folder to upload the image.');
            }
        });
    } else {
        console.error('Form not found!');
    }
});
