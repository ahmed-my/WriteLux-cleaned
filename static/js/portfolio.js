document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded and parsed'); // Debugging statement

    const form = document.getElementById('uploadForm');
    if (form) {
        console.log('Form found'); // Debugging statement

        form.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent the default form submission
            console.log('Form submission prevented'); // Debugging statement

            const formData = new FormData(form);
            
            fetch(form.action, {
                method: form.method,
                body: formData,
                headers: {
                    'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
                }
            }).then(response => {
                if (response.ok) {
                    alert('Image uploaded to portfolio.');
                    window.location.href = form.dataset.redirectUrl; // Use data attribute for redirect URL
                } else {
                    alert('There was an error uploading the image.');
                }
            }).catch(error => {
                alert('There was an error uploading the image.');
                console.error('Error:', error);
            });
        });
    } else {
        console.error('Form not found'); // Debugging statement
    }
});
