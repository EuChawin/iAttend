<?php
// Centralised configuration for the iAttend Web interface

// Absolute path to the SQLite database
// Resolves to: ../../database/attendance.db
define('DB_PATH', realpath(__DIR__ . '/../../database/attendance.db'));

// Connection Helper
function get_db_connection() {
    $db = new SQLite3(DB_PATH);
    if (!$db) {
        die("System error: Unable to connect to the database.");
    }
    return $db;
}
?>
