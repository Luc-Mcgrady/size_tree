function find_uid(d, uid) {
	if (d.i === uid) return d
	if (d.t === 'D')
		for (var i = 0; i < d.c.length; i++) {
			let result = find_uid(d.c[i], uid)
			if (result != undefined) {
				if (result.length != undefined) // Bad, TODO needs replacing
					return result
				return [result, d]
			}	
		}
}

var urlParams = new URLSearchParams(window.location.search);

console.log(data.i)

if (urlParams.get("id") != null && urlParams.get("id") != data.i){
	let result = find_uid(data, parseInt(urlParams.get("id")))
	data = result[0]
	var prevdir = result[1]
}

var graphdata = data.c
delete data.c	//save memory
var parentdata = data

let heading = document.getElementById("heading")
heading.innerHTML = data.n
heading.onclick = function(){
	window.location.replace("graph.html?id=" + prevdir.i );
}

document.title = data.n

data = undefined	//save memory

sum = 0
graphdata.forEach(function (item) {
    delete item.c
	sum += item.s
})

graphdata.sort( function(a, b){return b.s - a.s } )
var maxval = graphdata.reduce(function(a, b) {return (a.s > b.s) ? a: b;}).s

class Bar {
	constructor (bardata) {
		this.bardata = bardata
		var sel = this
		
		this.onclicked = function() {
			console.log(sel.bardata)
			if (sel.bardata.t === 'D')
			window.location.replace("graph.html?id=" + sel.bardata.i );
		}
		
		this.newbar = document.createElement("div")
		
		this.newbar.innerHTML = ' ' + (bardata.s / 1e+6) + " MB  " + bardata.n
		this.newbar.className = (bardata.t === 'D') ? "bar_directory" : "bar_file";
		this.newbar.style.width = 100 * (bardata.s / sum) + '%'
		
		document.getElementsByClassName("graph")[0].appendChild(this.newbar)
		this.newbar.onclick = this.onclicked
	}
}

var bars = []
graphdata.forEach(function(item){
	bars.push(new Bar(item)) 
})
