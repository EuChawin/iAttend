// iAttend Web Interface Scripts

document.addEventListener('DOMContentLoaded', () => {
    // Auto-focus the student ID input field on the login page if it exists
    const studentIdInput = document.getElementById('student_id');
    if (studentIdInput) {
        studentIdInput.focus();
    }
});
