function pushNumber(){
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
    } else {
        alert ("Please type in a valid zip code and phone number."); 
    }
}
