
<html>
<head>
<title>Secure Login Portal</title>
</head>
<body bgcolor=#1e1e2e>
<!-- standard MD5 implementation -->
<script type="text/javascript" src="md5.js"></script>

<script type="text/javascript">
  function verify() {
    checkpass = document.getElementById("pass").value;
    split = 4;
    if (checkpass.substring(0, split) === "DEV") {
      if (checkpass.substring(split * 6, split * 7) === "AaIu") {
      if ( checkpass.substring(split, split * 2) === "STORM{")  {
         if ( checkpass.substring(split * 3, split * 4) === "HXMJ") {
          if (checkpass.substring(split * 4, split * 5) === "P%y4") {
            if (checkpass.substring(split * 2, split * 3) === "tSty") {
            if (checkpass.substring(split * 5, split * 6) === "5WZQ") {
              
                if (checkpass.substring(split * 7, split * 8) === "v#%}" ) {
                  alert("Password Verified")
                  }
                }
              }
      
            }
          }
        }
      }
    }
    else {
      alert("Incorrect password");
    }
    
  }
</script>
<div style="position:relative; padding:5px;top:50px; left:38%; width:350px; height:140px; background-color:#313244">
<div style="text-align:center; color:#cdd6f4">
<p>This is the secure login portal</p>
<p>Enter valid credentials to proceed</p>
<form action="index.html" method="post">
<input type="text" id="pass" size="8" />
<br/>
<input type="submit" value="verify" onclick="verify(); return false;" />
</form>
</div>
</div>
</body>
</html>
