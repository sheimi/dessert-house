(function($) {

$.fancy_ajax = function(url) {
  $.get(url, function(data) {
    $.fancybox({content: data});
  });
};

$.fancy_ajax_g = function(info) {
  $.get(info.url, function(data) {
    $.fancybox({content: data, maxWidth: info.width, maxHeight: info.height});
  });
};

})($);
