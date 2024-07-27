<?php
session_start();
if (!isset($_SESSION['student_id'])) {
    header("Location: ../index.html");
    exit();
}

$student_id = $_SESSION['student_id'];
$name = $_SESSION['name'];
$db = new SQLite3('C:/sqlite/gui/attendance');  // Adjust path as per your setup

if (!$db) {
    die("Failed to connect to database: " . $db->lastErrorMsg());
}

// Fetch attendance records
$stmt = $db->prepare('SELECT date, attended FROM attendance_daily WHERE student_id = :student_id ORDER BY date DESC');
if (!$stmt) {
    die("Failed to prepare statement: " . $db->lastErrorMsg());
}
$stmt->bindValue(':student_id', $student_id, SQLITE3_INTEGER);
$result = $stmt->execute();
if (!$result) {
    die("Failed to execute query: " . $db->lastErrorMsg());
}

// Calculate attendance statistics
$today = date('Y-m-d');

// Total school days (excluding weekends and holidays)
$total_days_stmt = $db->query("SELECT COUNT(DISTINCT date) AS total_days FROM attendance_daily");
$total_days_row = $total_days_stmt->fetchArray(SQLITE3_ASSOC);
$total_days = $total_days_row['total_days'];

// Days attended
$attended_days_stmt = $db->prepare("SELECT COUNT(date) AS attended_days FROM attendance_daily WHERE student_id = :student_id AND attended = 1");
$attended_days_stmt->bindValue(':student_id', $student_id, SQLITE3_INTEGER);
$attended_days_row = $attended_days_stmt->execute()->fetchArray(SQLITE3_ASSOC);
$attended_days = $attended_days_row['attended_days'];

$attendance_percentage = ($total_days > 0) ? ($attended_days / $total_days) * 100 : 0;
$attendance_percentage = round($attendance_percentage, 2);

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Attendance Records and Statistics</title>
    <link rel="stylesheet" href="../css/styles.css">  <!-- Use existing CSS file -->
</head>
<body>
    <div class="container">
        <header>
            <img src="images/school-logo.jpg" alt="School Logo" class="school-logo">
            <h1>Assumption College Nakhonratchasima</h1>
        </header>
        <main>
            <div class="attendance-container">
                <h2>Attendance Records for <?php echo htmlspecialchars($name); ?></h2>
                
                <!-- Attendance Statistics -->
                <div class="statistics">
                    <h3>Attendance Statistics</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Total Days</th>
                                <td><?php echo $total_days; ?></td>
                            </tr>
                            <tr>
                                <th>Days Attended</th>
                                <td><?php echo $attended_days; ?></td>
                            </tr>
                            <tr>
                                <th>Attendance Percentage</th>
                                <td><?php echo $attendance_percentage; ?>%</td>
                            </tr>
                        </thead>
                    </table>
                </div>
                
                <!-- Attendance Records -->
                <h3>Attendance Records</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Attended</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php while ($row = $result->fetchArray(SQLITE3_ASSOC)) { ?>
                            <tr>
                                <td><?php echo htmlspecialchars($row['date']); ?></td>
                                <td><?php echo $row['attended'] ? 'Yes' : 'No'; ?></td>
                            </tr>
                        <?php } ?>
                    </tbody>
                </table>
                <a href="logout.php">Logout</a>
            </div>
        </main>
        <footer>
            <p>&copy; 2024 Assumption College Nakhonratchasima. All rights reserved.</p>
            <p>Website created by MonkeysFromS5</p>
        </footer>
    </div>
</body>
</html>
