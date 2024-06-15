<?php

// Include PHPMailer library
require '../assets/vendor/phpmailer/PHPMailerAutoload.php';

class PHP_Email_Form {
    private $to = 'info@voxvents.com'; // Change this to your receiving email address
    private $from_name = '';
    private $from_email = '';
    private $subject = '';
    private $message = '';
    private $mail;

    public function __construct() {
        $this->mail = new PHPMailer();
    }

    public function sendEmail($from_name, $from_email, $subject, $message) {
        // Set PHPMailer to use SMTP
        $this->mail->isSMTP();
        
        // SMTP configuration
        $this->mail->Host = 'smtp.yourprovider.com'; // Change this to your SMTP server host
        $this->mail->SMTPAuth = true;
        $this->mail->Username = 'your_smtp_username'; // Change this to your SMTP username
        $this->mail->Password = 'your_smtp_password'; // Change this to your SMTP password
        $this->mail->SMTPSecure = 'tls'; // Change if your SMTP server requires different encryption
        $this->mail->Port = 587; // Change if your SMTP server uses a different port

        // Sender and recipient details
        $this->mail->setFrom($from_email, $from_name);
        $this->mail->addAddress($this->to);
        $this->mail->Subject = $subject;
        $this->mail->Body = $message;

        // Send email
        if ($this->mail->send()) {
            return true;
        } else {
            return false;
        }
    }
}

// Process form submission
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Initialize PHP_Email_Form object
    $contact = new PHP_Email_Form();

    // Retrieve form data
    $name = $_POST['name'] ?? '';
    $email = $_POST['email'] ?? '';

    // Compose email subject and message
    $subject = "New Subscription: " . $email;
    $message = "Email: " . $email;

    // Send email
    if ($contact->sendEmail($name, $email, $subject, $message)) {
        echo 'Email sent successfully!';
    } else {
        echo 'Error sending email. Please try again later.';
        // Uncomment below line for debugging
        // echo $contact->mail->ErrorInfo;
    }
}

?>
