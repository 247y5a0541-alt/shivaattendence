let video = document.getElementById("video");

function startCamera(){
navigator.mediaDevices.getUserMedia({video:true})
.then(stream=>{
video.srcObject = stream;
});
}

function capture(){
alert("Image Captured");
}