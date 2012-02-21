(function($) {

$.fancy_ajax = function(url) {
  $.get(url, function(data) {
    $.fancybox({content: data});
  });
};

})($);
