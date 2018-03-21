/* новое добавление в корзину */
function addtostore(id) {
	
	
	console.log('addtostore');
	var data = $('form[name="addtostore'+id+'"]').serialize();
	console.log(data);
	
	$('.addtostorenospinner'+id).hide();
	$('.addtostoreajaxspinner'+id).show();
	
	$.ajax({
		type: "GET",
		url: "/major/cart/add/?"+data,
		dataType: "json",        
		success: function(data){
			console.log(data);
			if(data.res == 1) 
			{

				$('.addtostorenospinner'+id).show();
				$('.addtostoreajaxspinner'+id).hide();
				$('#addtostore').modal();
				//$('#addtostore .modal-body div').html(data);

			}
			else 
			{
				console.log('bad add to store');
				$('#modalerror').modal();	
			}
		}
	});
	
	return false;
}






$(document).ready(function(){


	$('.fancybox').fancybox({
		type: 'image',
		helpers: {
			overlay: {
			locked: false
			}
			}
		});
		
	$(".fancybox-media").fancybox({
		openEffect  : 'none',
		closeEffect : 'none',
		helpers : {
			media : {},
			overlay: {locked: false},
		}
	});


/* 	$(function() {
		$('.chosen-select').chosen({
			search_contains: true,
			
		});
		$('.chosen-select-deselect').chosen({ allow_single_deselect: true });
	}); */


/* 	$('.mydatepicker').datepicker({
		format: 'dd-mm-yyyy',
		 language: 'ru',
		 autoclose: true,
		 showOnFocus: false,
	}); */


	/* подсказки на кнопках сортировки */
	$('[data-toggle="tooltip"]').tooltip(); 


	/* confirm action */
	$('.jqueryconfirm').click(function(){
		if (confirm('Вы уверены?')) {return true;};
		return false;
	}); 

	

		
	//add class form-control to input
	$('input[type=text], input[type=file], input[type=number], input[type=password], textarea, select').addClass('form-control');



	

});  