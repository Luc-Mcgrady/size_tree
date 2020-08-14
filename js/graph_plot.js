var urlParams = new URLSearchParams(window.location.search);
var memory_optimised = options["slow_mode"] // If false speed optimised (far faster)
var animated = options["animated_bars"]
var idpath = [sizes.i]
var bars
var heading = document.getElementById("heading")
var absolute_path = document.getElementById("absolute_path")

class Bar {
	constructor (bardata) {
		this.bardata = bardata
		// id = i, Type = t, name = n, size = s, contents = c
		
		this.newbar = document.createElement("div")
		
		var display_num
		var display_unit // Could be one variable
		

		if (bardata.s < 1000){
			display_num = bardata.s
			display_unit = "B"
		} else if (bardata.s < 1e+6) {
			display_num = (bardata.s / 1000).toFixed(2)
			display_unit = "KB"
		} else if (bardata.s < 1e+9) {
			display_num = (bardata.s / 1e+6).toFixed(2)
			display_unit = "MB"
		} else {
			display_num = (bardata.s / 1e+9).toFixed(2)
			display_unit = "GB"
		}

		
		this.newbar.innerText = ' ' + display_num + display_unit + " | " + bardata.n
		this.newbar.className = (bardata.t === 'D') ? "bar_directory" : "bar_file";
		
		var targetwidth = 100 * (bardata.s / sum)
		if (animated)
			animate_bar(this.newbar,targetwidth/4,targetwidth)
		else
			this.newbar.style.width = targetwidth + '%'
		
		document.getElementsByClassName("graph")[0].appendChild(this.newbar)
		if (this.bardata.t === 'D')
			if (memory_optimised)
				this.newbar.onclick = this.change_url_id.bind(this)
			else
				this.newbar.onclick = this.change_dir_id.bind(this)
	}
	
	change_url_id() { //Changes the current dir in the memory optimised way.
		//console.log(this.bardata)
		window.location.replace("graph.html?id=" + this.bardata.i );
	}
	
	change_dir_id() {
		//console.log(this.bardata)
		idpath.push(this.bardata.i)
		plotUid(sizes, this.bardata.i)
		absolute_path.innerText += '\\' + this.bardata.n 
	}
}

function find_uid(d, uid) { // Returns the path with the uid and the paths parent
	if (d.i === uid) return [d, undefined]
	if (d.t === 'D')
		for (var i = 0; i < d.c.length; i++) {
			let result = find_uid(d.c[i], uid)
			if (result != undefined) {
				if (result[1] == undefined)
					result[1] = d
					return result
				return result
			}	
		}
}

function plot_data(gd) { // graphdata
	unplot()
	
		heading.innerText = gd.n
	
	sum = 0
	gd.c.forEach(function (item) {
		sum += item.s
	})

	gd.c.sort( function(a, b){return b.s - a.s } )
	var maxval = gd.c.reduce(function(a, b) {return (a.s > b.s) ? a: b;}).s

	var bars = []
	gd.c.forEach(function(item){
		bars.push(new Bar(item)) 
	})
	return bars
} 

function plotUid(data, uid) {

	let result = find_uid(data, uid)
	let values = result[0] 
	var prevdir = result[1]

	let graphdata = values.c
	
	let parentdata = values

	document.title = values.n

	
	return plot_data(values)
}

function unplot() {
	let graph_parent = document.getElementsByClassName("graph")[0]
	while (graph_parent.childNodes.length > 0) 
		graph_parent.removeChild(graph_parent.childNodes[0])
}

function animate_bar(elem, start, end) { //Start and end are ints repersenting persentages
	elem.style.width = start + "%"
	let currentwidth = parseFloat(elem.style.width.slice(0,elem.style.width.length-1))
	if (currentwidth < end) {
		var nextwidth = currentwidth + ((end - currentwidth) / 20) + 0.01
		setTimeout(function(){animate_bar(elem,nextwidth,end)}, 10) //100 ups
	} else {
		elem.style.width = end + "%" 
	}
}

if (memory_optimised)
	heading.onclick = function(){
		window.location.replace("graph.html?id=" + prevdir.i );
	}
else
	heading.onclick = function(){
		if (idpath.length > 1) {
			idpath.pop(-1)
			plotUid(sizes, idpath[idpath.length - 1])
			
			let foo = absolute_path.innerText.split("\\")
			absolute_path.innerText = foo.slice(0,foo.length-1).join('\\')
		}
	}


absolute_path.innerText += sizes.n
if (memory_optimised) {
	if (urlParams.get("id") != null && urlParams.get("id") != sizes.i)
		var bars = plotUid(sizes, parseInt(urlParams.get("id")))
	else
		var bars = plot_data(sizes)
	sizes = undefined	//save memory
} else {
	var bars = plot_data(sizes)
}
