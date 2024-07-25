document.addEventListener('DOMContentLoaded', function() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    document.querySelectorAll('.delete-link').forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            const url = this.getAttribute('data-url');
            const postId = this.getAttribute('data-post-id');
            const confirmDelete = confirm('Are you sure you want to delete this post?');

            if (confirmDelete) {
                fetch(url, {
                    method: 'DELETE',
                    headers: {
                        'X-CSRFToken': csrfToken,
                    },
                })
                .then(response => {
                    if (response.ok) {
                        document.getElementById('post-' + postId).remove();
                        document.getElementById('dashboard-post-' + postId).remove();
                    } else {
                        console.error('Failed to delete the post.');
                    }
                })
                .catch(error => console.error('Error:', error));
            }
        });
    });
});
