// Disable form submissions if there are invalid fields
	(function() {
	  'use strict';
	  window.addEventListener('load', function() {
		// Get the forms we want to add validation styles to
		var forms = document.getElementsByClassName('needs-validation');
		// Loop over them and prevent submission
		var validation = Array.prototype.filter.call(forms, function(form) {
		  form.addEventListener('submit', function(event) {
			if (form.checkValidity() === false) {
			  event.preventDefault();
			  event.stopPropagation();
			}
			form.classList.add('was-validated');
		  }, false);
		});
	  }, false);
	})();
	
	
	function preventNonNumericalInput(e) {
	  e = e || window.event;
	  var charCode = (typeof e.which == "undefined") ? e.keyCode : e.which;
	  var charStr = String.fromCharCode(charCode);

	  if (!charStr.match(/^[0-9]+$/))
		e.preventDefault();
	};	

	function upfct() {
		var xmlhttp = new XMLHttpRequest();
		xmlhttp.onreadystatechange = function() {
			if (this.readyState == 4 && this.status == 200) {
				document.getElementById("upfctstatus").innerHTML = this.responseText;
			}
		};
		xmlhttp.open("POST", "../server/upfct.php", true);
		xmlhttp.send(new FormData(document.getElementById("upfctmsg")));
		return false;
	};