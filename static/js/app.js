/* ═══════════════════════════════════════
   NailBook — Main JavaScript
   ═══════════════════════════════════════ */

// Toggle password visibility
function togglePassword(inputId) {
    var input = document.getElementById(inputId);
    var btn = input.parentElement.querySelector('.toggle-password');
    var eyeIcon = btn.querySelector('.eye-icon');
    var eyeOffIcon = btn.querySelector('.eye-off-icon');

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

// Show styled confirmation modal instead of browser confirm()
function showConfirm(message, onConfirm) {
    var overlay = document.getElementById('confirmModal');
    if (!overlay) return;
    document.getElementById('confirmMessage').textContent = message;
    var confirmBtn = document.getElementById('confirmYesBtn');
    var newBtn = confirmBtn.cloneNode(true);
    confirmBtn.parentNode.replaceChild(newBtn, confirmBtn);
    newBtn.id = 'confirmYesBtn';
    newBtn.addEventListener('click', function() {
        closeModal('confirmModal');
        onConfirm();
    });
    openModal('confirmModal');
}

// Intercept all forms with data-confirm attribute
document.addEventListener('submit', function(e) {
    var form = e.target;
    if (!form.hasAttribute('data-confirm')) return;
    if (form.dataset.confirmed === 'true') {
        form.removeAttribute('data-confirmed');
        return;
    }
    e.preventDefault();
    showConfirm(form.getAttribute('data-confirm'), function() {
        form.dataset.confirmed = 'true';
        form.submit();
    });
});

// Open edit client modal with pre-filled data from data attributes
document.addEventListener('click', function(e) {
    var btn = e.target.closest('.edit-client-btn');
    if (!btn) return;

    document.getElementById('editClientForm').action = '/clients/edit/' + btn.dataset.id;
    document.getElementById('edit_name').value = btn.dataset.name;
    document.getElementById('edit_phone').value = btn.dataset.phone;
    document.getElementById('edit_birthday').value = btn.dataset.birthday;
    document.getElementById('edit_notes').value = btn.dataset.notes;
    document.getElementById('edit_allergies').value = btn.dataset.allergies;
    document.getElementById('edit_favourite_colours').value = btn.dataset.colours;
    document.getElementById('edit_nail_shape').value = btn.dataset.shape;
    document.getElementById('edit_status').value = btn.dataset.status;
    openModal('editClientModal');
});

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

// Toggle client details expand/collapse
function toggleClientDetails(clientId, btn) {
    var details = document.getElementById('details-' + clientId);
    var text = btn.querySelector('.expand-text');
    var icon = btn.querySelector('.expand-icon');

    if (details.classList.contains('collapsed')) {
        details.classList.remove('collapsed');
        text.textContent = 'Show less';
        icon.style.transform = 'rotate(180deg)';
    } else {
        details.classList.add('collapsed');
        text.textContent = 'Show more';
        icon.style.transform = 'rotate(0deg)';
    }
}

// Open edit task modal from data attributes
document.addEventListener('click', function(e) {
    var btn = e.target.closest('.edit-task-btn');
    if (!btn) return;
    document.getElementById('editTaskForm').action = '/checklists/edit/' + btn.dataset.id;
    document.getElementById('edit_task_text').value = btn.dataset.text;
    openModal('editTaskModal');
});
