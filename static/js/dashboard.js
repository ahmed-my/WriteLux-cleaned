document.addEventListener('DOMContentLoaded', function () {
    const checkboxes = document.querySelectorAll('.post-checkbox');
    const createBtn = document.getElementById('create-post-btn');
    const readBtn = document.getElementById('read-post-btn');
    const updateBtn = document.getElementById('update-post-btn');
    const deleteBtn = document.getElementById('delete-post-btn');
    const selectAll = document.getElementById('select-all');

    // Select/Deselect all checkboxes
    if (selectAll) {
        selectAll.addEventListener('change', function () {
            checkboxes.forEach(checkbox => {
                checkbox.checked = selectAll.checked;
            });
        });
    }

    // Handle create operation (no need for selected posts)
    if (createBtn) {
        createBtn.addEventListener('click', function () {
            window.location.href = "{% url 'posts:post_create' %}";
        });
    }

    // Handle read, update operations
    [readBtn, updateBtn].forEach(btn => {
        if (btn) {
            btn.addEventListener('click', function () {
                const selected = document.querySelectorAll('.post-checkbox:checked');
                if (selected.length !== 1) {
                    alert('Please select exactly one post for this action.');
                    return;
                }
                const postId = selected[0].value;
                if (btn === readBtn) {
                    window.location.href = `{% url 'posts:post_detail' pk=0 %}`.replace('0', postId);
                } else if (btn === updateBtn) {
                    window.location.href = `{% url 'posts:post_update' pk=0 %}`.replace('0', postId);
                }
            });
        }
    });

    // Delete multiple posts
    if (deleteBtn) {
        deleteBtn.addEventListener('click', function () {
            const selected = document.querySelectorAll('.post-checkbox:checked');
            if (selected.length === 0) {
                alert('Please select at least one post to delete.');
                return;
            }
            if (confirm('Are you sure you want to delete the selected posts?')) {
                const ids = Array.from(selected).map(checkbox => checkbox.value);
                const url = `{% url 'posts:post_delete' pk=0 %}`.replace('0', ids.join(','));
                fetch(url, {
                    method: 'DELETE',
                    headers: {
                        'X-CSRFToken': '{{ csrf_token }}',
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ ids })
                }).then(response => {
                    if (response.ok) {
                        ids.forEach(id => {
                            const row = document.querySelector(`.post-item input[value='${id}']`).closest('.post-item');
                            if (row) row.remove();
                        });
                    } else {
                        alert('Failed to delete posts.');
                    }
                }).catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred while deleting posts.');
                });
            }
        });
    }
});