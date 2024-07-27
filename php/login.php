<?php
session_start();
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $student_id = $_POST['student_id'];
    $db = new SQLite3('C:/sqlite/gui/attendance');  // Adjust path as per your setup

    if (!$db) {
        die("Failed to connect to database: " . $db->lastErrorMsg());
    }

    $stmt = $db->prepare('SELECT student_id, name FROM students WHERE student_id = :student_id');
    if (!$stmt) {
        die("Failed to prepare statement: " . $db->lastErrorMsg());
    }

    $stmt->bindValue(':student_id', $student_id, SQLITE3_INTEGER);
    $result = $stmt->execute();
    if (!$result) {
        die("Failed to execute query: " . $db->lastErrorMsg());
    }

    $row = $result->fetchArray(SQLITE3_ASSOC);
    if ($row) {
        $_SESSION['student_id'] = $row['student_id'];
        $_SESSION['name'] = $row['name'];
        header("Location: attendance.php");
        exit();
    } else {
        echo "Invalid Student ID.";
    }
}
?>
