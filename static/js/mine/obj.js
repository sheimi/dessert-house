/*
 * dependency: core.js
 */
(function(window) {

/*
 * para need:
 * url
 * data
 * method
 */
function send_json(para) {
  return $.ajax({
    url: para.url,
    contentType: 'application/json',
    data: JSON.stringify(para.data),
    dataType: 'json',
    type: para.method
  });
}

function show_msg(msg) {
  return function(json) {
    if (json.success)
      success.top_message(msg);
    else
      error.top_message(json.message);
  };
}

function rest_creator(obj) {
  return function() {
    var url = '/rest/'+ obj;
    this.get = function(obj_id) {
      var t = send_json({
        url: url + '/'  + obj_id,
        method: 'GET'
      }).done(show_msg("get success"));
      return t;
    };
    this.update = function(obj_id, data) {
      var t = send_json({
        url: url + '/'  + obj_id,
        method: 'PUT',
        data: data
      }).done(show_msg("update success"));
      return t;
    };
    this.delete = function(obj_id) {
      var t = send_json({
        url: url + '/'  + obj_id,
        method: 'DELETE'
      }).done(show_msg("delete success"));
      return t;
    };
    this.create = function(data) {
      var t = send_json({
        url: url,
        method: 'POST',
        data: data
      }).done(show_msg("create success"));
      return t;
    };
  };
}

var user = new (rest_creator('User'))();
var role = new (rest_creator('Role'))();
var usertype = new (rest_creator('UserType'))();
var perm = new (rest_creator('Permission'))();
var product = new (rest_creator('Product'))();
var dessert_type = new (rest_creator('DessertType'))(); 
var dessert = new (rest_creator('Dessert'))();
var order = new (rest_creator('Order'))();
var order_item = new (rest_creator('OrderItem'))();
var reservation = new (rest_creator('Reservation'))();
var reservation_item = new (rest_creator('ReservationItem'))();


//add user
(function(user) {

var url = '/rest/User/';

user.get_by_name = function(username) {
};

user.recharge = function(user_id, year) {
  var t = send_json({
    url: url + user_id,
    method: 'PUT',
    data: {recharge : year}
  }).done(show_msg("recharge success"));
  return t;
};

user.deactivate = function(user_id) {
  var t = send_json({
    url: url + user_id + '/deactivate',
    method: 'DELETE'
  }).done(show_msg("deactivate success"));
  return t;
};

user.activate = function(user_id) {
  var t = send_json({
    url: url + user_id + '/activate',
    method: 'POST'
  }).done(show_msg("activate success"));
  return t;
};

})(user);

window.usertype = usertype;
window.user = user;
window.role = role;
window.perm = perm;
window.product = product;
window.dessert_type = dessert_type;
window.dessert = dessert;
window.rest_creator = rest_creator;
window.order = order;
window.order_item = order_item
window.reservation = reservation;
window.reservation_item = reservation_item;
window.send_json = send_json;

})(window);
