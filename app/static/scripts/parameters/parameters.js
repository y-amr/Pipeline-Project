function uuidv4() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}
function stripTrailingSlash(str) {
    if(str.substr(-1) === '/') {
        return str.substr(0, str.length - 1);
    }
    return str;
}

function generateRandomToken(idInput){
    document.getElementById(idInput).value = uuidv4();
}

function generateEndpoint(){
    if(document.getElementById("ENDPOINT").value === ""){
        alert("Please fill endpoint")
    }else{
        const url = stripTrailingSlash(document.getElementById("ENDPOINT").value);
        const version = "2.1.1"

        document.getElementById("ENDPOINT_211_CPO_TOKENS").value = url + "/ocpi/cpo/"+version+"/tokens";
        document.getElementById("ENDPOINT_211_EMSP_TOKENS").value = url + "/ocpi/emsp/"+version+"/tokens";

        document.getElementById("ENDPOINT_211_CPO_CDRS").value = url + "/ocpi/cpo/"+version+"/cdrs";
        document.getElementById("ENDPOINT_211_EMSP_CDRS").value = url + "/ocpi/emsp/"+version+"/cdrs";

        document.getElementById("ENDPOINT_211_CPO_SESSIONS").value = url + "/ocpi/cpo/"+version+"/sessions";
        document.getElementById("ENDPOINT_211_EMSP_SESSIONS").value = url + "/ocpi/emsp/"+version+"/sessions";

        document.getElementById("ENDPOINT_211_CPO_LOCATIONS").value = url + "/ocpi/cpo/"+version+"/locations";
        document.getElementById("ENDPOINT_211_EMSP_LOCATIONS").value = url + "/ocpi/emsp/"+version+"/locations";

        document.getElementById("ENDPOINT_211_CPO_COMMANDS").value = url + "/ocpi/cpo/"+version+"/commands";
        document.getElementById("ENDPOINT_211_EMSP_COMMANDS").value = url + "/ocpi/emsp/"+version+"/commands";

        document.getElementById("ENDPOINT_211_CPO_SESSIONS").value = url + "/ocpi/cpo/"+version+"/sessions";
        document.getElementById("ENDPOINT_211_EMSP_SESSIONS").value = url + "/ocpi/emsp/"+version+"/sessions";

        document.getElementById("ENDPOINT_211_CPO_VERSIONS").value = url + "/ocpi/cpo/versions";
        document.getElementById("ENDPOINT_211_EMSP_VERSIONS").value = url + "/ocpi/emsp/versions";

        document.getElementById("ENDPOINT_211_CPO_CREDENTIALS").value = url + "/ocpi/cpo/"+version+"/credentials";
        document.getElementById("ENDPOINT_211_EMSP_CREDENTIALS").value = url + "/ocpi/emsp/"+version+"/credentials";

        document.getElementById("ENDPOINT_211_CPO_TARIFFS").value = url + "/ocpi/cpo/"+version+"/tariffs";
        document.getElementById("ENDPOINT_211_EMSP_TARIFFS").value = url + "/ocpi/emsp/"+version+"/tariffs";


    }

}