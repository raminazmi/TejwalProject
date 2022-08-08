$(function(){
    var navbar = $('.header-inner');
    $(window).scroll(function(){
      if($(window).scrollTop() <=300){
        navbar.removeClass('navbar-scroll');
      }else{
        navbar.addClass('navbar-scroll');
      }
    });
  });

