let username = "pearlhacks10@bandwidth.com";
let user = "u-cnrexzgaxeihkdqvgh6qe7a";
let token = "t-l6hpngbf2sau4shhuyf2h2q";
let secret = "epsbmp6xw3u274mninwxr6mg4hlvsvcozpgsqgi";
let pass = "PjFfvrG4T8F6JVYf";
let base = "dC1sNmhwbmdiZjJzYXU0c2hodXlmMmgycTplcHNibXA2eHczdTI3NG1uaW53eHI2bWc0aGx2c3Zjb3pwZ3NxZ2k="

// Initialize Cloud Firestore through Firebase
var db = firebase.firestore();

function login(){
  let phrase = document.getElementById('passphrase').value;
  if(phrase=="drinkmorewater"){
    let html = `<br>
    <center class="blinking">Message: <br>
        <textarea id="message"style="width: 15rem; margin: 10px; text-align: center;" type="text"></textarea>
        <br> Target Zip Code:
        <input id="zip"style="width: 5rem; margin: 10px;" type="text">
        <br><button class = "blink" onclick="callBandwidth()">Send Message</button>

    </center>`;
    document.getElementById('admin_portal').innerHTML = html;
  }

}

async function getMessages(){
  var myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");
  myHeaders.append("Authorization", " Basic dC1sNmhwbmdiZjJzYXU0c2hodXlmMmgycTplcHNibXA2eHczdTI3NG1uaW53eHI2bWc0aGx2c3Zjb3pwZ3NxZ2k=");

  var requestOptions = {
    method: 'GET',
    headers: myHeaders,
    redirect: 'follow'
  };
  
  let res = await fetch("https://api.catapult.inetwork.com/v1/users/u-cnrexzgaxeihkdqvgh6qe7a/messages", requestOptions); 
  messages = await res.json();
  return messages;
}

async function callBandwidth(){
  let message = document.getElementById('message').value;
  if(message==""){
    message = "this is a TEST";
  }
  let zip = document.getElementById('zip').value;
  if(zip.length!=5){
    zip =27514;
  }else{
    zip = parseInt(zip);
  }
  // try {
  //   let request = await fetch('/data')
  //   subscriberInfo = JSON.parse(await request.json());

  //   let subscriberNumbers = []
  //   for (s in subscriberInfo["s"]) {
  //       loopMessage("+1" + String(subscriberInfo["s"][s]["number"]), message)
  //   }
    
  // } catch (error) {
  //     console.log(error);
  // }
  db.collection("subscribers").where("zip","==",zip).get().then((querySnapshot) => {
    querySnapshot.forEach((doc) => {
        console.log(`${doc.id} => ${doc.data().number}`);
        loopMessage(`${doc.data().number}`,message);
        //console.log(doc.getString('number'));
    });
  });
  
}

async function loopMessage(number, message){
  var myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");
  myHeaders.append("Authorization", " Basic dC1sNmhwbmdiZjJzYXU0c2hodXlmMmgycTplcHNibXA2eHczdTI3NG1uaW53eHI2bWc0aGx2c3Zjb3pwZ3NxZ2k=");

  var raw = JSON.stringify({
      "from":"+19195335013",
      "to": number,
      "text":message,
  });

  var requestOptions = {
  method: 'POST',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
  };

  let res = await fetch("https://api.catapult.inetwork.com/v1/users/u-cnrexzgaxeihkdqvgh6qe7a/messages", requestOptions);

}

async function pushNumber(){
    let num = document.getElementById("new_number").value;
    let zip = document.getElementById("new_zip").value;
    num = num.replace(/[^0-9]/g,'');
    zip = zip.replace(/[^0-9]/g,'');

    if(num.length==10){
      num = '+1'+num;
    }

    if(num.length == 12 && num.substring(1,2) == 1 && num.substring(num.length - 4, num.length - 7) != '555' && zip.length == 5){
        alert("Congrats.");
        if(document.getElementById('use_firebase').checked = true){
          db.collection("subscribers").add({
            number: num,
            zip: parseInt(zip),
          })
        }else{
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

        }
        
    } else {
        alert ("Please type in a valid zip code and phone number."); 
    }
  }

    function unsubscribe(){
      let num = document.getElementById("delete_num").value;
      num = num.replace(/[^0-9]/g,'');
      if(num.length==10){
        num = '+1'+num;
      }
      if(num.length == 12 && num.substring(1,2) == 1 && num.substring(num.length - 4, num.length - 7) != '555'){
        var delete_query = db.collection('subscribers').where('number','==',num);
        delete_query.get().then(function(querySnapshot) {
          querySnapshot.forEach(function(doc) {
            doc.ref.delete();
            alert("deleted "+num);
          });
        });
      }
  
    }



