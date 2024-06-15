<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Validate and sanitize inputs
    $artist_id = $_POST['artist_id'];
    $booking_date = $_POST['booking_date'];
    $event_name = $_POST['event_name'];
    $event_location = $_POST['event_location'];
    $event_price = $_POST['event_price'];
    $additional_details = $_POST['additional_details'];

    // Example validation (you may need more robust validation)
    if (empty($artist_id) || empty($booking_date) || empty($event_name) || empty($event_location) || empty($event_price)) {
        echo "Please fill in all required fields.";
        exit;
    }

    // Process the booking (insert into database, send notifications, etc.)
    // Example database insertion (you need to implement your database connection and insertion logic)
    $servername = "localhost";
    $username = "username";
    $password = "password";
    $dbname = "your_database";

    // Create connection
    $conn = new mysqli($servername, $username, $password, $dbname);

    // Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    // Prepare SQL statement
    $stmt = $conn->prepare("INSERT INTO bookings (artist_id, booking_date, event_name, event_location, event_price, additional_details) VALUES (?, ?, ?, ?, ?, ?)");
    $stmt->bind_param("isssis", $artist_id, $booking_date, $event_name, $event_location, $event_price, $additional_details);

    // Execute SQL statement
    if ($stmt->execute()) {
        echo "Booking request sent successfully!";
    } else {
        echo "Failed to send booking request. Please try again later.";
    }

    // Close connection
    $stmt->close();
    $conn->close();
}
?>
