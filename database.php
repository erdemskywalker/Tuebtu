<?php

$host = 'localhost'; 
$dbname = ''; 
$username = ''; 
$password = ''; 

$db = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8", $username, $password);
$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

?>