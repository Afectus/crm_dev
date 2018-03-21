
/* check all checkbox */
function checkall(e, name, callback) {
	res = $(e).prop('checked');
	$(name).prop('checked', res);
	callback();
	return true;
}



function imagebasedel(id)
{
	if (confirm('Вы уверены?')) {
		$.ajax({
			type: 'GET',
			url: '/imagebase/del/'+id,
			//data: data,
			dataType: 'json',
			beforeSend: function(){},
			success: function(data){
				console.log(data);
				if(data.res == 1)
				{
					//console.log('delete goods');
					$('.imagebase'+id).remove();
				}
			},
			error: function(xhr, textStatus, errorThrown){
				console.log(errorThrown);
			}
		});
	};
	return false;
}


function makecall(e, id) {
	var next = false;
	if (confirm('ПОЗВОНИТЬ КЛИЕНТУ?')) 
	{
		$.ajax({
			type: 'GET',
			url: '/makecall/'+id,
			//data: data,
			dataType: 'json',
			beforeSend: function()
				{ 
					$('.callresult').html('Звоним клиенту...');
					$('.callresult').addClass('text-success');
				},
			success: function(data){
				console.log(data);
				if(data.res == 1)
				{
					$('.callresult').html('Удачный звонок');
					$('.callresult').addClass('text-primary');
				}
				else 
				{
					$('.callresult').html('Не удалось позвонить');
					$('.callresult').addClass('text-danger');
				}
			},
			error: function(xhr, textStatus, errorThrown){
				console.log(errorThrown);
				$('.callresult').html('fail');
			}
		});
	}
	return false;
}




function smsqsend(e, id) {
	var url = $(e).attr('href');
	$.ajax({
		type: 'GET',
		//url: '/smsqsend/add/'+id,
		url: url,
		//data: data,
		dataType: 'json',
		beforeSend: function()
			{ 
				//$(e).addClass('hidden');
				$('.smsqsendajaxcontrol'+id).addClass('hidden');
				$('.smsqsendajaxspinner'+id).removeClass('hidden');
			},
		success: function(data){
			console.log(data);
			if(data.res == 1)
			{
				$('.smsqsendajaxspinner'+id).html('Добавлено в очередь');
			}
			else 
			{
				$('.smsqsendajaxspinner'+id).html('fail');
			}
		},
		error: function(xhr, textStatus, errorThrown){
			console.log(errorThrown);
			$('.smsqsendajaxspinner'+id).html('fail');
		}
	});
	return false;
}


function printtask(e, id, idbitrix=false, copies=1, barcode=0) {
	if(idbitrix)
	{
		//новое окно для добавления ценника картинки
		var newWin = window.open('http://babah24.ru/c/print/print.php?ELEMENT_ID='+idbitrix+'&save=1',idbitrix, 'width=850, height=800', 'scrollbars=yes');
	}
	
	var copies = $('input[name="copies'+id+'"]').val();
	
		
	$.ajax({
		type: 'GET',
		url: '/printtask/add/'+id+'/'+copies+'/'+barcode,
		//data: data,
		dataType: 'json',
		beforeSend: function()
			{ 
				//$(e).addClass('hidden');
				$('.printtask'+id).html('Добавляю...');
			},
		success: function(data){
			console.log(data);
			if(data.res == 1)
			{
				$('.printtask'+id).html('Добавлено');
			}
			else if(data.res == 2) {
				$('.printtask'+id).html('Дубль');
			}
			else 
			{
				$('.printtask'+id).html('fail');
			}
			},
		error: function(xhr, textStatus, errorThrown){
			console.log(errorThrown);
			$('.printtask'+id).html('fail');
		}
	});

	return false;
}




function childbooksend(e, id) {
	$.ajax({
		type: 'GET',
		url: '/childbook/add/'+id,
		//data: data,
		dataType: 'json',
		beforeSend: function(){},
		success: function(data){
			console.log(data);
			if(data.res == 1)
			{
				$(e).parent().html('+');
			}
			else 
			{
				$(e).html('fail');
			}
		},
		error: function(xhr, textStatus, errorThrown){
			console.log(errorThrown);
			$(e).html('fail');
		}
	});
	
	
	return false;
}




function getphone(e, id) {
	$.ajax({
		type: 'GET',
		url: '/buyer/getphone/'+id,
		//data: data,
		dataType: 'json',
		beforeSend: function(){},
		success: function(data){
			console.log(data);
			if(data.res == 1)
			{
				console.log(data.phone);
				$('.getphone'+id).html(data.phone);
			}
		},
		error: function(xhr, textStatus, errorThrown){
			console.log(errorThrown);
		}
	});
	return false;
}



/* confirm action */
function jdisabled(e) {
	$(e).addClass('disabled');
	//$(e).html('Подождите'+'...');
	//$(e).html('<img src="/static/img/spinner.gif" />');
	
	var suffix = '.';
	var suffixratio = '';
	var timerId = setInterval(function() {
		console.log(suffixratio);
		suffixratio = suffixratio + suffix;
		$(e).html('Подождите'+suffixratio);
		if(suffixratio.length > 3) {
			suffixratio = '';
		}
	}, 300);
	
	console.log('jdisabled');
	return true;
} 


$(document).ready(function(){

	$("#id_aclu").chosen({
		placeholder_text_multiple: " Права",
		no_results_text: "не найдено",
		search_contains: true,
	});
	
	$("#id_executor").chosen({
		placeholder_text_multiple: " Исполнители",
		no_results_text: "не найдено",
		search_contains: true,
	});
	
	$("#id_addressee_field").chosen({
		placeholder_text_multiple: " Адресаты",
		no_results_text: "не найдено",
		search_contains: true,
	});
	
	$("#id_distributor").chosen({
		placeholder_text_multiple: " Поставщики",
		no_results_text: "не найдено",
		search_contains: true,
	});

	$("#id_user").chosen({
		placeholder_text_multiple: " Пользователи",
		no_results_text: "не найдено",
		search_contains: true,
	});

	$('.fancybox').fancybox({
		type: 'image',
		helpers: {
			overlay: {
			locked: false
			}
			}
	});


	$(function() {
		$('.chosen-select').chosen({
			search_contains: true,
			
		});
		$('.chosen-select-deselect').chosen({ allow_single_deselect: true });
	});


	$('.mydatepicker').datepicker({
		format: 'dd-mm-yyyy',
		 language: 'ru',
		 autoclose: true,
		 showOnFocus: false,
	});

	
	


	/* подсказки на кнопках сортировки */
	$('[data-toggle="tooltip"]').tooltip(); 


	/* confirm action */
	$('.jqueryconfirm, .jconfirm').click(function(){
		if (confirm('Вы уверены?')) {return true;};
		return false;
	}); 

		
	//add class form-control to input
	$('input[type=text], input[type=file], input[type=number], input[type=password], textarea, select').addClass('form-control');


	
/* 	//owl.carousel
	var owlbrand = $('.mCcarousel').owlCarousel({
		loop:true,
		margin:10,
		nav:false,
		lazyLoad:true,
		autoWidth:false,
		responsive:{
			0:{
				items:1
			},
			500:{
				items:2
			},
			1000:{
				items:6
			}
		}
	})
	//owl trigger
	$('#mCcarousel-next').click(function() {
		owlbrand.trigger('prev.owl.carousel');
	})
	$('#mCcarousel-prev').click(function() {
		owlbrand.trigger('next.owl.carousel', [300]);
	}) */
	

});  