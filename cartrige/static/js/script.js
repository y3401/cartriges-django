var delc = document.querySelector('ol');
//var delp = document.querySelector('ol');
var divInfo = document.querySelector('inform');


function deleteCartrige(e) {
    console.log(e);
    if (e.target.id==('delc')) {
    if (window.confirm('Удалить этот картридж? Вы уверены?')==true) {
        var pk=e.target.getAttribute('value'); 
        var pat="../cartriges/" + pk + "/delete/";
        window.top.location.href=pat;
    }
  }
}

function delCart(pk) {
    if (window.confirm('Удалить этот картридж? \nВы уверены?')==true) { 
        var pat="../cartriges/" + pk + "/delete/";
        window.location.href=pat;
    }
}

function deletePrinter(e) {
    console.log(e);
    if (e.target.id==('delp')) {
    if (window.confirm('Удалить этот принтер? Вы уверены?')==true) {
        var pk=e.target.getAttribute('value'); 
        var pat="../printers/" + pk + "/delete/";
        window.top.location.href=pat;
    }
  }
}


delc.onclick=deleteCartrige;









