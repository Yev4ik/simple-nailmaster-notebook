/* ═══════════════════════════════════════
   NailBook — Main JavaScript
   ═══════════════════════════════════════ */

// Toggle password visibility
function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    const btn = input.parentElement.querySelector('.toggle-password');
    const eyeIcon = btn.querySelector('.eye-icon');
    const eyeOffIcon = btn.querySelector('.eye-off-icon');

    if (input.type === 'password') {
        input.type = 'text';
        eyeIcon.style.display = 'none';
        eyeOffIcon.style.display = 'block';
    } else {
        input.type = 'password';
        eyeIcon.style.display = 'block';
        eyeOffIcon.style.display = 'none';
    }
}

// Open modal
function openModal(modalId) {
    document.getElementById(modalId).classList.add('open');
}

// Close modal
function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('open');
}

// Close modal on overlay click
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('modal-overlay') && e.target.classList.contains('open')) {
        e.target.classList.remove('open');
    }
});

// Close modal on Escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal-overlay.open').forEach(function(modal) {
            modal.classList.remove('open');
        });
    }
});

// Auto-dismiss toasts after 4 seconds
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        document.querySelectorAll('.toast').forEach(function(toast) {
            toast.remove();
        });
    }, 4500);
});

// Open edit client modal with pre-filled data
function openEditClient(id, name, phone, birthday, notes, allergies, colours, shape, status) {
    document.getElementById('editClientForm').action = '/clients/edit/' + id;
    document.getElementById('edit_name').value = name;
    document.getElementById('edit_phone').value = phone;
    document.getElementById('edit_birthday').value = birthday;
    document.getElementById('edit_notes').value = notes;
    document.getElementById('edit_allergies').value = allergies;
    document.getElementById('edit_favourite_colours').value = colours;
    document.getElementById('edit_nail_shape').value = shape;
    document.getElementById('edit_status').value = status;
    openModal('editClientModal');
}

// Update procedure info in appointment form
function updateProcedureInfo() {
    var select = document.getElementById('procedureSelect');
    var info = document.getElementById('procedureInfo');
    var option = select.options[select.selectedIndex];

    if (option && option.dataset.price) {
        document.getElementById('procPrice').textContent = option.dataset.price;
        document.getElementById('procDuration').textContent = option.dataset.duration;
        info.style.display = 'flex';
    } else {
        info.style.display = 'none';
    }
}

// Open edit task modal
function openEditTask(taskId, taskText) {
    document.getElementById('editTaskForm').action = '/checklists/edit/' + taskId;
    document.getElementById('edit_task_text').value = taskText;
    openModal('editTaskModal');
}
