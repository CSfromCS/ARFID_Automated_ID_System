exitCard = "CC B4 C4 E9";
emailCard = "2C 3A BD E9";


function updateInfo(data){
	if(data){
		student = data[0];
		hasTapped = data[1];
		var pictureTag = document.getElementById('tapPic');
		pictureTag.style.display = "none";
		pictureTag.src = "Images/" + student[0] + ".jpg";
		document.getElementById('name').value = student[3] + " " + student[2];
		document.getElementById('section').value = student[6];
		document.getElementById('err').innerHTML = "";	
		pictureTag.style.display = "block";
	/*	if(hasTapped == true){
			document.getElementById('time').value = "You have already tapped today.";
		}else{	*/
			d = new Date();
			document.getElementById('time').value = "Time in: " + d.toLocaleTimeString() + " " + d.toDateString();
			if(student[8].indexOf('nan') == -1){
				console.log(student[8]);
				document.getElementById('err').innerHTML = "Sendng message...";
				document.getElementById('myModal').style.display = "block";
				eel.callSendSMS()(smsResultDisplay)				
			}else{
				document.getElementById('err').innerHTML = "No Guardian number found.";				
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
		document.getElementById('err').innerHTML = "Message sent!";	
		console.log("Message sent!")
	}else{
		document.getElementById('err').innerHTML = "Error in sending message.";	
		console.log("Error in sending message.")
	}
	document.getElementById('myModal').style.display = "none";
}
	
function scan(){
	console.log("Scanning...");
	eel.callScan()(startStudentPage);
}	
	
function startStudentPage(rfid){
	if(rfid == exitCard){			//Exit Key Card
		window.location="Index.html";	/*
	}else if(rfid == "8C 28 C2 E9"){	//Ma'am Dian 
		data = [[pic, 1, lastName, firstName, 4, 5, section], 2, [number, message]];
		updateInfo(data);
	}else if(rfid == "CC 0B C4 E9"){	//Sir SJ
	}else if(rfid == "EC A3 BE E9"){	//Ma'am Lau	*/
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
	}else{
		document.getElementById('message').innerHTML = "Error: " + result[1];
	}
}