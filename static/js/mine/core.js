/**
 * Foundation JavaScript for my english website.
 * utilities for the website
 * author: sheimi
 * version: 1
 */

// Array Remove - By John Resig (MIT Licensed)
Array.prototype.remove = function(from, to) {
  var rest = this.slice((to || from) + 1 || this.length);
  this.length = from < 0 ? this.length + from : from;
  return this.push.apply(this, rest);
};

//author kavinyao
(function($){
  $.fn.center = function() {
    return this.each(function(){
      var $this = $(this);
      $this.css("position", "absolute");
      $this.css("top", ($(window).height() - $this.height())/2 + $(window).scrollTop() + "px");
      $this.css("left", ($(window).width() - $this.width())/2 + $(window).scrollLeft() + "px");
    });
  };
  $.fn.topcenter = function() {
    return this.each(function(){
      var $this = $(this);
      $this.css("position", "fixed");
      $this.css("top", "40px");
      $this.css("left", ($(window).width() - $this.width())/2 + $(window).scrollLeft() + "px");
    });
  };
  $.fn.set_highlight = function() {
    $(this).hover(function() {
      $(this).css({background: 'rgba( 255, 255, 190, 1)'});
    }, function() {
      $(this).css({background: 'transparent'});
    });
  };
})(jQuery);


(function(window){
  me = {};
  me.sheimi = {
    notif: function(message, type, delay) {
      delay = typeof(delay) != 'undefined' ? delay : 4000;

      var notif = $('<div class="notif '+ type + '">' + message + '</div>');
      notif.hide();
      notif.appendTo($('body')).topcenter();
      notif.slideDown('slow').delay(delay).slideUp('slow');
    }
  };
  window.error = {
    top_message: function(message) {
      me.sheimi.notif(message, 'top-error');
    }
  };
  window.success= {
    top_message: function(message) {
      me.sheimi.notif(message, 'top-success');
    }
  };
})(window);
