<?php

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $contact = new PHP_Email_Form;

    // Set form data
    $contact->to = 'info@voxvents.com';
    $contact->from_name = $_POST['name'] ?? '';
    $contact->from_email = $_POST['email'] ?? '';
    $contact->subject = "New Subscription: " . ($_POST['email'] ?? '');

    // Add message to email body
    $contact->add_message($_POST['email'] ?? '', 'Email');

    // Attempt to send email
    if ($contact->send()) {
        echo 'Email sent successfully!';
    } else {
        echo 'Error sending email. Please try again later.';
        // Optionally, you can uncomment the line below for debugging:
        // echo $contact->error();
    }
}

?>
