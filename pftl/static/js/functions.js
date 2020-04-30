;(function($, window, document, undefined) {
	var $win = $(window);
	var $doc = $(document);

	$doc.ready(function() {

		$('.field').focus(function() {
	        $(this).parents('.field-wp').addClass('focused');
	    }).blur(function(){
	        $(this).parents('.field-wp').removeClass('focused');
	    });

	    if( $('.current-year').length ){
	    	var year = new Date().getFullYear();
	    	$('.current-year').html(year);
	    }

	    $('.toc a').on('touchstart click', function() {
		  	var $el = $(this);
		  	var id = $el.attr('href');
		  
			$('html, body').animate({
				scrollTop: $(id).offset().top
			}, 500);
		  
			// event.preventDefault();
		});

	    $('.menu-btn').click(function(event){
			$('.header').toggleClass('opened');
			$('.intro').toggleClass('opened');
			event.preventDefault();
		});

	   $('.subscribe-fixed .action').on('click', function(event){
	   		$(this).parent().toggleClass('opened');
	   		event.preventDefault();
	   })

	    $win.on('scroll', function(){
	    	var top = document.documentElement.scrollTop;
	    	
	    	if( top >= '500' ){
	    		$('.subscribe-fixed').addClass('show');
	    	} else {
	    		$('.subscribe-fixed').removeClass('show');
	    	}

	    });
		
	});

	// $win.load(function() {
		
	// });

})(jQuery, window, document);
