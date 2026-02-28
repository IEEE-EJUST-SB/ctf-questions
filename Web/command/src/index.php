<?php
// hard_ping.php

// Display form
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
?>
    <h1>SuperSecure Ping Tool</h1>
    <form method="POST">
        <label for="host">Host:</label>
        <input type="text" name="host" id="host" required>
        <button type="submit">Ping</button>
    </form>
<?php
    die();
}

// Sanitize input
$host = $_POST['host'] ?? '';

if (preg_match('/[;&|$`><]/', $host)) {

    die("Hacking attempt detected.");
}

$blocked_words = ['cat', 'ls', 'id'];

foreach ($blocked_words as $word) {
    if (stripos($host, $word) !== false) {
        die("Hacking attempt detected: forbidden word.");
    }
}
// Prevent local file and internal access
// if (preg_match('/127\.|localhost|0\.0\.0\.0|::1/', $host)) {
//     die("Access denied.");
// }

// Extra validation: allow only alphanumeric, dot, and dash
// if (!preg_match('/^[a-zA-Z0-9\.\-]+$/', $host)) {
//     die("Invalid hostname.");
// }

// Build safe shell command
$command = "ping -c 1 " . $host;

// shell_exec("apt-get update && apt-get install -y iputils-ping > /dev/null 2>&1");


// Simulate logging (this is the vulnerable line)
$output = shell_exec("echo '[LOG] User pinged: $host' >> /dev/null && $command 2>&1");

// Display output
echo "<pre>$host</pre>";

echo "<pre>$output</pre>";

// Hidden flag location
if (isset($_GET['source'])) {
    highlight_file(__FILE__);
}

?>
