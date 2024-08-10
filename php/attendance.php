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
$stmt = $db->prepare('
    SELECT date, entry_time, exit_time, late, attended
    FROM attendance_daily
    WHERE student_id = :student_id
    ORDER BY date DESC
');
if (!$stmt) {
    die("Failed to prepare statement: " . $db->lastErrorMsg());
}

$stmt->bindValue(':student_id', $student_id, SQLITE3_INTEGER);
$result = $stmt->execute();
if (!$result) {
    die("Failed to execute query: " . $db->lastErrorMsg());
}

// Calculate attendance and late stats
$total_days = 0;
$present_days = 0;
$late_days = 0;

while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
    $total_days++;
    if ($row['attended']) {
        $present_days++;
    }
    if ($row['late']) {
        $late_days++;
    }
}

$absent_days = $total_days - $present_days;
$attendance_percentage = $total_days > 0 ? ($present_days / $total_days) * 100 : 0;
$late_percentage = $total_days > 0 ? ($late_days / $total_days) * 100 : 0;
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Attendance Records</title>
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
                <table>
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Entry Time</th>
                            <th>Exit Time</th>
                            <th>Late</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php
                        // Reset the result pointer to the start
                        $result->reset();
                        while ($row = $result->fetchArray(SQLITE3_ASSOC)) { ?>
                            <tr>
                                <td><?php echo htmlspecialchars($row['date']); ?></td>
                                <td><?php echo htmlspecialchars($row['entry_time'] ? $row['entry_time'] : 'N/A'); ?></td>
                                <td><?php echo htmlspecialchars($row['exit_time'] ? $row['exit_time'] : 'N/A'); ?></td>
                                <td><?php echo $row['late'] ? 'Yes' : 'No'; ?></td>
                                <td><?php echo $row['attended'] ? 'Present' : 'Absent'; ?></td>
                            </tr>
                        <?php } ?>
                    </tbody>
                </table>
                
                <!-- Stats section -->
                <div class="stats-container">
                    <h3>Attendance Statistics</h3>
                    <p>Total Days: <?php echo $total_days; ?></p>
                    <p>Present Days: <?php echo $present_days; ?></p>
                    <p>Absent Days: <?php echo $absent_days; ?></p>
                    <p>Late Days: <?php echo $late_days; ?></p>
                    <p>Attendance Percentage: <?php echo number_format($attendance_percentage, 2); ?>%</p>
                    <p>Late Percentage: <?php echo number_format($late_percentage, 2); ?>%</p>
                </div>

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
