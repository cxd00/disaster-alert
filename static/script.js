let user = "u-cnrexzgaxeihkdqvgh6qe7a";
let token = "t-l6hpngbf2sau4shhuyf2h2q";
let secret = "epsbmp6xw3u274mninwxr6mg4hlvsvcozpgsqgi";
let pass = "PjFfvrG4T8F6JVYf";
let base = "dC1sNmhwbmdiZjJzYXU0c2hodXlmMmgycTplcHNibXA2eHczdTI3NG1uaW53eHI2bWc0aGx2c3Zjb3pwZ3NxZ2k="

async function callBandwidth(){
  try {
    let dt = await fetch('/data')
    console.log(dt)
    dt = await dt.json()
    console.log(dt)
    
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    myHeaders.append("Authorization", " Basic dC1sNmhwbmdiZjJzYXU0c2hodXlmMmgycTplcHNibXA2eHczdTI3NG1uaW53eHI2bWc0aGx2c3Zjb3pwZ3NxZ2k=");

    var raw = JSON.stringify({"from":"+19195335013","to":"+19105995176","text":"bump it"});

    var requestOptions = {
    method: 'POST',
    headers: myHeaders,
    body: raw,
    redirect: 'follow'
    };

    let res = await fetch("https://api.catapult.inetwork.com/v1/users/u-cnrexzgaxeihkdqvgh6qe7a/messages", requestOptions);

    console.log(res);
  } catch (error) {
      console.log(error);
  }
  
}

async function pushNumber(){
    let num = document.getElementById("new_number").value;
    let zip = document.getElementById("new_zip").value;
    num = num.replace(/[^0-9]/g,'');
    zip = zip.replace(/[^0-9]/g,'');
    console.log(num);
    console.log(zip);

    if(((num.length == 11 && num.substring(0,1) == 1) || num.length == 10)
    && num.substring(num.length - 4, num.length - 7) != '555' 
    && zip.length == 5){
        console.log(num);
        console.log(zip);
        alert("Congrats.");
        data = {
          "number" : num,
          "zip" : zip 
        }

        let url = new URL("http://127.0.0.1:5000/subscriber/")
        let params = {number: num, zip: zip}
        url.search = new URLSearchParams(params).toString();
        await fetch(url, {
          method : "POST"
        })

        callBandwidth();
        
    } else {
        alert ("Please type in a valid zip code and phone number."); 
    }

}

