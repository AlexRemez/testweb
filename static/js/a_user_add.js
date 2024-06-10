document.addEventListener('DOMContentLoaded', () => {
    const tgIdInput = document.getElementById('tg_id');
    const firstNameInput = document.getElementById('first_name');
    const submitBtn = document.getElementById('submitBtn');
    function validateForm() {
        let isValid = true;
        if (!tgIdInput.value.trim()) {
            tgIdInput.classList.add('error');
            isValid = false;
        } else {
            tgIdInput.classList.remove('error');
        }
        if (!firstNameInput.value.trim()) {
            firstNameInput.classList.add('error');
            isValid = false;
        } else {
            firstNameInput.classList.remove('error');
        }
        return isValid;
    }
    function toggleSubmitButton() {
        if (tgIdInput.value.trim() && firstNameInput.value.trim()) {
            submitBtn.classList.add('visible');
        } else {
            submitBtn.classList.remove('visible');
        }
    }
    tgIdInput.addEventListener('input', toggleSubmitButton);
    firstNameInput.addEventListener('input', toggleSubmitButton);
    submitBtn.addEventListener('click', () => {
        if (validateForm()) {
            const data = {
                tg_id: tgIdInput.value,
                first_name: firstNameInput.value,
                username: document.getElementById('username').value
            };
            fetch('/admin/users/create_user', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                if (result.success) {
                    window.location.href = `/admin/user/${result.user_id}?message=Пользователь успешно создан!`;
                } else {
                    // handle error
                }
            })
            .catch(error => {
                // handle error
            });
        }
    });
});