
$(function() {

(function poll() {
   setTimeout(function() {
       $.ajax({ url: "http://131a46b7.ngrok.com/params", success: function(data) {
            $("#volume").text(data.volume);
            $("#volume-bar").css("width", data.volume + "%");
            $("#speed").text(data.speed)
            $("#eq0 div div").css("height", data.eq0 + "%");
            $("#eq1 div div").css("height", data.eq1 + "%");
            $("#eq2 div div").css("height", data.eq2 + "%");
            $("#eq3 div div").css("height", data.eq3 + "%");
            $("#eq4 div div").css("height", data.eq4 + "%");
       }, dataType: "json", complete: poll });
    }, 250);
})();

});