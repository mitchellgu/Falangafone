
$(function() {

(function poll() {
   setTimeout(function() {
       $.ajax({ url: "http://131a46b7.ngrok.com/params", success: function(data) {
            $("#volume").text(data.volume);
            $("#speed").text(data.speed)
       }, dataType: "json", complete: poll });
    }, 250);
})();

});