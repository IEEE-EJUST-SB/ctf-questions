<h2>Simple Source Preview Tool</h2>
<form method="GET">
    <input type="text" name="url" placeholder="Enter a URL">
    <input type="submit" value="Fetch">
</form>

<?php
$url = $_GET['url'] ?? '';
$serverIP = $_SERVER['SERVER_ADDR'];
// Basic filters
$blocked = ['127.','localhost', '::1', 
'0.0.0.0','2130706433','0x7f000001',
'0177.0.0.1','::ffff:127.0.0.1',
'[0000::1]','[0:0:0:0:0:ffff:127.0.0.1]',
'[::ffff:127.0.0.1]',$serverIP,'localh',
'local',
'ip6-localhost',
'ip6-loopback',
];
foreach ($blocked as $block) {
    if (stripos($url, $block) !== false) {
        die("Access to local IPs is forbidden.");
    }
}

// Allow only http(s)
if (!preg_match('/^https?:\/\//i', $url)) {
    die("Only HTTP/HTTPS allowed.");
}

// SSRF logic
$resp = @file_get_contents($url);
if ($resp !== false) {
    echo "<pre>" . htmlentities($resp) . "</pre>";
} else {
    echo "Could not fetch URL.";
}

?>
