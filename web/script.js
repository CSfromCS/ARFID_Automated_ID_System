exitCard = "CC B4 C4 E9";
emailCard = "2C 3A BD E9";
absentCard = "5C DD B5 E9";

var time = 0;

function updateInfo(data){
	if(data){
		student = data[0];
		hasTapped = data[1];
		var pictureTag = document.getElementById('tapPic');
		document.getElementById('tapPic').src = "Images/" + student[0] + ".jpg";
		document.getElementById('name').value = student[3] + " " + student[2];
		document.getElementById('section').value = student[6];
		document.getElementById('err').innerHTML = "";
	/*	if(hasTapped == true){
			document.getElementById('time').value = "You have already tapped today.";
		}else{ */
			d = new Date();
			document.getElementById('time').value = "Time in: " + d.toLocaleTimeString() + " ---- " + d.toDateString();
			if(student[8].indexOf('nan') == -1){
				console.log(student[8]);
				document.getElementById('err').innerHTML = "Sendng message...";
				document.getElementById('modalInfo').innerHTML = "Sending message to "+student[7]+"...";
				document.getElementById('myModal').style.display = "block";
				eel.callSendSMS()(smsResultDisplay);
			}else{
				document.getElementById('modalInfo').innerHTML = "Guardian number could not be found.";
				document.getElementById('myModal').style.display = "block";
				document.getElementById('err').innerHTML = "No Guardian number found.";
				setTimeout(function(){document.getElementById('myModal').style.display = "none"}, 1000);			
			}
		//}
	}else{
		console.log(data);
		document.getElementById('tapPic').src = "Images/blank.jpg";
		document.getElementById('name').value = "Unknown rfid, please register card.";
		document.getElementById('section').value = "";
		document.getElementById('time').value = "";
	}
	scan();
}
function smsResultDisplay(result){
	if(result){
		document.getElementById('modalInfo').innerHTML = "Message sent!";
		document.getElementById('err').innerHTML = "Message sent!";	
		console.log("Message sent!")
	}else{
		document.getElementById('modalInfo').innerHTML = "Error in sending message!";
		document.getElementById('err').innerHTML = "Error in sending message.";	
		console.log("Error in sending message.")
	}
	setTimeout(function(){document.getElementById('myModal').style.display = "none"}, 800);
}
	
function textAbsents(students){
	resetTimer()
	if(students){
		document.getElementById('myModal').style.display = "block";
		console.log("Modal open");
		student = students[0];
		console.log(student);
		document.getElementById('modalInfo').innerHTML = "Sending message for "+student[2]+".<br>"+students.length+" left.";
		document.getElementById('tapPic').src = "Images/" + student[0] + ".jpg";
		document.getElementById('name').value = student[3] + " " + student[2];
		document.getElementById('section').value = student[6];
		document.getElementById('err').innerHTML = "";	
		eel.callSendAbsentSMS(students)(textAbsents);
	}else{
		document.getElementById('myModal').style.display = "block";
		document.getElementById('modalInfo').innerHTML = "Everyone received messages today!";
		console.log("Everyone has tapped today!");
		document.getElementById('tapPic').src = "Images/blank.jpg";
		document.getElementById('name').value = "";
		document.getElementById('section').value = "";
		document.getElementById('err').innerHTML = "Everyone received messages today!";
		setTimeout(function(){document.getElementById('myModal').style.display = "none"}, 800);
		scan();
	}
}
	
function scan(){
	resetTimer()
	console.log("Scanning...");
	eel.callScan()(startStudentPage);
}
function clear() {
		console.log("Screen cleared.");
		document.getElementById('tapPic').src = "Images/blank.jpg";
		document.getElementById('name').value = "";
		document.getElementById('section').value = "";
		document.getElementById('time').value = "";
		document.getElementById('err').innerHTML = "Idle.";
		document.getElementById('myModal').style.display = "none";
    }	
function resetTimer() {	
        clearTimeout(time);
        time = setTimeout(clear, 10000)
    }
	
function startStudentPage(rfid){
	if(rfid == exitCard){
		window.location="Index.html";
	}else if(rfid == absentCard){
		eel.callSearchAbsents()(textAbsents);
	}else{
		eel.callStudentPage(rfid)(updateInfo);
	}
}



function startSendPage(){
	document.getElementById('backButton').style.display = "none";
	eel.callScan()(checkEmailCard)
}

function checkEmailCard(rfid){
	if(rfid == emailCard){
		document.getElementById('message').innerHTML = "Sending emails...";
		document.getElementById('modalInfo').innerHTML = "Creating excel files, sending emails...<br>Please wait.";
		document.getElementById('myModal').style.display = "block";
		eel.callSendToTeachers()(displayEmailPage);
	}else if(rfid == exitCard){
		window.location="Index.html";
	}else{
		document.getElementById('message').innerHTML = "Error: Incorrect Email Key Card";
		startSendPage();
	}
}

function displayEmailPage(result){
	document.getElementById('backButton').style.display = "block";
	console.log(result)
	if(result == true){
		document.getElementById('message').innerHTML = "Success! Emails sent.";
		document.getElementById('modalInfo').innerHTML = "Success! Emails sent.";
	}else{
		document.getElementById('message').innerHTML = "Error: " + result[1];
		document.getElementById('modalInfo').innerHTML = "Error: " + result[1];
	}
	setTimeout(function(){document.getElementById('myModal').style.display = "none"}, 800);
}