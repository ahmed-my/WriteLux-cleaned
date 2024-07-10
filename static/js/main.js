console.log("Using JS. This is a cool")
document.addEventListener('DOMContentLoaded', function() {
    const successMessages = document.querySelectorAll('.messages .success');
    if (successMessages.length > 0) {
        alert('Your post was successfully updated!');
    }
});
