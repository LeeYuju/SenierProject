<?php
   include_once 'config.php';
   $con=mysqli_connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME);

   $deviceId = $_GET['deviceId'];
   $dust = $_GET['dust'];


   include_once('push_notification.php');
   include_once 'config.php';
   $conn = mysqli_connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME);
   $sql = "Select Token From token where deviceId = '$deviceId'";
   $result = mysqli_query($conn,$sql);
   $tokens = array();
   if(mysqli_num_rows($result) > 0 ){
        while ($row = mysqli_fetch_assoc($result)) {
                $tokens[] = $row["Token"];
                  }
   }
   mysqli_close($conn);

   $Tmsg = "미세먼지 수치가 매우 높습니다!";
   $Bmsg = $dust."µg/m3";

   $inputData = array("title" => $Tmsg, "body" => $Bmsg);
   $result = send_notification($tokens,$inputData);
   echo $result;

?>
