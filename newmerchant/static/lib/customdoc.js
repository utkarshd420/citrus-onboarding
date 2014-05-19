$(document).ready(function(){
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
      url: '../upload_file/',
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
