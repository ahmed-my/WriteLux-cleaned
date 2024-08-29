document.addEventListener('DOMContentLoaded', function() {
    console.log('Script loaded');

    const form = document.getElementById('uploadForm');
    const folderCheckboxes = document.querySelectorAll('input[type="checkbox"][name="folders"]');

    if (form) {
        console.log('Form found:', form);

        const folderIdsInput = document.createElement('input');
        folderIdsInput.type = 'hidden';
        folderIdsInput.name = 'folder_ids';
        form.appendChild(folderIdsInput);

        function updateSelectedFolders() {
            const selectedFolderIds = [];
            folderCheckboxes.forEach((checkbox) => {
                console.log('Checkbox:', checkbox.value, 'Checked:', checkbox.checked);
                if (checkbox.checked) {
                    selectedFolderIds.push(checkbox.value);
                }
            });
            folderIdsInput.value = selectedFolderIds.join(',');
            console.log('Updated folder IDs:', folderIdsInput.value);
        }

        folderCheckboxes.forEach((checkbox) => {
            checkbox.addEventListener('change', updateSelectedFolders);
        });

        updateSelectedFolders();

        form.addEventListener('submit', function(event) {
            event.preventDefault();
            console.log('Form submission triggered.');

            if (!folderIdsInput.value) {
                alert('Please select at least one folder to upload the image.');
                return;
            }

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
                    alert('Image uploaded to the selected folders.');
                    window.location.href = form.dataset.redirectUrl;
                } else {
                    alert('There was an error uploading the image.');
                    console.log('Response status:', response.status);
                }
            }).catch(error => {
                alert('There was an error uploading the image.');
                console.error('Error:', error);
            });
        });
    } else {
        console.error('Form not found!');
    }
});
