<?php
   include_once 'config.php';
   $con=mysqli_connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME);

   $ID = $_GET['ID'];

   $sql = "delete from userdata where ID = '$ID'";

   $result=mysqli_query($con,$sql);

   if ($result){
   echo "Values have been deleted successfully";
   }  else{
   echo mysqli_error($con);
   echo "Error";
   }
?>
