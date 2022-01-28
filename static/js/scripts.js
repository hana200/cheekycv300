/*!
    * Start Bootstrap - Resume v6.0.2 (https://startbootstrap.com/theme/resume)
    * Copyright 2013-2020 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-resume/blob/master/LICENSE)
    */
    const menuToggle = document.querySelector('.menu-toggle input');
    const nav = document.querySelector('nav ul');

    menuToggle.addEventListener('click',function(){
      nav.classList.toggle('slide');
    }
    )
    function openNav() {
      document.getElementById("cv-content-sm").style.display = "block";
      document.getElementById("open1").style.display = "none";
      document.getElementById("open1_img").style.display = "none";
      document.getElementById("close1").style.display = "block";
      document.getElementById("close1_img").style.display = "block";
    }

    function closeNav() {
      document.getElementById("cv-content-sm").style.display = "none";
      document.getElementById("close1").style.display = "none";
      document.getElementById("close1_img").style.display = "none";
      document.getElementById("open1").style.display = "block";
      document.getElementById("open1_img").style.display = "block";
    }

    function openMenu() {
      document.getElementById("cheeky-menu").style.display = "block";
      document.getElementById("open2").style.display = "none";
      document.getElementById("open2_img").style.display = "none";
      document.getElementById("close2").style.display = "block";
      document.getElementById("close2_img").style.display = "block";
    }

    function closeMenu() {
      document.getElementById("cheeky-menu").style.display = "none";
      document.getElementById("close2").style.display = "none";
      document.getElementById("close2_img").style.display = "none";
      document.getElementById("open2").style.display = "block";
      document.getElementById("open2_img").style.display = "block";
    }
    function closeMenuCV() {
      document.getElementById("cv-content-sm").style.display = "none";
      document.getElementById("close1").style.display = "none";
      document.getElementById("close1_img").style.display = "none";
      document.getElementById("open1").style.display = "block";
      document.getElementById("open1_img").style.display = "block";
    }

      function show1() {

        document.getElementById("sidebar-open").style.visibility == "hidden";
        document.getElementById('sidebar-close').classList.toggle('active1');
      }
      function stayHiddenDIV() {
        var div = document.getElementById("sidebar-open");
        //Check div is hidden or not. If hidden then display
        if (window.getComputedStyle(div).visibility === "hidden") {
        div.style.visibility = "hidden";
        alert('You refreshed!');
        }
      }
      function checkFirstVisit() {
        if(document.cookie.indexOf('mycookie')==-1) {
          // cookie doesn't exist, create it now
          document.cookie = 'mycookie=1';
        }
        else {
          // not first visit, so alert         
          stayHiddenDIV();
        }
      }
// -a-------------------------------------------------

  function SEE() {
    // get the clock
    var how_div = document.getElementById('how_div');

    // get the current value of the clock's display property
    var displaySetting = how_div.style.display;

    // also get the clock button, so we can change what it says
    var how_btn = document.getElementById('how_btn');

    // now toggle the clock and the button text, depending on current state
    if (displaySetting == 'block') {
      // clock is visible. hide it
      how_div.style.display = 'none';
      // change button text
      how_btn.innerHTML = 'SHOW HOW';
    }
    else {
      // clock is hidden. show it
      how_div.style.display = 'block';
      // change button text
      how_btn.innerHTML = 'HIDE HOW';
    }
  }

// ---------------------------------------------------------
    (function ($) {
    "use strict"; // Start of use strict

    // Smooth scrolling using jQuery easing
    $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function () {
        if (
            location.pathname.replace(/^\//, "") ==
                this.pathname.replace(/^\//, "") &&
            location.hostname == this.hostname
        ) {
            var target = $(this.hash);
            target = target.length
                ? target
                : $("[name=" + this.hash.slice(1) + "]");
            if (target.length) {
                $("html, body").animate(
                    {
                        scrollTop: target.offset().top,
                    },
                    1000,
                    "easeInOutExpo"
                );
                return false;
            }
        }
    });

    // Closes responsive menu when a scroll trigger link is clicked
    $(".js-scroll-trigger").click(function () {
        $(".navbar-collapse").collapse("hide");
    });

    // Activate scrollspy to add active class to navbar items on scroll
    $("body").scrollspy({
        target: "#sideNav",
    });
})(jQuery); // End of use strict

