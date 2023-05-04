

////////////////////////////////////////////////////////////////////////////////////
// Hamburger
const menu_toggle = document.querySelector('.menu-toggle');
const sidebar = document.querySelector('.sidebar');


if(menu_toggle){
  menu_toggle.addEventListener('click', () => {
			menu_toggle.classList.toggle('is-active');
			sidebar.classList.toggle('is-active');
		});
}
////////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////////
////Top button////

const toTop = document.querySelector(".to-top");

window.addEventListener("scroll", () => {
  if (window.pageYOffset > 100) {
    toTop.classList.add("active");
  } else {
    toTop.classList.remove("active");
  }
})
////////////////////////////////////////////////////////////////////////////////////
//menu navigation

//const activePage = window.location.pathname;
//console.log(activePage)

jQuery(function($) {
  var path = window.location.href;
  console.log("window.location.href=", path)
  // because the 'href' property of the DOM element is the absolute path
  //'.menu .menu-item'  'nav a'
  $('.menu .menu-item').each(function() {
    if (this.href === path) {
      $(this).addClass('is-active');
    }
  });
});


/*
$(function(){
    var current = location.pathname;
    console.log(current)
    $('.menu .menu-item').each(function(){
        var $this = $(this);
        // if the current path is like this link, make it active
        if($this.attr('href').indexOf(current) !== -1){
            $this.addClass('is-active');
        }
    })
})
*/

////////////////////////////////////////////////////////////////////////////////////

// chosen items from combobox duplicates to input (geolocations)
$(document).ready(function() {
       $("#select-geo").select2({
            placeholder: "Select geolocations...",
            closeOnSelect: false
       });
            $("#select-geo").on('change', function()
            {
                //var contriesdisplay =$("#select-geo option:selected").text();
                var option_all = $("#select-geo option:selected").map(function () {
                    return $(this).text();
                 }).get().join(',');

                $("#id_geolocations").val(option_all);
            });
     });


//const geo_input111 = document.getElementById('id_geolocations');
//document.getElementById("demo1").innerHTML = geo_input111.value;
//const geo_input2 = document.getElementById('select-geo');
//document.getElementById("demo2").innerHTML = geo_input2.value;

// if combobox is empty we set values by default from input (geolocations)
var selected_combobox = $('#select-geo').val() // value=3 (Austria)

if(jQuery.isEmptyObject(selected_combobox) ){

    const geo_input = document.getElementById('id_geolocations').value; // take names(format text) from input which was added before
    var myArray = geo_input.split(","); // split them by comma

    const geo_combobox = document.getElementById('select-geo'); // get all values from combobox
    for (var i = 0; i < geo_combobox.length; i++)
    {
        for (var j = 0; j < myArray.length; j++)
        {
           if (geo_combobox[i].text == myArray[j])
           {
              var ident = geo_combobox[i].value; // 1 2 3 4...
              $('#select-geo option[value="' + ident +'"]').prop("selected", true);
           }
        }

    }
}



////////////////////////////////////////////////////////////////////////////////////
////Filter////

//// Set the initial state of the checkboxes based on the local storage
//window.onload = function() {
//    document.getElementById("checkbox1").checked = localStorage.getItem("checkbox1") === "true";
//    document.getElementById("checkbox2").checked = localStorage.getItem("checkbox2") === "true";
//    document.getElementById("checkbox3").checked = localStorage.getItem("checkbox3") === "true";
//};
//
//// Uravil
//document.querySelectorAll('input[type="checkbox"]').forEach(function(checkbox) {
//    checkbox.addEventListener('change', function() {
//        localStorage.setItem(checkbox.id, checkbox.checked);
//    });
//});
//
//// Submit the form
//document.getElementById("filter-form").addEventListener("submit", function() {
//    // Do something before submitting the form
//});
//
//
//// When the page loads
//document.addEventListener('DOMContentLoaded', function() {
//  // Loop through each checkbox and set its checked status based on sessionStorage
//  var checkboxes = document.querySelectorAll('input[type="checkbox"]');
//  checkboxes.forEach(function(checkbox) {
//    var checkboxId = checkbox.id;
//    var checkboxState = sessionStorage.getItem(checkboxId);
//    if (checkboxState === 'checked') {
//      checkbox.checked = true;
//    }
//  });
//
//  // Add event listener to the form
//  document.querySelector('form').addEventListener('submit', function(event) {
//    // Loop through each checkbox and store its checked status in sessionStorage
//    checkboxes.forEach(function(checkbox) {
//      var checkboxId = checkbox.id;
//      var checkboxState = checkbox.checked ? 'checked' : 'unchecked';
//      sessionStorage.setItem(checkboxId, checkboxState);
//    });
//  });
//});

////////////////////////////////////////////////////////////////////////////////////

// // Save checkbox state in local storage when form is submitted
//    document.querySelector('.form-filter').addEventListener('submit', function() {
//        document.querySelectorAll('.checked').forEach(function(checkbox) {
//            localStorage.setItem(checkbox.id, checkbox.checked);
//        });
//    });
//
//    // Retrieve checkbox state from local storage and set checkbox state
//    document.querySelectorAll('.checked').forEach(function(checkbox) {
//        checkbox.checked = (localStorage.getItem(checkbox.id) === 'true');
//    });

////////////////////////////////////////////////////////////////////////////////////
//
//// get all checkboxes
//const checkboxes = document.querySelectorAll('input[type=checkbox]');
//console.log("checkboxes=", checkboxes)
//
//// add event listener to form submission event
//const form = document.querySelector('.form-filter');
//form.addEventListener('submit', function() {
//  // save checkbox state to localStorage
//  checkboxes.forEach(checkbox => {
//    localStorage.setItem(checkbox.name, checkbox.checked);
//  });
//});
//
//// set checkbox state from localStorage
//checkboxes.forEach(checkbox => {
//  const checked = localStorage.getItem(checkbox.name) === 'true';
//  checkbox.checked = checked;
//});
//

////////////////////////////////////////////////////////////////////////////////////
//document.querySelector('form').addEventListener('submit', function(event) {
//  var fileInput = document.querySelector('#{{ form.file_field.id_for_label }}');
//  if (fileInput.value === '') {
//    alert('Please select a file');
//    event.preventDefault();
//  }
//});
////////////////////////////////////////////////////////////////////////////////////




