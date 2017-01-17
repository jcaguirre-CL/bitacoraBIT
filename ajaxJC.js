(function (global) {

	

	function getRequestObject() {
		if (window.XMLHttpRequest) {
			return (new XMLHttpRequest());
		}
		else if (window.ActiveXObject) {
			
			return (new ActiveXObject("Microsoft.XMLHTTP"));
		}
		else {
			global.alert("Ajax is not supported!");
			return(null);
		}

	}

var request = getRequestObject();
var myhandler = null;

/*function handleResponse(request,
						responseHandler,
						isJsonResponse) {
	console.log("********HR : request = " + request);
	console.log("********HR : responseHandler = " + responseHandler);
	console.log("********HR : isJsonResponse = " + isJsonResponse);
	if ((request.readyState == 4) &&
		(request.status == 200)) {

	if (isJsonResponse == undefined) {
		isJsonResponse = true;
	}
	if (isJsonResponse) {
		responseHandler(JSON.parse(request.responseText))
	}
	else {
		console.log("dentro del handleResponse");

		responseHandler(request.responseText);
	}
	}	
}*/

var compara = 0;

xmlJson = getRequestObject();

var auto = setInterval(function callTimer(){
	
console.log(xmlJson);

xmlJson.onreadystatechange=function(){

		if (xmlJson.readyState==4){
			if (xmlJson.status==200){
				respu = JSON.parse(xmlJson.responseText)
/*				if (compara==respu.clip){
					console.log("progreso se mantiene");
				}
				else {
					console.log("progreso cambia" + compara);
					compara = respu.progreso;
				}*/
				//var barrita = document.getElementById("barraInterna"+respu.output);
				document.getElementById("clip"+respu.output).innerHTML=respu.clip;
				document.getElementById("inicio"+respu.output).innerHTML=respu.inicio;
				document.getElementById("barraInterna"+respu.output).style.width = respu.progreso + '%';
				//barrita.style.width = respu.progreso + '%';
				document.getElementById("progresoLabel"+respu.output).innerHTML=respu.progreso;
				//document.getElementById("estado").innerHTML=respu.estado;
				switch (respu.estado)
				{
					case 0 : document.getElementById("estado"+respu.output).innerHTML="Activo";
					break;
					case 1 : document.getElementById("estado"+respu.output).innerHTML="Ok";
					break;
					case 2 : document.getElementById("estado"+respu.output).innerHTML="Error";
					break;
				}
				switch (respu.output)
				{
					case 1 : document.getElementById("output"+respu.output).innerHTML="A";
					break;
					case 2 : document.getElementById("output"+respu.output).innerHTML="B";
					break;
					case 3 : document.getElementById("output"+respu.output).innerHTML="C";
					break;
					case 4 : document.getElementById("output"+respu.output).innerHTML="D";
					break;
				}
				//document.getElementById("output").innerHTML=respu.output;
				//console.log("jsonautoupdate");
			}
		}
	}
	xmlJson.open("GET", "progreso.json", true);
//xmlJson.timeout = 500;
	xmlJson.send();


}, 1000);

})(window);


