<?php
  require_once "vendor/autoload.php";
  define('CHUNK_SIZE', 1024*1024);
  $log = "Begin! \n";
  $key = "qc16DVI315KSG2bP65Oz747V6f95tM0m";
  $loginName = $loginPassword = $response = "";

  //Create a checkInput method to protect againt injection
  function checkInput($data){
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data);
    return $data;
  }

  //Connect to the database
  function connectToDb(){
    return mysqli_connect("localhost", "cs3041", "iHeartTcp", "CS3041");
  }

  //Function to automate hashing, where data is the plain text password
  //Concatenated with a unique hash
  function hashPass($data){
    return hash("md5", $data);
  }

  //Generate a unique 16 character salt
  function generateSalt(){
    return base64_encode(openssl_random_pseudo_bytes(16));
  }

  //Retrieve a users salt from the password, assuming he is a valid user
  function getUserSalt($user){
    $query = sprintf("SELECT salt FROM users WHERE name='%s'", $user);
    $conn = connectToDb();
    if($conn){
      $result = mysqli_query($conn, $query);
      if($result){
        $res = $result->fetch_row();
        return $res[0];
      }else{
        die("Failed To Get Salt");
      }
    }
  }

  //Get the users hashed password from the database, assuming it is
  //a valid user
  function getUserPassword($user){
    $query = sprintf("SELECT hash FROM users WHERE name='%s'", $user);
    $conn = connectToDb();
    if($conn){
      $result = mysqli_query($conn, $query);
      if($result){
        $res = $result->fetch_row();
        return $res[0];
      }else{
        die("Failed");
      }
    }
  }

  //Important to make sure user exists before performing user operations
  function checkUserExists($name){
    $query = sprintf("SELECT name FROM users WHERE name='%s'", $name);
    $conn = connectToDb();
    if($conn){
      $result = mysqli_query($conn, $query);
      $numRows = $result->num_rows;
      if($numRows > 0){
        return true;
      }else{
        return false;
      }
    }
  }

  //Check if a user has admin privileges. This is necessary for when adding
  //and removing users
  function isAdminLevel($user){
    $query = sprintf("SELECT admin FROM users WHERE name='%s'", $user);
    $conn = connectToDb();
    if($conn){
      $result = mysqli_query($conn, $query);
      if($result){
        $res = $result->fetch_row();
        if($res[0] == "yes"){
          return True;
        }else{
          return False;
        }
      }else{
        die("Insufficient Permissions to carry out this operation");
      }
    }
  }

  //Used to add a new user to the encrypted group
  function addUser($name, $salt, $hash, $admin){
    if(checkUserExists($name)){
      die("This username is already taken");
    }
    $query = sprintf("INSERT INTO users (name, salt, hash, admin) VALUES ('%s','%s','%s','%s')",
                  $name, $salt, $hash, $admin);
    $conn = connectToDb();
    if($conn){
      return mysqli_query($conn, $query);
    }else{
      die("Failed to connect to Database");
    }
  }

  function removeUser($name){
    if(!checkUserExists($name)){
      die("This user does not exist");
    }
    $query = sprintf("DELETE FROM users WHERE name='%s'", $name);
    $conn = connectToDb();
    if($conn){
      return mysqli_query($conn, $query);
    }else{
      die("Failed to connect to Database");
    }
  }

  //This function gets the encrypted hash from the database and compares it
  //with the generated hash from user inputted password and retrieved salt
  function verifyLogin($name, $pass){
    $salt = getUserSalt($name);
    $hashedInputPass = hashPass($pass . $salt);
    $storedPass = getUserPassword($name);
    return ($hashedInputPass == $storedPass);
  }

  function returnKeys(){
    die("qc16DVI315KSG2bP65Oz747V6f95tM0m");
  }

  //Function list directory to user
  function returnDirectory(){
    $dir = scandir("uploads/");
    return $dir;
  }

  //Download requested file
  function downloadFile($file, $retbytes=TRUE){
    $buffer = '';
    $cnt =0;
    $file = "uploads/".$file;
    // $handle = fopen($filename, 'rb');
    $handle = fopen($file, 'rb');
    if ($handle === false) {
      return false;
    }
    while (!feof($handle)) {
      $buffer = fread($handle, CHUNK_SIZE);
      echo $buffer;
      ob_flush();
      flush();
      if ($retbytes) {
        $cnt += strlen($buffer);
      }
    }
    $status = fclose($handle);
    if ($retbytes && $status) {
      return $cnt; // return num. bytes delivered like readfile() does.
    }
  }

  function uploadFile(){
    $targetName="";
    if(!empty($_FILES["file"])){
      $targetDir = "uploads/";
      $name = basename($_FILES["file"]["name"]);
      $targetName = $targetDir . $name;
      $uploadOk = TRUE;
      $imageFileType = strtolower(pathinfo($targetName, PATHINFO_EXTENSION));
      $check = filesize($_FILES["file"]["tmp_name"]);
      if($check!==FALSE){
        move_uploaded_file($_FILES["file"]["tmp_name"], $targetName) or die("Error uploading file to server");
        die("Successfully uploaded file");
      }else{
        die("Please upload a valid file");
      }
    }else{
      die("No file found");
    }
  }

  //Only run any of the processing functions when the request method is
  //POST
  if($_SERVER["REQUEST_METHOD"] == "POST"){
    //First we find out what operation the user wanted to perform
    $requestType;
    if(!empty($_POST["RequestType"])){
      $requestType = checkInput($_POST["RequestType"]);
      $log = $log . "Got Request type: " . $requestType . "\n";
    }else{
      die("Request Type must be specified");
    }

    //We use a switch statement to check the possible operations requested by
    //The user
    switch($requestType){
      case "LOGIN":
        //When it's a case of logging in, we want to retrieve the salt,
        //hash the inputted password, then check it against the existing hash
        //First we must parse user name and password
        $name = $pass = $response = "";
        if((!empty($_POST["name"])) && (!empty($_POST["password"]))){
          $name = checkInput($_POST["name"]);
          $pass = checkInput($_POST["password"]);
          if(verifyLogin($name, $pass)){
            if(isAdminLevel($name)){
              die("y");
            }else{
              die("n");
            }
          }else{
            die("Incorrect username/password");
          }
        }else{
          die("Username and Password fields cannot be left blank");
        }
        break;

      case "CREATE":
        //When it's the case of creating a user, we want to verify the user
        //Then we create a salt, create a hash, and store all three in the DB
        //First we verify the users login details
        $name = $pass = "";
        if((!empty($_POST["name"])) && (!empty($_POST["password"]))){
          $name = checkInput($_POST["name"]);
          $pass = checkInput($_POST["password"]);
          $authenticated = verifyLogin($name, $pass);
        }else{
          die("Username and Password Fields cannot be left blank");
        }

        //Next we verify the user is an admin and add the new user if he is
        if($authenticated){
          $privileged = isAdminLevel($name);
          if($privileged && (!empty($_POST["newName"])) && (!empty($_POST["newPass"])) && (!empty($_POST["admin"]))){
            $salt = generateSalt();
            $newName = checkInput($_POST["newName"]);
            $newPass = checkInput($_POST["newPass"]);
            $admin = checkInput($_POST["admin"]);
            $hashedPass = hashPass($newPass . $salt);
            //Add the user
            if(addUser($newName, $salt, $hashedPass, $admin)){
              die("Successfully created new user");
            }else{
              die("An error occured while creating the new user");
            }
          }else{
            if($privileged){
              die("One or more fields were missing");
            }else{
              die("Insufficient permissions to carry out this action");
            }
          }
        }else{
          die("Incorrect username/password");
        }
        break;

      case "REMOVE":
        //Another scenario is that an admin wants to remove a user from the group
        //First we must verify the person making the request has the permissions to do so
        //Then we must check the user exists
        $name = $pass = "";
        if((!empty($_POST["name"])) && (!empty($_POST["password"]))){
          $name = checkInput($_POST["name"]);
          $pass = checkInput($_POST["password"]);
          $authenticated = verifyLogin($name, $pass);
        }else{
          die("Username and Password fields cannot be left blank");
        }

        //If the user is authenticated, continue with removal of other user
        if($authenticated){
          $privileged = isAdminLevel($name);
          if($privileged && (!empty($_POST["removalName"]))){
            $removalName = checkInput($_POST["removalName"]);
            if(removeUser($removalName)){
              die("User successfully removed");
            }else{
              die("There was an error removing the specified user");
            }
          }else{
            if($privileged){
              die("Must enter the name of user to be removed");
            }else{
              die("Insufficient permissions to remove user");
            }
          }
        }else{
          die("Incorrect username/password");
        }
        break;

      case "getKey":
        $name = $pass = "";
        if(!empty($_POST["name"]) && !empty($_POST["password"])){
          $name = checkInput($_POST["name"]);
          $password = checkInput($_POST["password"]);
          if(verifyLogin($name, $password)){
            returnKeys();
          }else{
            die("Incorrect username password combination");
          }
        }else{
          die("Username or password cannot be blank");
        }
        break;

      case "listDirectory":
        $name = $pass = "";
        if(!empty($_POST["name"]) && !empty($_POST["password"])){
          $name = checkInput($_POST["name"]);
          $pass = checkInput($_POST["password"]);
          if(verifyLogin($name, $pass)){
            echo implode(",", returnDirectory());
          }else{
            die("Incorrect Username/Password Combination");
          }
        }
        break;

      case "uploadFile":
        $name = $pass = "";
        if(!empty($_POST["name"]) && !empty($_POST["password"])){
          $name = checkInput($_POST["name"]);
          $pass = checkInput($_POST["password"]);
          if(verifyLogin($name, $pass)){
            uploadFile();
          }
        }
        break;

      default:
        die("Valid operation not specified");
    }
  }elseif($_SERVER["REQUEST_METHOD"] == "GET" && !empty($_GET["file"])){
    #If a file has been requested for download, serve it
      $file = basename(checkInput($_GET["file"]));
      downloadFile($file);
  }else{
    die("<h1>Error, Unauthorized Access</h1><br><hr><p>An attempt at Unauthorized access to this page has been made. Details of this incident have been
    passed on to the admin");
  }
 ?>
