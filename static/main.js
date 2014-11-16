
$(function() {

(function poll() {
   setTimeout(function() {
       $.ajax({ url: "http://131a46b7.ngrok.com/params", success: function(data) {
            $("#volume").text(data.volume + "%");
            $("#volume-bar").css("width", data.volume + "%");
            $("#speed").text(data.speed + "%")
            $("#speed-bar").css("width", String(parseInt(data.speed)/2.0) + "%");
            $("#pan").text(String(parseInt(data.pan*2-100)) + "%")
            $("#pan-bar").css("width", data.pan + "%");
            $("#eq0 div div").css("height", data.eq0 + "%");
            $("#eq0-value").text(String(Math.round((data.eq0-50.0)/50.0*15.0*100)/100) + " dB")
            $("#eq1 div div").css("height", data.eq1 + "%");
            $("#eq1-value").text(String(Math.round((data.eq1-50.0)/50.0*15.0*100)/100) + " dB")
            $("#eq2 div div").css("height", data.eq2 + "%");
            $("#eq2-value").text(String(Math.round((data.eq2-50.0)/50.0*15.0*100)/100) + " dB")
            $("#eq3 div div").css("height", data.eq3 + "%");
            $("#eq3-value").text(String(Math.round((data.eq3-50.0)/50.0*15.0*100)/100) + " dB")
            $("#eq4 div div").css("height", data.eq4 + "%");
            $("#eq4-value").text(String(Math.round((data.eq4-50.0)/50.0*15.0*100)/100) + " dB")
            $("#song").text(data.track)
       }, dataType: "json", complete: poll });
    }, 400);
})();

});