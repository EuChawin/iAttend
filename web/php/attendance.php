<?php
session_start();
require_once 'config.php';

if (!isset($_SESSION['student_id'])) {
    header("Location: ../index.html");
    exit();
}

$student_id = $_SESSION['student_id'];
$name = $_SESSION['name'];
$db = get_db_connection();

// Fetch attendance records
$stmt = $db->prepare('
    SELECT date, entry_time, exit_time, late, attended
    FROM attendance_daily
    WHERE student_id = :student_id
    ORDER BY date DESC
');
if (!$stmt) {
    die("System error: Failed to prepare statement.");
}

$stmt->bindValue(':student_id', $student_id, SQLITE3_TEXT);
$result = $stmt->execute();
if (!$result) {
    die("System error: Failed to execute query.");
}

// Process data
$records = [];
$total_days = 0;
$present_days = 0;
$late_days = 0;

while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
    $records[] = $row;
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
    <title>iAttend - My Attendance</title>
    <link rel="stylesheet" href="../css/styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
</head>
<body class="fade-in">
    <div class="app-wrapper">
        <header class="top-nav">
            <div class="brand">
                <img src="../assets/school-logo.jpg" alt="ACN Logo" class="school-logo">
                <div class="brand-text">
                    <h1>iAttend</h1>
                    <span class="sub-brand">Assumption College Nakhonratchasima</span>
                </div>
            </div>
            <div class="user-menu">
                <span class="user-name"><?php echo htmlspecialchars($name); ?></span>
                <a href="logout.php" class="btn btn-outline">Logout</a>
            </div>
        </header>

        <main class="dashboard-content">
            <div class="stats-grid">
                <div class="stat-card">
                    <h3>Total Days</h3>
                    <div class="stat-value"><?php echo $total_days; ?></div>
                </div>
                <div class="stat-card">
                    <h3>Present</h3>
                    <div class="stat-value text-success"><?php echo $present_days; ?></div>
                </div>
                <div class="stat-card">
                    <h3>Absent</h3>
                    <div class="stat-value text-danger"><?php echo $absent_days; ?></div>
                </div>
                <div class="stat-card">
                    <h3>Late</h3>
                    <div class="stat-value text-warning"><?php echo $late_days; ?></div>
                </div>
                <div class="stat-card">
                    <h3>Attendance Rate</h3>
                    <div class="stat-value"><?php echo number_format($attendance_percentage, 1); ?>%</div>
                </div>
            </div>

            <div class="card table-card">
                <div class="card-header">
                    <h2>Attendance History</h2>
                </div>
                <div class="table-responsive">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Date</th>
                                <th>Entry Time</th>
                                <th>Exit Time</th>
                                <th>Late Status</th>
                                <th>Attendance</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php if (empty($records)): ?>
                            <tr>
                                <td colspan="5" class="text-center">No attendance records found.</td>
                            </tr>
                            <?php else: ?>
                                <?php foreach ($records as $row): ?>
                                <tr>
                                    <td class="font-medium"><?php echo htmlspecialchars($row['date']); ?></td>
                                    <td><?php echo htmlspecialchars($row['entry_time'] ?: '--:--'); ?></td>
                                    <td><?php echo htmlspecialchars($row['exit_time'] ?: '--:--'); ?></td>
                                    <td>
                                        <?php if ($row['late']): ?>
                                            <span class="badge badge-warning">Late</span>
                                        <?php else: ?>
                                            <span class="badge badge-neutral">On Time</span>
                                        <?php endif; ?>
                                    </td>
                                    <td>
                                        <?php if ($row['attended']): ?>
                                            <span class="badge badge-success">Present</span>
                                        <?php else: ?>
                                            <span class="badge badge-danger">Absent</span>
                                        <?php endif; ?>
                                    </td>
                                </tr>
                                <?php endforeach; ?>
                            <?php endif; ?>
                        </tbody>
                    </table>
                </div>
            </div>
        </main>

        <footer>
            <p>&copy; <?php echo date("Y"); ?> Assumption College Nakhonratchasima. All rights reserved.</p>
            <p class="credit">Powered by iAttend</p>
        </footer>
    </div>
    <script src="../js/main.js"></script>
</body>
</html>
