

 window.onload = function(){

 var video = document.getElementById('video');
if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    stream = navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
        video.srcObject = stream;
        video.play();
    });
}
var canvas = document.getElementById('canvas');
var context = canvas.getContext('2d');
var video = document.getElementById('video');

document.getElementById("snap").addEventListener("click", function() {
	document.getElementById("canvas").height = "240";
	context.drawImage(video, 0, 0, 320, 240);

	 document.getElementById("id_hiddenimage").value = canvas.toDataURL();
});

document.getElementById("login-submit").addEventListener("click", function() {
	context.drawImage(video, 0, 0, 320, 240);
	 document.getElementById("id_hiddenimage").value = canvas.toDataURL();
});

}

