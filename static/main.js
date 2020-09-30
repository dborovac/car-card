var url = "https://colormind.io/api/";
var data = {
	model : "default",
	input : ["N","N","N","N","N"]
}

function changeClr() {
        var http = new XMLHttpRequest();
        http.setRequestHeader('Access-Control-Allow-Origin', '*');

        http.onreadystatechange = function() {
	        if(http.readyState == 4 && http.status == 200) {
                var palette = JSON.parse(http.responseText).result;
        
                let card = document.getElementsByClassName('card');
                let stats = document.getElementsByClassName('stats');

                card[0].style.backgroundColor = rgbToHex(palette[0][0], palette[0][1], palette[0][2]);
                stats[0].style.backgroundColor = rgbToHex(palette[1][0], palette[1][1], palette[1][2]);
                stats[0].style.borderColor = rgbToHex(palette[2][0], palette[2][1], palette[2][2]);
	        }
        }
        http.open("POST", url, true);
        http.send(JSON.stringify(data));
}

function rgbToHex(r, g, b) {
        r = r.toString(16);
        g = g.toString(16);
        b = b.toString(16);

        if (r.length == 1) r = "0" + r;
        if (g.length == 1) g = "0" + g;
        if (b.length == 1) b = "0" + b;

        return "#" + r + g + b;
}