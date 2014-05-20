$(document).ready(function() {
$.ajaxSetup({ 
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                 if (cookie.substring(0, name.length + 1) == (name + '=')) {
                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                     break;
                 }
             }
         }
         return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     } 
});
    $( "#tabs" ).tabs(
	{disabled: [1,2]}
	);
	$("#payment-tabs").tabs();
	$("#headings-custom-tab2").css("color","#A8A8A8");
	$("#headings-custom-tab3").css("color","#A8A8A8");
  });

function newpost()
{
	var company_name= $("#company-name").val();
	var company_category = $("#company-category").val();
	var your_name = $("#your-name").val();
	var email = $("#email").val();
	var phone= $("#phone").val();
	var password = $("#password").val();
	var datastring = 'company-name=' +company_name +'&company-category='+company_category+'&your-name='+your_name+'&email='+email+'&phone='+phone+'&password='+password;
	$.ajax({
		url:"../reg/",
		data:datastring,
		processData:false,
		type: 'POST',
		success:function(data)
		{
			console.log(data);
			switch_tab(0);
		}
});
}
 function switch_tab(temp) 
 {
	if(temp == 0)
	{
		$( "#tabs" ).tabs(
			{disabled:[0,2]}
		);
		$("#tab-2").click();
		$("#headings-custom-tab1").css("color","#00CC00");
		$("#ver1").attr("class","fa fa-check fa-stack-1x");
		$("#headings-custom-tab2").css("color","#FF9900");	

	}
	else if(temp == 1)
	{
		$( "#tabs" ).tabs(
			{disabled:[0,1]}
		);
		$("#tab-3").click();
		$("#headings-custom-tab2").css("color","#00CC00");
		$("#ver2").attr("class","fa fa-check fa-stack-1x");
		$("#headings-custom-tab3").css("color","#FF9900");	
	}
	else if (temp == 2)
	{
		$("#ver3").attr("class","fa fa-check fa-stack-1x");
		//add migration to pg
	}
	//have to add ajax data saving
 }
