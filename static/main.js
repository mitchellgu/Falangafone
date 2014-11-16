
$(function() {

(function poll() {
   setTimeout(function() {
       $.ajax({ url: "http://131a46b7.ngrok.com/params", success: function(data) {
            $("#height").text(data.height);
       }, dataType: "json", complete: poll });
    }, 250);
})();

});