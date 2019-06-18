<?php
include_once 'config.php';
$link=mysqli_connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME);
if (!$link)
{
    echo "MySQL ���� ���� : ";
    echo mysqli_connect_error();
    exit();
}

mysqli_set_charset($link,"utf8");

$ID = $_GET['ID'];

$sql="select * from userdata where ID = '$ID'";

$result=mysqli_query($link,$sql);
$data = array();
if($result){
    while($row=mysqli_fetch_array($result)){
        array_push($data,
            array(
            'ID'=>$row[1],
            'PASSWORD'=>$row[2],
            'NAME'=>$row[3],
            'AGE'=>$row[4],
            'EMAIL'=>$row[5],
            'DEVICE'=>$row[6]
        ));
    }

    header('Content-Type: application/json; charset=utf8');
    $json = json_encode(array("webnautes"=>$data), JSON_PRETTY_PRINT+JSON_UNESCAPED_UNICODE);

    echo to_han($json);

}
else{
    echo "SQL�� ó���� ���� �߻� : ";
    echo mysqli_error($link);
}

function han ($s) { return reset(json_decode('{"s":"'.$s.'"}')); }

function to_han ($str) { return preg_replace('/(\\\u[a-f0-9]+)+/e','han("$0")',$str); }


mysqli_close($link);

?>
