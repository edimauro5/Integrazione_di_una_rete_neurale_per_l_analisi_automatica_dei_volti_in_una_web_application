function formcheck_reg(modulo) {
    if (modulo.password2.value == "") {
        alert("Confermare la password");
        document.reg.password2.focus();
        return false;
    }
    if (modulo.password1.value != document.reg.password2.value) {
        alert("La conferma della password è fallita");
        document.reg.password2.focus();
        document.reg.password2.select();
        return false;
    }
    if (!pass(modulo.password1))
        return false;
    if (!checkmail(modulo.email))
        return false;
    var check4 = /[$-/:-?{-~!"^_`\[\]]/;
    var check5 = /\s/;
    if(check5.test(modulo.username.value) || check4.test(modulo.username.value)){
        alert("Username non valido");
        return false;
    }
    return true;
}


function checkmail(input) {
    var re = /[^@]+@[^@]+\.[^@]/;
    if (!re.test(input.value)) {
        alert("Email non valida");
        return false;
    }
    return true;
}


function controlla(input) {
    content = input.value;
    pos = content.indexOf("@", 0);
    if (pos > -1) {
        alert("Il " + input.placeholder + " non può contenere @");
        var splitted = new Array();
        splitted = content.split("@");
        content = splitted[0];
        input.value = content;
    }
}


function nonumber(event) {
    var tasto;
    tasto = event.key;
    if (("0123456789").indexOf(tasto) > -1) {
        alert("Il " + event.target.placeholder + " non può contenere numeri");
        return false;
    }
    if (("!?=()%&£$+*#-_^.;,:[]{}/|\\'§<>°ç").indexOf(tasto) > -1) {
        alert("Il " + event.target.placeholder + " non può contenere caratteri speciali");
        return false;
    }
    return true;
}


function checkpass(input) {
    var x = 0;
    var password = input.value;
    var bar = document.getElementById("bar");
    var al = document.getElementById("alert");

    var check3 = /[A-Z]/;
    var check = /[0-9]/;
    var check4 = /[$-/:-?{-~!"^_`\[\]]/;
    var check5 = /\s/;
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
    if (password.length == 0) {
        x == 0;
        al.innerHTML = "";
        bar.style.width = 0 + "%";
    } else if (check5.test(password)) {
        al.innerHTML = "La Password non deve contenere spazi";
        bar.style.backgroundColor = "red";
    } else if (check3.test(password) & password.length >= 6) {
        bar.style.backgroundColor = "yellow";
        al.innerHTML = "Good";
        bar.style.width = 50 + "%";
        if (check.test(password) || check4.test(password)) {
            bar.style.backgroundColor = "greenyellow";
            al.innerHTML = "Strong";
            bar.style.width = 75 + "%";
        }
        if (check.test(password) & check4.test(password)) {
            bar.style.backgroundColor = "green";
            al.innerHTML = "Very strong";
            bar.style.width = 100 + "%";
        }
    } else {
        bar.style.backgroundColor = "red";
        al.innerHTML = "Weak";
        bar.style.width = 25 + "%";
    }
    if (check5.test(password)) {
        al.innerHTML = "La Password non deve contenere spazi";
        bar.style.backgroundColor = "red";
    }
}


function pass(password) {
    var al = document.getElementById("alert");
    if (al.innerHTML == "Weak") {
        alert("La " + password.placeholder + " non soddisfa i prerequisiti richiesti");
        return false;
    }
    return true;
}
