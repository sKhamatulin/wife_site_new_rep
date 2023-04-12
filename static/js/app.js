/*  Theme Name: Dealarc | Responsive Bootstrap 4 Landing Template
    Author: Themesdesign
    Version: 2.0.0
    File Description: Main JS file of the template
*/

(function ($) {
  "use strict";

  // Add scroll class
  $(window).scroll(function () {
    var scroll = $(window).scrollTop();

    if (scroll >= 50) {
      $(".sticky").addClass("nav-sticky");
    } else {
      $(".sticky").removeClass("nav-sticky");
    }

    if ($(this).scrollTop() > 100) {
      $(".back-to-top").fadeIn();
    } else {
      $(".back-to-top").fadeOut();
    }
  });

  // Smooth scroll
  $(".navbar-nav a").on("click", function (event) {
    var $anchor = $(this);
    $("html, body")
      .stop()
      .animate(
        {
          scrollTop: $($anchor.attr("href")).offset().top - 0,
        },
        1500,
        "easeInOutExpo"
      );
    event.preventDefault();
  });

  //Owl Carousel
  $("#owl-demo-cs-testi").owlCarousel({
    autoPlay: 3000,
    navigation: false,
    slideSpeed: 300,
    paginationSpeed: 400,
    singleItem: true,
  });

  //Scrollspy
  $(".navbar-nav").scrollspy({
    offset: 70,
  });

  //Contact Form
  $("#contact-form").submit(function () {
    var action = $(this).attr("action");

    $("#message").slideUp(750, function () {
      $("#message").hide();

      $("#submit")
        .before('<img src="images/ajax-loader.gif" class="contact-loader" />')
        .attr("disabled", "disabled");

      $.post(
        action,
        {
          name: $("#name").val(),
          email: $("#email").val(),
          comments: $("#comments").val(),
        },
        function (data) {
          document.getElementById("message").innerHTML = data;
          $("#message").slideDown("slow");
          $("#cform img.contact-loader").fadeOut("slow", function () {
            $(this).remove();
          });
          $("#submit").removeAttr("disabled");
          if (data.match("success") != null) $("#cform").slideUp("slow");
        }
      );
    });

    return false;
  });

  // Back to top
  $(".back-to-top").click(function () {
    $("html, body").animate({ scrollTop: 0 }, 1000);
    return false;
  });
})(jQuery);
