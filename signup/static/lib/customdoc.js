$(document).ready(function(){
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
$("input[type='file']").change(function(){
var id = this.id
$('progress[name='+id+']').show()
var fd = new FormData();
fd.append( this.id, $('#'+this.id)[0].files[0]);
    $.ajax( {
   xhr: function()
   {
     var xhr = new window.XMLHttpRequest();
     //Upload progress
     xhr.upload.addEventListener("progress", function(evt){
       if (evt.lengthComputable) {
         var percentComplete = evt.loaded / evt.total;
	$('progress[name='+id+']').val(percentComplete*100);
         console.log(percentComplete);
       }
     }, false);
     //Download progress
     xhr.addEventListener("progress", function(evt){
       if (evt.lengthComputable) {
         var percentComplete = evt.loaded / evt.total;
        // console.log(percentComplete);
       }
     }, false);
     return xhr;
   },
      url: '../../uploadfiles/',
      type: 'POST',
      data: fd,
      processData: false,
      contentType: false,
      success: function(data){
	$('label[name='+id+']').css('color','green');
}
    } );
 
});
});
