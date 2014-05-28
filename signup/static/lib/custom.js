$(document).ready(function() {
switch_tab(0);
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
	{disabled: [1,2,3]}
	);
	$("#payment-tabs").tabs();
	$("#headings-custom-tab2").css("color","#A8A8A8");
	$("#headings-custom-tab3").css("color","#A8A8A8");
	$("#headings-custom-tab4").css("color","#A8A8A8");
  });

function newpost()
{
	var selected = [];
	$("input[name=services]:checked").each(
	function(){
	selected.push($(this).val());
	});
    console.log(selected);
	var datastring = {
		"company-name":$("#company-name").val(),
		"company-website":$("#company-website").val(),
		"company-category":$("#company-category").val(),
		"company-business-type":$("#company-business-category").val(),
		"services":selected,
		"your-name": $("#your-name").val(),
		"email":$("#email").val(),
		"phone":$("#phone").val(),
		"password":$("#password").val(),
	}
	$.ajax({
		type: 'POST',
		url:"../reg/",
		data:JSON.stringify({data:datastring}),
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		processData:false,
		success:function(data)
		{
			console.log(data);
			switch_tab(1);
		},
        failure: function(errMsg) {
                    alert(errMsg);
        }
});
}
 function switch_tab(temp) 
 {
	if(temp == 1)
	{
		$( "#tabs" ).tabs(
			{disabled:[0,2,3]}
		);
		$("#tab-2").click();
		$("#headings-custom-tab1").css("color","#00CC00");
		$("#ver1").attr("class","fa fa-check fa-stack-1x");
		$("#headings-custom-tab2").css("color","#FF9900");	

	}
	else if(temp == 2)
	{
		$( "#tabs" ).tabs(
			{disabled:[0,1,3]}
		);
		$("#tab-3").click();
		$("#headings-custom-tab2").css("color","#00CC00");
		$("#ver2").attr("class","fa fa-check fa-stack-1x");
		$("#headings-custom-tab3").css("color","#FF9900");	
	}
	else if (temp == 3)
	{
		$("#tabs").tabs({
			disabled:[0,1,2]
		});
		$("#tab-4").click();
		$("#headings-custom-tab3").css("color","#00CC00");
		$("#ver3").attr("class","fa fa-check fa-stack-1x");
		$("#headings-custom-tab4").css("color","#FF9900");		
		//add migration to pg
	}
	//have to add ajax data saving
 }
function iniPay(){

    $.get('../gencode', function(data){
            console.log(data['orderAmount']);
            $("#merchantId").val()=data['merchantId']; 
            $("#orderAmount").val()=data['orderAmount'];
            $("#merchantTxnId").val()=data['merchantTxnId'];
            $("#currency").val()=data['currency'];
            $("#companyName").val()=data['companyName'];
            $("#merchantEmail").val()=data['merchantEmail'];
            $("#secSignature").val()=data['secSignature'];
        });
}
