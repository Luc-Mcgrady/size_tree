var graphdata = data.c
delete data.c
var parentdata = data

document.getElementById("heading").innerHTML = data.n
document.title = data.n

data = undefined

// Format the data to reduce background ram usage

graphdata.forEach(function (item) {
    delete item.c
})

graphdata.sort( function(a, b){return b.s - a.s } )
var maxval = graphdata.reduce(function(a, b) {return (a.s > b.s) ? a: b;}).s

function index_on_uid(uid) {
	
}

class Bar {
	constructor (bardata) {
		this.bardata = bardata
		var sel = this
		this.onclicked = function() {
			console.log(sel.bardata)
			if (sel.bardata.t === 'D')
			window.location.replace("graph.html?id=" + sel.bardata.i);
		}
		
		this.newbar = document.createElement("div")
		
		this.newbar.innerHTML = ' ' + (bardata.s / 1e+6) + " MB  " + bardata.n
		this.newbar.className = (bardata.t === 'D') ? "bar_directory" : "bar_file";
		this.newbar.style.width = 75 * (bardata.s / maxval) + '%'
		
		document.getElementsByClassName("graph")[0].appendChild(this.newbar)
		this.newbar.onclick = this.onclicked
	}
}

var bars = []
graphdata.forEach(function(item){
	bars.push(new Bar(item, maxval)) 
})
