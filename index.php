<?php $actual_link = (isset($_SERVER['HTTPS']) ? "https" : "http") . "://$_SERVER[HTTP_HOST]$_SERVER[REQUEST_URI]"; ?>
<html>
<head>
<meta http-equiv='refresh' content='2;url=<?php echo $actual_link; ?>'>
<?php
echo 'magento on EB <br/>';

echo 'Looking in the media folder...';

if ($handle = opendir('media')) {

    while (false !== ($entry = readdir($handle))) {

        if ($entry != "." && $entry != "..") {

            echo "$entry\n";
        }
    }

    closedir($handle);
}

?>
