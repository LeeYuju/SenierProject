<?php
include_once 'config.php';
$con=mysqli_connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME);


$deviceId = $_GET['deviceId'];
$token = $_GET['token'];

$sql="UPDATE token SET deviceId = '$deviceId' WHERE Token = '$token'";

if (mysqli_query($con,$sql))
{
   echo "Values have been inserted successfully";
}
?>
