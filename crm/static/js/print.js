function makeid()
{
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    for( var i=0; i < 5; i++ )
        text += possible.charAt(Math.floor(Math.random() * possible.length));

    return text;
}

var socketa = false; //если отвалился nodejs что бы остальной javascript не отваливался

var clientid = makeid();

function clearbarcodeinput() 
{
	$('#id_barcode').val('');
	$('#id_barcode').focus(); 
	return false;
}

function printqrcode(e, id) 
{
	var print = $(e).attr('data-print');
	if(print == 'false')
	{
		console.log('set true');
		$(e).attr('data-print', 'true');

		setTimeout(function(){
			console.log('set false')
			$(e).attr('data-print', 'false');
		}, 10000);
		return false;
	}
	if(print == 'true')
	{
		console.log('from client send')
		$(e).attr('data-print', 'false');
		socketa.emit('print', { 'name': 'qrcode', 'id': id });
	}
	return false;
}


$(document).ready(function(){
	//clearbarcodeinput();
	
	try {socketa = io.connect('http://crm.babah24.ru:3000');}
	catch(e) {console.log(e);}
		
	if(socketa) //если сокет подключен то выполняем код
		{
			socketa.on('connect', function(){
				console.log("connect to server socket.io");
				socketa.emit('myauth', { 'name': clientid });
			});
			socketa.on('disconnect', function (){
				console.log("disconnect from server socket.io");
			});
			//получаем сообщение от сервера
			socketa.on('message', function(data){
				//console.log(data);
			});

			socketa.on('myauth', function (data){
				console.log(data);
			});
			
			socketa.on('res', function (data){
				console.log(data);
				if(data['type'] == 'link')
				{
					$('.nodejsdebugger').html('<a href="http://192.168.0.250/pricezip/'+data['data']+'.zip">Скачать архив ценников</a>')
					$('.downloadprice').removeAttr('disabled');
				}
				if(data['type'] == 'info')
				{
					$('.nodejsdebugger').html(data['data'])
				}
			});
			
			
		};
});