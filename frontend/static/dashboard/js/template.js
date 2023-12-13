if (typeof jQuery === "undefined") {
    throw new Error("jQuery plugins need to be before this file");
}

$(function() {
    "use strict";

    // main sidebar toggle js
    $('.menu-toggle').on('click', function () {
        $('.sidebar').toggleClass('open');
        $('.open').removeClass('sidebar-mini');
    });

    // layout a sidebar mini version
    $('.sidebar-mini-btn').on('click', function () {
        $('.sidebar').toggleClass('sidebar-mini');
        $('.sidebar-mini').removeClass('open');
    });

    // chat page chatlist toggle js
    $('.chatlist-toggle').on('click', function () {
        $('.card-chat').toggleClass('open');
    });

    $(".theme-rtl input").on('change',function() {
        if(this.checked) {
            $("body").addClass('rtl_mode');
        }else{
            $("body").removeClass('rtl_mode');
        }
       
    });

    // cSidebar overflow daynamic height
    
    overFlowDynamic();

    $(window).resize(function(){
        overFlowDynamic();
    });

    function overFlowDynamic(){ 
        var sideheight=$(".sidebar.sidebar-mini").height() + 48;
        
        if(sideheight <= 760) {  
            $(".sidebar.sidebar-mini").css( "overflow", "scroll");  
        }
        else{
            $(".sidebar.sidebar-mini").css( "overflow", "visible"); 
        }
    }
    

    // Dropdown scroll hide using table responsive
    
    $('.table-responsive').on('show.bs.dropdown', function () {
        $('.table-responsive').css( "overflow", "inherit" );
    });
   
    $('.table-responsive').on('hide.bs.dropdown', function () {
            $('.table-responsive').css( "overflow", "auto" );
    })

    // light and dark theme setting js
    var toggleSwitch = document.querySelector('.theme-switch input[type="checkbox"]');
    var toggleHcSwitch = document.querySelector('.theme-high-contrast input[type="checkbox"]');
    var currentTheme = localStorage.getItem('theme');
    if (currentTheme) {
        document.documentElement.setAttribute('data-theme', currentTheme);
    
        if (currentTheme === 'dark') {
            toggleSwitch.checked = true;
        }
        if (currentTheme === 'high-contrast') {
            toggleHcSwitch.checked = true;
            toggleSwitch.checked = false;
        }
    }
    function switchTheme(e) {
        // if (e.target.checked) {
        //     document.documentElement.setAttribute('data-theme', 'dark');
        //     localStorage.setItem('theme', 'dark');
        //     $('.theme-high-contrast input[type="checkbox"]').prop("checked", false);
        // }
        // else {        
        //     document.documentElement.setAttribute('data-theme', 'light');
        //     localStorage.setItem('theme', 'light');
        // }    
    }
    // toggleSwitch.addEventListener('change', switchTheme, false);
    // end
});

// live support team js
// $(function() {
//     "use strict";
//     var Tawk_API=Tawk_API||{}, Tawk_LoadStart=new Date();
//     (function(){
//         var s1=document.createElement("script"),s0=document.getElementsByTagName("script")[0];
//         s1.async=true;
//         s1.src='https://embed.tawk.to/6051a040f7ce18270930e55a/1f0vdjvfu';
//         s1.charset='UTF-8';
//         s1.setAttribute('crossorigin','*');
//         s0.parentNode.insertBefore(s1,s0);
//     })();
// });

$('.quest-box').each(function(){
    var $this = $(this)

    $('.bookmark-icon input[type="checkbox"]', $this).on('change', function() {
      if ($(this).is(':checked')) {
          $('.section-question a').each(function() {
              if ($(this).data('name') === $this.attr('id')) {
                  $(this).addClass('has-bookmark')
              }
          })
      } else {
        $('.section-question a').each(function() {
          if ($(this).data('name') === $this.attr('id')) {
              $(this).removeClass('has-bookmark')
          }
        })
      }
    })
    
    $('.section-content input[type="radio"]', $this).on('change', function() {
        if ($(this).is(':checked')) {
            $('.section-question a').each(function() {
                if ($(this).data('name') === $this.attr('id')) {
                    $(this).addClass('has-answer')
                }
            })
        }
    })
})


function filterQuiz() {
    $('.list-filter-bookmark').each(function() {
      $('#all-bookmark').on('click', function() {
        $('.section-question li a').show();
        console.log('a');
        $('.list-filter-bookmark li a').removeClass('active');
        $(this).addClass('active');
      })
      $('#bookmarked').on('click', function() {
        $('.section-question li a').hide();
        $('.section-question li a.has-bookmark').show();
        $('.list-filter-bookmark li a').removeClass('active');
        $(this).addClass('active');
      })
      $('#unbookmarked').on('click', function() {
        $('.section-question li a.has-bookmark').hide();
        $('.section-question li a:not(.has-bookmark)').show();
        $('.list-filter-bookmark li a').removeClass('active');
        $(this).addClass('active');
      })
    })
}

filterQuiz();

$('#btn-show-list').on('click', function(){
  $('.list-question-menu').slideToggle()
})

$('.hide-quiz-list').on('click', function(){
  $('.list-question-menu').slideUp()
})
// $(".sticky_column").stick_in_parent({
//     offset_top: 200,
//     inner_scrolling: true,
//     parent: '.sticky-container'
// });
// var stickyEl = new Sticksy('.sticky_column', {
//     topSpacing: 100,
//     listen: true,
// })

var a = $('.current-quiz').html();
function Test() {
  
  // var b = $('.total-quiz').html();
  this.current = parseInt(a);
  this.init();
  this.initEvent();
  
}

Test.prototype.init = function () {
  this.$checkPoints = $(".section-item-link input");
  this.$questionAreas = $(".quest-box");
  this.totalLength = this.$questionAreas.length;
  this.total = this.$questionAreas.length + this.current - 1 ;
  this.$boxLiActive = $('.section-question li a')
  this.$boxActive = $('.section-question li');
};
Test.prototype.initEvent = function () {
  var _this = this;
  
  $(".section-question a").click(function() {
    var data = $(this).data('name');
    // console.log(data)
    _this.$questionAreas.css("display", "none");
    _this.$boxActive.removeClass('active')

    $(this).parent('li').addClass('active')
    // _this.current = $(this).parent('li').index();
    // _this.currentIndex = $(this).parent('li').index()
    var c = $(this).html()
    _this.current = parseInt(c)
    console.log(_this.current)
    
    $("#" + data).fadeIn(); 
    $('.current-quiz').html(_this.current)
    if (_this.current == _this.total) {
      $('.next-question').addClass('btn-disable')
    }
    if (_this.current < _this.total) {
      $('.next-question').removeClass('btn-disable')
    }
    
    if (_this.current - 1 < _this.total) {
      $('.prev-question').removeClass('btn-disable')
    }
    if (_this.current == a) {
      $('.prev-question').addClass('btn-disable')
    }
  }) 
  $(".next-question").click(function (e) {
    
    e.preventDefault();
    // console.log(_this.current)
    var d = _this.total - _this.totalLength;
    console.log(_this.total)
    if (_this.current == _this.total) {
   
      return;
    } else if (_this.current < _this.total) {
      

      $('.section-question li[data-li = '+ (_this.current) +']').removeClass('active');
      $('.section-question li[data-li = '+ (_this.current + 1) +']').addClass('active');
       
     
      $('.quest-box[data-quest = '+ (_this.current) +']').hide();
      $('.quest-box[data-quest = '+ (_this.current + 1) +']').fadeIn();
      // $(_this.$questionAreas[_this.current - 1]).fadeIn();
      _this.current++;
      $('.current-quiz').html(_this.current)
      $('.prev-question').removeClass('btn-disable')
      
    }
    if (_this.current == _this.total) {
      $(this).addClass('btn-disable')
    }
  });
  $(".prev-question").click(function (e) {
    e.preventDefault();
    if (_this.current >= 0) {
      console.log('a')

      $('.next-question').removeClass('btn-disable')
      $('.section-question li[data-li = '+ (_this.current) +']').removeClass('active');
      $('.section-question li[data-li = '+ (_this.current - 1) +']').addClass('active');

      $('.quest-box[data-quest = '+ (_this.current) +']').hide();
      $('.quest-box[data-quest = '+ (_this.current - 1) +']').fadeIn();
     
  
      _this.current--;

      
      $('.current-quiz').html(_this.current)
    }

    if (_this.current == a) {
      $(this).addClass('btn-disable')
    }
  });
  $('.quest-box input').click(function () {
    // console.log('aaaa');
    if ($(this).closest('.quest-box').find('input:checked').length >= 1) {
      $(this).closest('.quest-box').find('.next-question').prop('disabled', false);
    }
    else {
      $(this).closest('.quest-box').find('.next-question').prop('disabled', true);
    }
  });
};

new Test();


$('.vid-list-container a').on('click', function() {
  $('.vid-list-container a').removeClass('active')
  $(this).addClass('active')
  var a = $(this).attr('data-video-title');
  $('.title-video').text(a)
})

document.addEventListener("DOMContentLoaded", e => {
  let card_number_input = document.querySelector("#card-number"),
      card_number_display = document.querySelector("div#card .card-number");
  


  
  let cvc_input = document.querySelector(".cvc input");
      // cvc_display = document.querySelector(".cvc > span:nth-child(2)");

  // let form = document.querySelector("form");
  
  card_number_input.onkeydown = e => { 
    let key = e.keyCode || e.charCode;
    
    let is_digit = (key >= 48 && key <= 57) || (key >= 96 && key <= 105);
    let is_delete = key == 8 || key == 46;
    
    if (is_digit || is_delete) { 
      let text = e.target.value;
      let len = text.length;
      
      if(is_digit && (len==4 || len==9 || len==14))
        card_number_input.value = text + " ";
    }      
    else return false;
  }
  
  card_number_input.onkeyup = e => { 
    let key = e.keyCode || e.charCode;
    
    let is_digit = (key >= 48 && key <= 57) || (key >= 96 && key <= 105);
    let is_delete = key == 8 || key == 46;
    
    if (is_digit || is_delete) { 
      let text = e.target.value;
      let len = text.length;
      let digits = "XXXX XXXX XXXX XXXX".split('');
      
      if(is_digit && (len==4 || len==9 || len==14))
        digits[len] = " ";

      for(let i=0;i<len;i++)
        digits[i] = text.charAt(i);

      // card_number_display.innerText = digits.join('');
    }      
    else return false;
  }
  

  


  cvc_input.onkeyup = e => {
    let text = e.target.value;
    let digits = ['_','_','_'];

    for(let i=0;i<text.length;i++)
      digits[i] = text.charAt(i);

    // cvc_display.innerText = digits.join('');
  }
  
  // form.onsubmit = e => {
  //   e.preventDefault();
  // }
});



$('.box-radio input[type="radio"]').on('change', function(){
  console.log('aaa')
  var a = $(this).attr('id');
  console.log(a)
  if ($('input#' + a).is(':checked')) {
      $('.check-info').slideUp(); 
      $('.check-info[data-id="' + a + '"]').slideDown(); 
      
  }
  // if ($('input#phacmacy-pick').is(':checked')) {
      
  //     setTimeout(() => {
  //         $('.phacmacy-tab').fadeIn();
  //     }, 300);
  //     $('.deliver-tab').fadeOut();
  //     $('.deliver-tab input').prop('required', false)
  // }

  
})