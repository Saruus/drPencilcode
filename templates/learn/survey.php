

<?php
	//Connecting to sql db.
	$connect = mysqli_connect("localhost","root","DRPencilcode","drpencilcode");
	//Sending form data to sql db.
	mysqli_query($connect,"INSERT INTO survey (question1)
	VALUES ('$_POST[task1]')";
?>
