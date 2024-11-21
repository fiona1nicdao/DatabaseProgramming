<?php
    //Connect to database
    $hd = mysqli_connect("localhost", "dbuser", "user1", "db1")
     or die ("Unable to connect");

    //Execute sample query
    $res = mysqli_query($hd, "SELECT * FROM customer")
          or die ("Unable to run query");

    //Query number of rows in rowset
    $nrows = mysqli_num_rows($res);

    //Output
    echo "The query returned $nrows row(s):<br/>";

    //Iteration loop, for each row in rowset
	$nr = 0; 
    while ($row = mysqli_fetch_assoc($res))
    {
        $nr = $nr + 1;
		// Assigning variables from cell values
        $data1 = $row["title"];
        $data2 = $row["fname"];
        $data3 = $row["lname"];
        $data4 = $row["phone"];

        //Outputting data to browser
        echo "ROW# $nr : $data1 $data2 $data3 $data4 <br/>";
    }

    mysqli_close($hd);
?>

