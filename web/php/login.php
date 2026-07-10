<?php
session_start();
require_once 'config.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $student_id = trim($_POST['student_id']);
    
    // Basic validation
    if (empty($student_id) || !ctype_digit($student_id)) {
        header("Location: ../index.html?error=invalid_format");
        exit();
    }

    $db = get_db_connection();

    $stmt = $db->prepare('SELECT student_id, name FROM students WHERE student_id = :student_id');
    if (!$stmt) {
        die("System error: Failed to prepare statement.");
    }

    $stmt->bindValue(':student_id', $student_id, SQLITE3_TEXT);
    $result = $stmt->execute();
    
    if (!$result) {
        die("System error: Failed to execute query.");
    }

    $row = $result->fetchArray(SQLITE3_ASSOC);
    if ($row) {
        $_SESSION['student_id'] = $row['student_id'];
        $_SESSION['name'] = $row['name'];
        header("Location: attendance.php");
        exit();
    } else {
        // Redirect back to login with error
        header("Location: ../index.html?error=not_found");
        exit();
    }
}
?>
