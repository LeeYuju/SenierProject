<?php
        function send_notification ($tokens, $data)
        {
                $url = 'https://fcm.googleapis.com/fcm/send';
                $msg = array(
                        'body'  => $data["body"],
                        'title' => $data["title"],
                        "icon" => "myicon");

    echo $data["title"];
                echo $tokens;

                $fields = array(
                                'registration_ids'              => $tokens,
                                'notification'  => $msg
                        );

                $headers = array(
                        'Authorization:key =' . GOOGLE_API_KEY,
                        'Content-Type: application/json'
                        );

           $ch = curl_init();
     curl_setopt($ch, CURLOPT_URL, $url);
     curl_setopt($ch, CURLOPT_POST, true);
     curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
     curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
     //curl_setopt ($ch, CURLOPT_SSL_VERIFYHOST, 0);
     //curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
     curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($fields));
     $result = curl_exec($ch);
     if ($result === FALSE) {
          die('Curl failed: ' . curl_error($ch));
      }
     curl_close($ch);
     return $result;
        }
 ?>
