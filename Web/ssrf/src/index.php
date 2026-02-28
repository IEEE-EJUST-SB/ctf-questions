
<?php
$ip = $_SERVER['REMOTE_ADDR'];

if ($ip === '127.0.0.1' || $ip === '::1') {
    // Localhost access
    echo "Internal Admin Page\n";
    echo "Flag: DEVSTORM{fG^UOcV@$95Kq*X%}";

} 
// else {


    $files = scandir('.');
    foreach ($files as $file) {
        if ($file === '.' || $file === '..' || $file === 'index.php') continue;
        echo "/".$file . "\n";
    }
// }
?>
