var xmlhttp = new XMLHttpRequest();
xmlhttp.timeout = 1e9;

ip_add = '131.179.6.39';
ip_port = 'http://' + ip_add + ':8000';

xmlhttp.onreadystatechange = function () {
    if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
        console.log('server response: ' + xmlhttp.responseText);
    }
}

function lamp_up() {
	var msg = "lamp_up"
	xmlhttp.open('POST', ip_port, true);
	xmlhttp.send(msg);
}

function lamp_down() {
	var msg = "lamp_down"
	xmlhttp.open('POST', ip_port, true);
	xmlhttp.send(msg);
}

function trash_open() {
	var msg = "trash_open"
	xmlhttp.open('POST', ip_port, true);
	xmlhttp.send(msg);
}

function trash_close() {
	var msg = "trash_close"
	xmlhttp.open('POST', ip_port, true);
	xmlhttp.send(msg);
}
// xmlhttp.open('POST', 'http://localhost:8000', true);
// xmlhttp.send();







// xmlhttp.open("POST", "http://localhost:8080/", true);
// // xmlhttp.responseType = "arraybuffer";
// xmlhttp.setRequestHeader("Content-type", "text/html");
// xmlhttp.send("this is");


// sendImageFromCanvas();

// context.drawImage(document.getElementById("testimg"), 0, 0);
// var imgData = context.getImageData(0, 0, canvas.width, canvas.height);
// context.putImageData(imgData, 0, 0);
// xmlhttp.open('POST', 'http://localhost:8000', true);
// xmlhttp.setRequestHeader("Content-type", "text/html");
// xmlhttp.send();

// downloadFile("test.jpg", file);

// var imgData = file.split(",")[1];
// saveAs(imgData, "test.jpg");

// function dataURLtoFile(dataurl, filename) {
//     var arr = dataurl.split(','), mime = arr[0].match(/:(.*?);/)[1],
//         bstr = atob(arr[1]), n = bstr.length, u8arr = new Uint8Array(n);
//     while(n--){
//         u8arr[n] = bstr.charCodeAt(n);
//     }
//     return new File([u8arr], filename, {type:mime});
// }

// var file1 = dataURLtoFile(file, 'test.jpg');

// function okbtn1(){
// 	var msg;
// 	msg = "ok"
// 	xmlhttp.open('POST', 'http://localhost:8080/figures', true);
// 	xmlhttp.send(msg);
// 	if (ok_num == 0){
// 		$("#instruction").val("press \"ok!\" again");
// 		ok_num+=1;
// 	} else {
// 		$("#instruction").val("press \"save cad img\" to save the img");
// 	}
// }



