
function showvideocount(id)
{
	$.ajax({
		type: 'GET',
		url: '/dev/ajax/showvideocount/'+id,
		//data: data,
		dataType: 'json',
		beforeSend: function(){},
		success: function(data){
			console.log(data);
			if(data.res == 1)
			{
				console.log('show video count + 1');
			}
		},
		error: function(xhr, textStatus, errorThrown){
			console.log(errorThrown);
		}
	});
}






$(document).ready(function(){

	$('*').attr({
		"ondrag":"return false",
		"ondragdrop":"return false",
		"ondragstart":"return false"
	})

});