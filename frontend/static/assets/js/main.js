/*-----------------------------------------------------------------------------------


    Note: This is Main Js file
-----------------------------------------------------------------------------------
    Js INDEX
    ===================
    ## Main Menu
    ## Document Ready
    ## Prealoder
    ## Sticky
    ## Back to top
    ## Counter
    ## Magnific-popup js
    ## Nice select
    ## Slick Slider
    ## Isotope JS
    ## wow JS
    ## Item Active
-----------------------------------------------------------------------------------*/

(function($) {
    'use strict';

    //===== Main Menu
    function mainMenu() {
        // Variables
        var var_window = $(window),
            navContainer = $('.header-navigation'),
            navbarToggler = $('.navbar-toggler'),
            navMenu = $('.nav-menu'),
            navMenuLi = $('.nav-menu ul li ul li'),
            closeIcon = $('.navbar-close');
        // navbar toggler
        navbarToggler.on('click', function() {
            navbarToggler.toggleClass('active');
            navMenu.toggleClass('menu-on');
        });
        // close icon
        closeIcon.on('click', function() {
            navMenu.removeClass('menu-on');
            navbarToggler.removeClass('active');
        });
        // adds toggle button to li items that have children
        navMenu.find('li a').each(function() {
            if ($(this).next().length > 0) {
                $(this).parent('li').append('<span class="dd-trigger"><i class="far fa-angle-down"></i></span>');
            }
        });
        // expands the dropdown menu on each click
        navMenu.find('li .dd-trigger').on('click', function(e) {
            e.preventDefault();
            $(this).parent('li').children('ul').stop(true, true).slideToggle(350);
            $(this).parent('li').toggleClass('active');
        });
        // check browser width in real-time
        function breakpointCheck() {
            var windoWidth = window.innerWidth;
            if (windoWidth <= 1199) {
                navContainer.addClass('breakpoint-on');
            } else {
                navContainer.removeClass('breakpoint-on');
            }
        }
        breakpointCheck();
        var_window.on('resize', function() {
            breakpointCheck();
        });
    };
    // Panel Widget
    var panelIcon = $('.bar-item'),
    panelClose = $('.panel-close,.panel-overlay'),
    panelWrap = $('.offcanvas-panel');
    panelIcon.on('click', function (e) {
        panelWrap.toggleClass('panel-on');
        e.preventDefault();
    });
    panelClose.on('click', function (e) {
        panelWrap.removeClass('panel-on');
        e.preventDefault();
    });
    // Nav Overlay On
    $(".navbar-toggler, .navbar-close,.nav-overlay").on('click', function (e) {
        $(".nav-overlay").toggleClass("active");
    });
    $(".nav-overlay").on('click', function (e) {
        $(".navbar-toggler").removeClass("active");
        $(".nav-menu").removeClass("menu-on");
    });

    // Document Ready
    $(document).ready(function() {
        mainMenu();
        setTimeout(() => {
            $('.preloader').fadeOut(1000)
        }, 5200);
    });

    $('.box-price').each(function() {
        var $this = $(this);
        $('input[type="radio"]', this).on('change', function() {
            var data = $(this).attr('data-price')
            $('.price span', $this).text(data)
        })
    })

    $('.courses-list-content .content-more').each(function() {
        var text = $('.text', this)
        $('.show-more-content', this).on('click', function() {
            //toggle elements with class .ty-compact-list that their index is bigger than 2
            text.toggleClass('active')
            //change text of show more element just for demonstration purposes to this demo
            $(this).text() === 'Show More' ? $(this).text('Show Less') : $(this).text('Show More');
        });
    })

    $(document).ready(function() {
        $('.toggle-accordion').on('click', function () {
            $('#list-1 .collapse').collapse('toggle');
            $(this).text() === 'Expand all sections' ? $(this).text('Collapse all sections') : $(this).text('Expand all sections');
        });
        
           
      });

    $('.vid-list-container a').on('click', function() {
        $('.vid-list-container a').removeClass('active')
        $(this).addClass('active')
    })
    if ($(".swiper-pricing").length) {
		$(".swiper-pricing").each(function() {
			var $ttPrice = $(this);
    
      // Init Swiper
			// =============
			var $ttPriceSwiper = new Swiper ($ttPrice[0], {
				// Parameters
				// effect: "cards",
                // centeredSlidesBounds: true,
                // centeredSlides: true,
                // centerInsufficientSlides: true,
                // slideToClickedSlide: true,
                spaceBetween: 0,
                grabCursor: true,
                slidesPerView: 1,
                coverflowEffect: {
                    rotate: 15,
                    slideShadows: false,
                }, 
        
				speed: 600,
				autoplay: {
                    delay: 7000,
                    disableOnInteraction: true
                },
                pagination: {
                    el: $ttPrice.find(".swiper-pagination")[0],
                    clickable: true,
                },
                breakpoints: {
                    992: {
                        slidesPerView: 3,
                    },
                    768: {
                        slidesPerView: 2,
                    },
                    576: {
                        slidesPerView: 1,
                    }
                },
				// Navigation arrows
				// navigation: {
				// 	nextEl: $ttCertificate.find(".swiper-button-next")[0],
				// 	prevEl: $ttCertificate.find(".swiper-button-prev")[0],
				// },

				
			});
    })
  }

    if ($(".swiper-certi").length) {
		$(".swiper-certi").each(function() {
			var $ttCertificate = $(this);
    
      // Init Swiper
			// =============
			var $ttCertificateSwiper = new Swiper ($ttCertificate[0], {
				// Parameters
				// effect: "cards",
                centeredSlidesBounds: true,
                centeredSlides: true,
                centerInsufficientSlides: true,
                slideToClickedSlide: true,
                spaceBetween: 30,
                grabCursor: true,
                slidesPerView: 3,
                effect: 'coverflow',
                coverflowEffect: {
                    rotate: 15,
                    slideShadows: false,
                }, 
        
				speed: 600,
				autoplay: {
                    delay: 7000,
                    disableOnInteraction: true
                },
                pagination: {
                    el: $ttCertificate.find(".swiper-pagination")[0],
                    clickable: true,
                },
				// Navigation arrows
				// navigation: {
				// 	nextEl: $ttCertificate.find(".swiper-button-next")[0],
				// 	prevEl: $ttCertificate.find(".swiper-button-prev")[0],
				// },

				// // Pagination
				// pagination: {
				// 	el: $ttPortfolioSlider.find(".swiper-pagination")[0],
				// 	clickable: true,
				// },
			});
    })
  }



    //===== Prealoder
    // $(document).on('ready', function(event) {
    //     $('.preloader').delay(5000).fadeOut('500');
    // })
    
    //===== Sticky
    $(window).on('scroll', function(event) {
        var scroll = $(window).scrollTop();
        if (scroll < 100) {
            $(".header-navigation").removeClass("sticky");
        } else {
            $(".header-navigation").addClass("sticky");
        }
    });

    //===== Back to top
    $(window).on('scroll', function(event) {
        if ($(this).scrollTop() > 600) {
            $('.back-to-top').fadeIn(200)
        } else {
            $('.back-to-top').fadeOut(200)
        }
    });
    $('.back-to-top').on('click', function(event) {
        event.preventDefault();
        $('html, body').animate({
            scrollTop: 0,
        }, 1500);
    });

    var hHeader = $('.theme-header').height() + 30;

    $(".sticky_column").stick_in_parent({
        offset_top: hHeader,
        inner_scrolling: false
    });

    //===== Counter js
    $('.count').counterUp({
        delay: 100,
        time: 4000
    });

    //===== Magnific-popup js
    $('.video-popup').magnificPopup({
        type: 'iframe',
        removalDelay: 300,
        mainClass: 'mfp-fade'
    });

    $(".img-popup").magnificPopup({
        type: "image",
         gallery: { 
          enabled: true 
        }
    });
    //===== Nice select js
    $('select').niceSelect();

    // Scrolling button
	// =================
	if ($(".tt-scrolling-btn").length) {
		$(".tt-scrolling-btn").each(function() {
			var $this = $(this);
			var $scrBtnSvg = $this.find(".scr-btn-spinner");
			gsap.from($scrBtnSvg, {
				rotate: 240,
				ease: "none",
				scrollTrigger: {
					trigger: $scrBtnSvg,
					start: "-40% bottom",
					end: "120% top",
					scrub: true,
					markers: false,
				}, 
			});
		});
	}

    
    //===== Slick slider js
    
    $('.portfolio-slider-one').slick({
		dots: true,
		arrows: false,
        infinite: true,
		speed: 1500,
        autoplay: true,
		slidesToShow: 3,
        slidesToScroll: 1,
        prevArrow: '<div class="prev"><i class="far fa-angle-left"></i></div>',
		nextArrow: '<div class="next"><i class="far fa-angle-right"></i></div>',
        responsive: [
            {
                breakpoint: 1200,
                settings: {
                    arrows: false,
                    slidesToShow: 2
                }
            },
            {
                breakpoint: 767,
                settings: {
                    arrows: false,
                    slidesToShow: 1
                }
            }
        ]
    });
    $('.testimonial-slider-one').slick({
		dots: true,
		arrows: false,
        infinite: true,
		speed: 1500,
        autoplay: true,
        vertical: true,
        adaptiveHeight: false,
		slidesToShow: 1,
        slidesToScroll: 1,
        prevArrow: '<div class="prev"><i class="far fa-angle-left"></i></div>',
		nextArrow: '<div class="next"><i class="far fa-angle-right"></i></div>',
        responsive: [
            {
                breakpoint: 1200,
                settings: {
                    dots: false
                }
            }
        ]
    });
    var maxHeight = -1;
    $('.testimonial-slider-one .slick-slide').each(function() {
        if ($(this).height() > maxHeight) {
            maxHeight = $(this).height();
        }
    });
    $('.testimonial-slider-one .slick-slide').each(function() {
        if ($(this).height() < maxHeight) {
            $(this).css('margin', Math.ceil((maxHeight-$(this).height())/2) + 'px 0');
        }
    });
    var sliderdots= $('.testimonial-two-dots');
    $('.testimonial-slider-two').slick({
		dots: true,
		arrows: false,
        infinite: true,
		speed: 1500,
        autoplay: false,
        appendDots: sliderdots,
		slidesToShow: 1,
        slidesToScroll: 1,
        prevArrow: '<div class="prev"><i class="far fa-angle-left"></i></div>',
		nextArrow: '<div class="next"><i class="far fa-angle-right"></i></div>'
    });
    $('.testimonial-slider-three').slick({
		dots: true,
		arrows: false,
        infinite: true,
		speed: 1500,
        autoplay: true,
		slidesToShow: 2,
        slidesToScroll: 1,
        prevArrow: '<div class="prev"><i class="far fa-angle-left"></i></div>',
		nextArrow: '<div class="next"><i class="far fa-angle-right"></i></div>',
        responsive: [
            {
                breakpoint: 991,
                settings: {
                    slidesToShow: 1
                }
            }
        ]
    });
    var sliderarrows= $('.partners-arrows');
    $('.partners-slider-one').slick({
		dots: false,
		arrows: true,
        infinite: true,
		speed: 1500,
        autoplay: true,
        appendArrows: sliderarrows,
		slidesToShow: 6,
        slidesToScroll: 1,
        prevArrow: '<div class="prev"><i class="far fa-arrow-left"></i></div>',
		nextArrow: '<div class="next"><i class="far fa-arrow-right"></i></div>',
        responsive: [
            {
                breakpoint: 1199,
                settings: {
                    slidesToShow: 4
                }
            },
            {
                breakpoint: 991,
                settings: {
                    slidesToShow: 3
                }
            },
            {
                breakpoint: 767,
                settings: {
                    slidesToShow: 1
                }
            }
        ]
    });
    //====== Isotope js
    $('.portfolio-area').imagesLoaded( function() {
        // items on button click
        $('.filter-btn').on('click', 'li', function () {
            var filterValue = $(this).attr('data-filter');
            $grid.isotope({
                filter: filterValue
            });
        });
        // menu active class
        $('.filter-btn li').on('click', function (e) {
            $(this).siblings('.active').removeClass('active');
            $(this).addClass('active');
            e.preventDefault();
        });
        var $grid = $('.portfolio-grid').isotope({
            itemSelector: '.portfolio-column',
            layoutMode: 'fitRows'
        });
    });
    $('.masonry-portfolio').imagesLoaded( function() {
        // items on button click
        $('.filter-btn').on('click', 'li', function () {
            var filterValue = $(this).attr('data-filter');
            $grid.isotope({
                filter: filterValue
            });
        });
        // menu active class
        $('.filter-btn li').on('click', function (e) {
            $(this).siblings('.active').removeClass('active');
            $(this).addClass('active');
            e.preventDefault();
        });
        var $grid = $('.masonry-row').isotope({
            itemSelector: '.portfolio-column',
            percentPosition: true
        });
    });

    //===== Wow js
    
    new WOW().init();

    // Item Active
    $('.counter-area-v2').on('mouseover', '.counter-item', function() {
        $('.counter-item.item-active').removeClass('item-active');
        $(this).addClass('item-active');
    });

    //====== Parallax js

    $('.scene').each(function () {
        new Parallax($(this)[0]);
    });
    
    // page_scroll JS

    $("a.page-scroll").on('click', function (e) {
        e.preventDefault();
        var hash = this.hash;
        var position = $(hash).offset().top - 50;
        $("html").animate({
            scrollTop : position
        },1000);
    });
    //====== Pricing tab Js

    $('.pricing-nav-tab a:last-child').click(function () {
        $(this).parent('.pricing-nav-tab').addClass('for-year');
    });
    $('.pricing-nav-tab a:first-child').click(function () {
        $(this).parent('.pricing-nav-tab').removeClass('for-year');
    });

    $(function() {
        $('.video-hover').on('mouseenter', function() {
            // $(this).play();
            $('.img-video',this).fadeOut()
            $('video',this).trigger('play');
            
        })
        $('.video-hover').on('mouseleave', function() {
            // $(this).play();
            $('video',this).trigger('pause');
            $('.img-video',this).fadeIn()
        })
    })

    //==== Scroll change backround 

    $(window).scroll(function() {
        //get all elements with class ".sub"
        var $sub = $(".section-color"),
            $window = $(window),
            $main = $("body");

        var $scroll = $window.scrollTop() + $window.height() / 3;

        //for each element with class ".sub"
        $sub.each(function() {
            var $this = $(this);
            //check if it is being viewed
            if (
            $this.position().top <= $scroll &&
            $this.position().top + $this.height() > $scroll
            ) {
            //if is viewed: get its id
            //store it in className var
            var className = $this.attr("id");
            //remove color classes from the 'main' div
            $main.removeClass(function(index, css) {
                var regExp = /(^|\s)color-section-\S+/g;
                var regExpResult = css.match(regExp);
                if (regExpResult !== null) {
                regExpResult = regExpResult.join(" ");
                }
                return regExpResult;
            });
            //add class to the 'main' div (className var)
            $main.addClass(className);
            }
        });
    }).scroll();


    
})(window.jQuery);



tsParticles.load("tsparticles", {
    background: {
        color: ""
      },
      backgroundMode: {
        enable: false
      },
      detectRetina: true,
      fpsLimit: 60,
      interactivity: {
        detectsOn: ".testimonial-area",
        events: {
          onClick: {
            enable: true,
            mode: "push"
          },
          onHover: {
            enable: false,
            mode: "bubble"
          },
          resize: true
        },
        modes: {
          bubble: {
            distance: 400,
            duration: 2,
            opacity: 1,
            size: 40,
            speed: 3
          },
          push: {
            quantity: 2,
            size: 16,
          }
        }
      },
      particles: {
        rotate: {
          value: 0,
          random: true,
          direction: "clockwise",
          animation: {
            enable: false,
            speed: 5,
            sync: false
          }
        },
        move: {
            attract: { enable: false, rotateX: 1200, rotateY: 1200 },
            bounce: false,
            direction: "none",
            enable: true,
            out_mode: "bounce",
            random: false,
            speed: 3,
            straight: false
        },
        fullScreen: {
            enable: true,
            zIndex: 1
        },
        number: {
          density: {
            enable: true,
            area: 1400
          },
          value: 8
        },
        opacity: {
          value: 0.2
        },
        color: "#4b5da9",
        shape: {
          type: "circle"
        },
        size: {
            value: 80,
            random: true,
            anim: {
                enable: true,
                speed: 10,
                size_min: 16,
                sync: false
            }
        }
      }
});


tsParticles.load("tsparticles-banner", {
    background: {
        color: ""
      },
      backgroundMode: {
        enable: false
      },
      detectRetina: true,
      fpsLimit: 60,
      interactivity: {
        detectsOn: ".testimonial-area",
        events: {
          onClick: {
            enable: true,
            mode: "push"
          },
          onHover: {
            enable: false,
            mode: "bubble"
          },
          resize: true
        },
        modes: {
          bubble: {
            distance: 400,
            duration: 2,
            opacity: 1,
            size: 40,
            speed: 3
          },
          push: {
            quantity: 2,
            size: 16,
          }
        }
      },
      particles: {
        rotate: {
          value: 0,
          random: true,
          direction: "clockwise",
          animation: {
            enable: false,
            speed: 5,
            sync: false
          }
        },
        move: {
            attract: { enable: false, rotateX: 1200, rotateY: 1200 },
            bounce: false,
            direction: "none",
            enable: true,
            out_mode: "bounce",
            random: false,
            speed: 3,
            straight: false
        },
        fullScreen: {
            enable: true,
            zIndex: 1
        },
        number: {
          density: {
            enable: true,
            area: 800
          },
          value: 6
        },
        opacity: {
          value: 0.3
        },
        color: {
            value: ["#43539a","#7da6d7"]
        },
        shape: {
          type: "circle"
        },
        size: {
            value: 80,
            random: true,
            anim: {
                enable: true,
                speed: 10,
                size_min: 16,
                sync: false
            }
        }
      }
});

$('.tabs-btn a').on('mouseover', function(e) {
    $('.tabs-btn a').removeClass('active');
    $(this).addClass('active');
});

// tsParticles.load("tsparticles-footer", {
//     background: {
//         color: ""
//       },
//       backgroundMode: {
//         enable: false
//       },
//       detectRetina: true,
//       fpsLimit: 60,
//       interactivity: {
//         detectsOn: ".testimonial-area",
//         events: {
//           onClick: {
//             enable: true,
//             mode: "push"
//           },
//           onHover: {
//             enable: false,
//             mode: "bubble"
//           },
//           resize: true
//         },
//         modes: {
//           bubble: {
//             distance: 400,
//             duration: 2,
//             opacity: 1,
//             size: 40,
//             speed: 3
//           },
//           push: {
//             quantity: 2,
//             size: 16,
//           }
//         }
//       },
//       particles: {
//         rotate: {
//           value: 0,
//           random: true,
//           direction: "clockwise",
//           animation: {
//             enable: false,
//             speed: 5,
//             sync: false
//           }
//         },
//         move: {
//             attract: { enable: false, rotateX: 0, rotateY: 0 },
//             bounce: false,
//             direction: "none",
//             enable: false,
//             out_mode: "out",
//             random: false,
//             speed: 0,
//             straight: false
//         },
//         fullScreen: {
//             enable: true,
//             zIndex: 1
//         },
//         number: {
//           density: {
//             enable: true,
//             area: 800
//           },
//           value: 15
//         },
//         opacity: {
//           value: 0.3
//         },
//         color: {
//             value: ["#43539a","#7da6d7"]
//         },
//         shape: {
//           type: "circle"
//         },
//         size: {
//             value: 80,
//             random: true,
//             anim: {
//                 enable: true,
//                 speed: 10,
//                 size_min: 16,
//                 sync: false
//             }
//         }
//       }
// });

