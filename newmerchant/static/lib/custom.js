$(document).ready(function() {
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
//	alert(1); 
	var datastring = 'company-name=' +company_name +'&company-category='+company_category+'&your-name='+your_name+'&email='+email+'&phone='+phone+'&password='+password;
//	formData = new FormData(e.target);
	$.ajax({
		url:"../new/",
		data:datastring,
		processData:false,
		type: 'POST',
		success:function(data)
		{
		//	alert(data);
			alert("Account Created");
			console.log(data);
			switch_tab(0);
		}
});
}
//	});  
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
		//submit data via ajax

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
