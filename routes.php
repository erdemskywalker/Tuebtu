<?php
include "TemplateEngine.php";
session_start();

$template = new TemplateEngine(__DIR__ . '/views');

$routes = [
    '' => 'main'
];


function main() {
    global $template;
    echo $template->render('main');
}





