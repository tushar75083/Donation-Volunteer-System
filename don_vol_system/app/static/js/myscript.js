// datatable==> gives ready made code for search options ,pagination etc
// mytable is id for tables created...
$(document).ready(function() {
    $('#mytable').DataTable();
} );



// sidebar toggeling
let btn = document.querySelector("#btn-sidebar")
let sidebar = document.querySelector(".sidebar")

btn.onclick = function(){
    console.log("click");
    sidebar.classList.toggle("active");
}