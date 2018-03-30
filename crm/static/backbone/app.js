

/* get detail */
var Discounts = Backbone.Model.extend({
    urlRoot: 'http://box.babah24.ru/api/goods/detail'
});

a = new Discounts({id: 115}).fetch()


/* add object */
/* var Discounts = Backbone.Model.extend({
    urlRoot: 'http://box.babah24.ru/api/goods/create',
});

var newDiscounts = new Discounts({ status: true, name: '1', });

newDiscounts.save(null, {
    success: function (model, response) {
        console.log("success");
    },
    error: function (model, response) {
		console.log(response);
        console.log(response.responseJSON.detail);
    }
}); */




/* form */

var User = Backbone.Model.extend({
	//template: _.template($('#formTemplate').html()),


});

var user = new User();

var form = new Backbone.Form({
    model: user,
	
	schema: {
        name: { type: 'Text', maxlength: 30, title: 'Tooltip help', validators: ['required',] },
    },
	
	submitButton: '123',
}).render();


$(document).ready(function() {
	$('.myform').append(form.el);
});







