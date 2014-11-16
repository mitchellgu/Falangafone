
$(function() {

(function poll() {
   setTimeout(function() {
       $.ajax({ url: "http://131a46b7.ngrok.com/params", success: function(data) {
            $("#volume").text(data.volume);
            $("#volume-bar").css("width", data.volume + "%");
            $("#speed").text(data.speed)
            $("#speed-bar").css("width", String(parseInt(data.speed)/2.0) + "%");
       }, dataType: "json", complete: poll });
    }, 150);
})();

});