<?php
$errors = '';
$myemail = 'pricklprickl@gmail.com';
$pricklmail = 'hello@prickl.com';
if(empty($_POST['name'])  || 
   empty($_POST['email']) || 
   empty($_POST['message']))
{
    $errors .= "\n Error: Fields cannot be empty!";
    $_SESSION['error'] = 'Fields cannot be empty!';
    header('Location: https://prickl.com/pg/error_fd.html');
    exit(); 
}


$name = $_POST['name']; 
$email_address = $_POST['email']; 
$message = $_POST['message']; 

if (!preg_match(
"/^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,3})$/i", 
$email_address))
{
    $errors .= "\n Error: Invalid email address";
    $_SESSION['error'] = 'Invalid email address';
    header('Location: https://prickl.com/pg/error_em.html');
    exit();
}

if( empty($errors))

{

$to = $myemail;

$email_subject = "CHEEKY enquiry from $name";

$email_body = "CHEEKY enquiry message from \n\n Name: $name : \n\n Email: $email_address \n \n\n Message: \n\n $message \n \n ".


$headers = "From: $pricklmail\n";

$headers .= "Reply-To: $email_address";

mail($to,$email_subject,$email_body,$headers);

//redirect to the 'thank you' page

header('Location: https://prickl.com/pg/thanks.html');

}



?>