
var balls = [];

balls.push({'id':1, 'x':50, 'y':50, 'radius':15, 'color': 'c1', 'colortext': ''});
balls.push({'id':2, 'x':100, 'y':100, 'radius':15, 'color': 'c2', 'colortext': ''});
balls.push({'id':3, 'x':200, 'y':200, 'radius':15, 'color': 'c3', 'colortext': ''});
balls.push({'id':4, 'x':241, 'y':220, 'radius':15, 'color': 'c2', 'colortext': ''});

var colors = {'c1':'red','c2':'yellow','c3':'blue',}

var shownumber = false;

var bw=0;
var bh=0;

var cw = 0;
var ch = 0;

offsetX=0;
offsetY=0;

balldrag=false;

var backsrc = 'http://st2.depositphotos.com/4754361/11200/v/950/depositphotos_112003916-stock-illustration-cartoon-flat-vector-interior-office.jpg';

var startradius = 15;

function randradius(radius=startradius) {
	radius = radius + Math.floor((Math.random() * 4) + 1);
	return radius;
}



function setbackground(e) {
	backsrc = $(e).find('input[name="background"]').val();
	console.log(backsrc);
	mydraw();
}
function listball() {
	$('.listballs').html('');
	for (var i = 0; i < balls.length; i++) 
	{
		var b = balls[i];
		//console.log(b);
		$('.listballs').append('<div class="form-group"><a href="#" id="'+b.id+'" class="btn btn-primary" onclick="setball('+b.id+'); return false;">'+b.id+'</a></div>')
	}
}
function addball() {	
	var l = balls.length+2;
	var pos = 20+(l*5);
	balls.push({'id':l, 'x':pos, 'y':pos, 'radius':randradius(), 'color': 'c1', 'colortext': 'red'});
	$('.listballs').append('<div class="form-group"><a href="#" id="'+l+'" class="btn btn-primary" onclick="setball('+l+'); return false;">'+l+'</a></div>')
	$('form#listball').find('input[name="ball"]').val(l);
	mydraw();
}
function delball(e) {	
	var ballid = $('form#listball').find('input[name="ball"]').val();
	for(var i = 0; i < balls.length; i++) 
	{
		var b = balls[i];
		if(b.id == ballid) 
		{
			console.log('delball '+ballid);
			//delete balls[i];
			balls.splice(i, 1);
			console.log('remove ball '+ballid);
			$('a[id="'+b.id+'"]').parent().remove();
		}
	}
	mydraw();
}
function setball(id) {
	$('form#listball').find('input[name="ball"]').val(id);
}
function changecolor(id) {
	var idball = $('form#listball').find('input[name="ball"]').val();
	for(var i = 0; i < balls.length; i++) 
	{
		var b = balls[i];
		if(b.id == idball) 
		{
			var c = colors['c'+id];
			b.color = 'c'+id;
			mydraw();

		}
	}
}

function setradius(action) {
	if(action == true && startradius < 30)
	{
		startradius = startradius + 1;
		console.log('+', startradius);
	}
	else if(action == false && startradius > 1)
	{
		startradius = startradius - 1;
		console.log('-', startradius);
	}
	else 
	{
		return false;
	}
	mydraw();
}

function fshownumber(e) {
	if(shownumber == false)
	{
		shownumber = true;
	}
	else 
	{
		shownumber = false;
	}
	mydraw();
}

function init(w,h) {
	canvas = document.getElementById("canvas"),
	context = canvas.getContext('2d');
	
	cw = canvas.width;
	ch = canvas.height;	
	
	context.beginPath();
	context.fillRect(0, 0, cw, ch); //запонляем канвас черным квадратом
	context.closePath();
	
	canvas.onmousedown = mdown;
	canvas.onmouseup = mup;
	canvas.onmousemove = mmove;
	
	var canvasOffset=$("#canvas").offset();
	offsetX=canvasOffset.left;
	offsetY=canvasOffset.top;

}

function drawball(){
	for (var i = 0; i < balls.length; i++) 
	{
		var b = balls[i];

		var id = b['id'];
		var x = b['x'];
		var y = b['y'];
		var radius = randradius(); //случайный радиус
		b.radius = startradius;
		var color = b['color'];

		/* градиент */
		var grd=context.createRadialGradient(x+5, y-5, radius, x+5, y-5, 0);
		grd.addColorStop(0,colors[color]);
		grd.addColorStop(1,"white");
		/* конец градиент */
		
		/* шар */
		context.beginPath();
		//context.arc(canvas.width / x, canvas.height / y, radius, 0, 2 * Math.PI, false);
		context.arc(x, y, radius, 0, 2 * Math.PI, false);
		context.fillStyle = grd;
		context.fill();
		//border
		context.lineWidth = 0.3;
		context.strokeStyle = '#484848';
		context.stroke();
		
		if(shownumber == true) //показывать цифры или нет
		{
			context.beginPath();
			context.fillStyle = "black";
			//context.strokeStyle = "#F00";
			context.font = "italic 10pt Arial";
			context.fillText(id, x, y);
			//context.font = 'bold 30px sans-serif';
			//context.strokeText("Stroke text", 20, 100);
		}
	}

}

function mydraw() {
	console.log('mydraw');

	var background = new Image;
	background.src = backsrc;

	background.onload = function() 
	{
		if (background != null && 0 != background.width && background.complete) 
		{
			bw=background.width;
			bh=background.height;
			//console.log(background.width, background.height);
			context.drawImage(background, 0, 0, cw, ch);
			drawball();
		}
	}
		
}

function mup(){
	console.log('mousaup');
	balldrag=false;
	//canvas.onmousemove = null;
}

function mmove(e) {
	if(balldrag) {
		console.log('mousdown', e.pageX, e.pageY);
		var idball = $('form#listball').find('input[name="ball"]').val();
		for(var i = 0; i < balls.length; i++) 
		{
			var b = balls[i];
			if(b.id == idball) 
			{
				console.log(b.id);
				console.log('=', canvas.offsetLeft, canvas.offsetTop);

				console.log('=', offsetX, offsetY);
				
				b.x = e.pageX-offsetX;
				b.y = e.pageY-offsetY;
				
				mydraw();
				//drawball();
			}
		}
	}
}

function mdown(e){
	balldrag=true;
/* 	console.log('mousdown', e.pageX, e.pageY);
	var idball = $('form#listball').find('input[name="ball"]').val();
	for(var i = 0; i < balls.length; i++) 
	{
		var b = balls[i];
		if(b.id == idball) 
		{
			console.log(b.id);
			console.log('=', canvas.offsetLeft, canvas.offsetTop);

			console.log('=', offsetX, offsetY);
			
			b.x = e.pageX-offsetX;
			b.y = e.pageY-offsetY;
			
			mydraw();
			//drawball();
		}
	} */
}

function balltotext() {
	var res = '';
	for (var i = 0; i < balls.length; i++) 
	{
		var b = balls[i];
		var tmp = "balls.push({'id':"+b.id+", 'x':"+b.x+", 'y':"+b.y+", 'radius':"+b.radius+", 'color': '"+b.color+"'});";
		res = res + tmp + '\n';
	}
	
	res = res + '\n' + 'var colors = {';
	
	for(c in colors)
	{
		console.log(colors[c]);
		res = res + "'"+c+"':'"+colors[c]+"',"
		
	}

	res = res + '}';

	return res;
}

function genconf() {
	var name = Math.random().toString(36).slice(-8); //генерируем имя

	colortotext = JSON.stringify(colors);

	for (var i = 0; i < balls.length; i++) 
	{
		var b = balls[i];
		/* create conf */
		$.ajax({
			type: 'POST',
			url: '/mod/ballgenconf/',
			data: {name: name, bid: b.id, x: b.x, y: b.y, radius: b.radius, color: b.color, colortext: colortotext, background: backsrc},
			dataType: 'json',
			beforeSend: function(){},
			success: function(data){
				console.log(data);
				if(data.res == 1){}
			},
			error: function(xhr, textStatus, errorThrown){
				console.log(errorThrown);
			}
		});
	}
	$('.savelist').prepend('<a href="#" class="btn btn-default" onclick="getconf(\''+name+'\'); return false;">'+name+'</a>')
}


function getconf(name) {
	console.log('getconf');
  	$.getJSON( "/mod/ballgetconf/"+name, function(data) {
		balls = [];
		//console.log(data);
		if(data.res == 1) 
		{
			//set background
			backsrc = data.background;
			$('body').find('input[name="background"]').val(backsrc);
		
 			$.each(data.item, function(key, val) {
				//console.log(key, val);
				balls.push(val);
				startradius = val.radius;
			});
   			$.each(data.color, function(key, val) {
				//console.log(key, val);
				colors[key] = val; //{'c1':'#0086ff','c2':'#f11fdd','c3':'#19ecac',}
				
				$('#colorpicker-'+key).spectrum("set", val);
			});
			mydraw();
			listball();
		}
	});

}



$(document).ready(function(){
	
	$("a#bfile").click(function(){
		console.log('get file');
		var res = balltotext();
		this.href = "data:text/plain;charset=UTF-8,"  + encodeURIComponent(res);
	});
		
		
	$("#colorpicker-c1").spectrum({
		color: colors['c1'],
		change: function(color) {
			var c = color.toHexString(); // #ff0000
			//console.log(c);
			colors['c1'] = c;
			drawball();
		}
	});
	$("#colorpicker-c2").spectrum({
		color: colors['c2'],
		change: function(color) {
			var c = color.toHexString(); // #ff0000
			//console.log(c);
			colors['c2'] = c;
			drawball();
		}
	});
	$("#colorpicker-c3").spectrum({
		color: colors['c3'],
		change: function(color) {
			var c = color.toHexString(); // #ff0000
			//console.log(c);
			colors['c3'] = c;
			drawball();
		}
	});
		
	listball();
	init();
	mydraw();
	
	/* рисуем дугу */
/* 	context.beginPath();
	context.arc(canvas.width / 2, canvas.height / 2, 100, 0, (Math.PI/180)*180, true);
	context.fillStyle = "red";
	context.fill(); // *14
	context.closePath();
	
	var sw=canvas.width / 4;
	var sh=canvas.height / 2;


	for (var i = 0; i < balls.length; i++) 
	{
		var b = balls[i];

		console.log(sw, sh);
		
		context.beginPath();
		context.moveTo(sw, sh);
		
		sw=sw+10;
		sh=sh-30-b.radius;
		
		context.lineTo(sw, sh);

		context.fillStyle = "blue";
		context.fill(); // *14
		context.lineWidth = 5;
		context.strokeStyle = b.color;
		context.stroke(); // *22
		context.closePath();
		

	} */



   

});




/*


var canvas;
var ctx;


var arka = new Image;


var arkax = 70;
var arkay = 70;

var arkaw = 400;
var arkah = 300;

var arkadrag = false;
//var WIDTH = 400;
//var HEIGHT = 300;
//var dragok = false;


function init() {
	canvas = document.getElementById("example"),
	ctx = canvas.getContext('2d');
	ctx.fillRect(0, 0, example.width, example.height);
	return setInterval(mydraw, 100);
}




function drawarka() {
	arka.src = 'http://gallery.yopriceville.com/var/resizes/Free-Clipart-Pictures/Balloons-PNG/Transparent_Balloon_Arch_with_Decoration_Clipart.png?m=1399672800';
	
	arka.onload = function() 
	{
		if (arka != null && 0 != arka.width && arka.complete) 
		{
			//console.log('arka good');
			ctx.drawImage(arka, arkax, arkay, arkaw, arkah);
			ctx.strokeStyle="#FF0000";
			ctx.strokeRect(arkax, arkay, arkaw, arkah);
		}
		else
		{
			console.log('arka bad');
		}
	}
	return false;
}



function mydraw() {

	var backsrc = setbackground('form');
	//console.log(backsrc);
	
	var background = new Image;
	background.src = backsrc;

	background.onload = function() 
	{
		if (background != null && 0 != background.width && background.complete) 
		{
			//console.log(background.width, background.height);
			ctx.drawImage(background, 0, 0, 600, 400);
			drawarka();
		}
	}
		
}

function mup(){
	console.log('mousaup');
	arkadrag=false;
	//canvas.onmousemove = null;
}


function mmove(e) {
	if (arkadrag)
	{
		//ctx.clearRect(0, 0, example.width, example.height)
		
		a = e.pageX - (e.pageX - 70);
		//a = e.pageX;
		//aa = e.pageX - a;
		
		b = e.pageY - (e.pageY - 70);
		//b = e.pageY;
		//bb = e.pageY - b;
		console.log('X', e.pageX, a);
		console.log('Y', e.pageY, b);
		
		arkax = a - canvas.offsetLeft;
		arkay = b - canvas.offsetTop;
	}
}

function mdown(e){
	console.log('mousdown', e.pageX, e.pageY);
	if (e.pageX >= arkax+canvas.offsetLeft && e.pageX <= (arkax+canvas.offsetLeft)+arkaw && e.pageY >= arkay+canvas.offsetTop && e.pageY <= (arkay+canvas.offsetTop)+arkah)
	{
		console.log(e.pageY,' >= ',arkay+canvas.offsetTop,e.pageY ,'<=', (arkay+canvas.offsetTop)+arkah);
		arkadrag=true;
		if (arkadrag)
		{
			canvas.onmousemove = mmove;
		}
	}
}

$(document).ready(function(){

	init();
	canvas.onmousedown = mdown;
	canvas.onmouseup = mup;
	
	$('#fback').submit(function(event) {
		mydraw(ctx);
		event.preventDefault();
	});
	
	
});

*/

