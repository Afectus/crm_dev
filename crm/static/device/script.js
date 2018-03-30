$(document).ready(function() {
	initWebSocket();
});



var websocket;

function initWebSocket() {
	websocket = new WebSocket("ws://localhost:8080/");
	return false;
}

function openVideo(video){
	websocket.send("master_video;0;"+video+";local");
}

var id = 0;
var p = 0;
var openSet, closeSet, changeSort;

$( document ).ready(function() {
	var w = $('body').css('width').replace('px','')*1 - 560 - 25;
	var i = Math.floor(w/2);
	$('.items .item').css('width', i+'px');

	$('#ajax .bg').on('click', function(){
		closeSet();
	});
	openSet = function(id){
		$('#ajax').show();
		$('#panel').show();
		$('#panel').load('/ajax.php?id='+id);
	}
	closeSet = function(){
		$('#ajax').hide();
		$('#panel').hide();
		$('#sort').hide();
		$('#panel').html('');
	}

	$('.sort').on('click', function(){
		$('#ajax').show();
		$('#sort').show();
	});
	changeSort = function(by){
		window.location = '/index.php?page=cat&id='+id+'&p=1&order='+by;
	}

	$('*').attr({
       "ondrag":"return false",
       "ondragdrop":"return false",
       "ondragstart":"return false"
    })
});