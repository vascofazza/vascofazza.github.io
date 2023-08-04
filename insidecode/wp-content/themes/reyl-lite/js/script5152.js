jQuery(document).ready(function($) {

			//Anomation at load -----------------
			Pace.on('done', function(event) {
				
			});//Pace


			$("body").on('click', 'article a[href^="'+window.location.origin+'"]', function(event) {
				event.preventDefault();
				/* Act on the event */
				$(".ql-animations #main article").each(function(index, el) {
					$(el).addClass('ql_clicked');
				});
				var target = $(this).attr('href');
				 setTimeout(function() {
			       window.location.href = target;
			    }, 600);
			});

			$(".ql_scroll_top").click(function() {
			  $("html, body").animate({ scrollTop: 0 }, "slow");
			  return false;
			});

			$("#primary-menu > li > ul > li.dropdown").each(function(index, el) {
				$(el).removeClass('dropdown').addClass('dropdown-submenu');
			});

			$('.dropdown-toggle').dropdown();

			$('*[data-toggle="tooltip"]').tooltip();

});