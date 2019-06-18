<?php
   include_once 'config.php';
   $con=mysqli_connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME);

   $ID = $_GET['ID'];
   $PASSWORD = $_GET['PASSWORD'];
   $NAME = $_GET['NAME'];
   $AGE = $_GET['AGE'];
   $EMAIL = $_GET['EMAIL'];
   $DEVICE = $_GET['DEVICE'];

   $sql = "insert into userdata(ID,PASSWORD,NAME,AGE,EMAIL,DEVICE)
   values ('$ID','$PASSWORD','$NAME', '$AGE','$EMAIL','$DEVICE');"

   $result=mysqli_query($con,$sql);

   if ($result){
   echo "Values have been inserted successfully";
   }  else{
   echo mysqli_error($con);
   echo "Error";
   }
?>
