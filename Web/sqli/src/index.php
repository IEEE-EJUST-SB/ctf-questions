<?php
// Minimal error handling for production
ini_set('display_errors', 0);
error_reporting(0);
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Form</title>
    <style>
      body {
        background-color: #f3f4f6;
        font-family: Arial, sans-serif;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin: 0;
      }
      .login-container {
        background-color: #fff;
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        width: 300px;
      }
      .login-container h2 {
        margin-bottom: 1.5rem;
        text-align: center;
      }
      .form-group {
        margin-bottom: 1rem;
      }
      .form-group label {
        display: block;
        margin-bottom: 0.5rem;
        font-weight: bold;
      }
      .form-group input {
        width: 100%;
        padding: 0.5rem;
        border: 1px solid #ccc;
        border-radius: 0.5rem;
        box-sizing: border-box;
      }
      .login-btn {
        width: 100%;
        padding: 0.75rem;
        border: none;
        border-radius: 0.5rem;
        background-color: #3b82f6;
        color: white;
        font-size: 1rem;
        cursor: pointer;
        transition: background-color 0.3s;
      }
      .login-btn:hover {
        background-color: #2563eb;
      }
      .result {
        margin-top: 1rem;
        padding: 0.75rem;
        background-color: #f8f9fa;
        border-radius: 0.5rem;
        font-size: 0.9rem;
      }
    </style>
</head>
<body>

<div class="login-container">
  <p>username: guest  password: guest123</p>
    <h2>Login</h2>
    <form method="POST">
        <div class="form-group">
            <label for="name">Username</label>
            <input type="text" name="name" id="name" required>
        </div>
        <div class="form-group">
            <label for="password">Password</label>
            <input type="password" name="password" id="password" required>
        </div>
        <button type="submit" class="login-btn">Log In</button>
    </form>

<?php
if (isset($_POST['name']) && isset($_POST['password'])) {
    echo "<div class='result'>";
    
    $user_name = $_POST['name'];
    $user_password = $_POST['password'];
    
    $filter = array('union', 'select', 'or', 'load_file', 'from', 'where', '=', 'like');
    
    // Apply filter to block certain keywords
    foreach ($filter as $word) {
        if (stripos($user_name, $word) !== false || stripos($user_password, $word) !== false) {
            echo "Blocked keyword detected!";
            echo "</div>";
            exit();
        }
    }
    
    try {
        $dsn = "mysql:host=mariadb;dbname=ctf_lab;charset=utf8mb4";
        $username = "appuser";
        $password = "apppassword";
        
        $pdo = new PDO($dsn, $username, $password);
        
        // Build the query (intentionally vulnerable)
        $query = "SELECT username, password FROM users WHERE username = '$user_name' AND password = '$user_password'";
        
        // Execute query
        $stmt = $pdo->query($query);
        $results = $stmt->fetchAll(PDO::FETCH_ASSOC);
        
        if (count($results) > 0) {
            foreach ($results as $row) {
                echo "User: " . htmlspecialchars($row["username"]) . " - Password: " . htmlspecialchars($row["password"]);
            }
        } else {
            echo "No user found with these credentials.";
        }
        // echo  '<p>',$query,'</p>';
        
    } catch (Exception $e) {
        echo "An error occurred. Please try again.";
    }
    
    echo "</div>";
}
?>
</div>

</body>
</html>