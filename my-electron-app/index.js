document.getElementById("myButton").addEventListener("click", greeting);

function greeting(){
    var name = document.getElementById("myName").value;
    document.getElementById("greet").innerHTML = "Hello " + name + " !";
}