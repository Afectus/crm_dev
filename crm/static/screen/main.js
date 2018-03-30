
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


function videoclose(e)
{
	//$('#player').addClass('hidden');
	//$('#player').show();
	$('#player').html('');
	return false;
}

function videoclick(e)
{
	console.log('video click from onclick');
	videoclose();
	return false;
}


function rvideo(e)
{

	var vid = $(e).attr('data-video-source');

	$('#player').html(
	'<video id="mainvideo" width="1" height="1" onclick="videoclose(this);"><source src="http://127.0.0.1/video/'+vid+'" type="video/mp4"></video>'
	);

	var video = $('#player video');
	
	video[0].load();
	video[0].play();
	
	//$('#player').hide();
	
	video[0].onended = function(e) {
		videoclose();
		console.log('video end');
    };
	
	//for opera
	//var videoElement = document.getElementById('mainvideo');    
	//videoElement.webkitRequestFullScreen();
	
	//for firefox
	//firefox hide fullscreen message
	//about:config
	//full-screen-api.warning.delay;0
	//full-screen-api.warning.timeout;0
	//mozilla disable fullscreen message in user.js
	//user_pref("full-screen-api.warning.delay",0);
	//user_pref("full-screen-api.warning.timeout",0);
	var elem = document.getElementById('mainvideo');
	if (elem.requestFullscreen) {
	elem.requestFullscreen();
	} else if (elem.mozRequestFullScreen) {
	elem.mozRequestFullScreen();
	} else if (elem.webkitRequestFullscreen) {
	elem.webkitRequestFullscreen();
	}
	return false;
}


$(document).ready(function(){

	$('*').attr({
		"ondrag":"return false",
		"ondragdrop":"return false",
		"ondragstart":"return false"
	})

});