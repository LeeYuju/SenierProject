<?php
        if(isset($_POST["Token"])){

                $token = $_POST["Token"];
                //�����ͺ��̽��� �����ؼ� ��ū�� ����
                include_once 'config.php';
                $conn = mysqli_connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME);
                $query = "INSERT INTO token(Token) Values ('$token') ON DUPLICATE KEY UPDATE Token = '$token'; ";
                mysqli_query($conn, $query);

                mysqli_close($conn);
        }
?>
