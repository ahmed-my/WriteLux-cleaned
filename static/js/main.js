document.addEventListener('DOMContentLoaded', function() {
    const successMessages = document.querySelectorAll('.messages .success');
    if (successMessages.length > 0) {
        successMessages.forEach(message => {
            alert(message.textContent);
        });
    }
});

/* confirm delete */
document.addEventListener('DOMContentLoaded', function() {
    console.log('Document loaded, adding event listeners.');
    document.querySelectorAll('.delete-link').forEach(function(link) {
        console.log('Adding event listener to:', link);
        link.addEventListener('click', function(event) {
            event.preventDefault();
            console.log('Delete link clicked.');
            const url = this.getAttribute('data-url');
            const confirmDelete = confirm('Are you sure you want to delete this post?');
            
            if (confirmDelete) {
                console.log('User confirmed delete.');
                window.location.href = url;
            } else {
                console.log('User canceled delete.');
            }
        });
    });
});
