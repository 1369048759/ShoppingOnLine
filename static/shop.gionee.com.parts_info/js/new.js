
function redu(){

	var result = document.getElementById("iptQuantityQum").value;
	if(result > 1){
		result = parseInt(result) - 1;
		document.getElementById("iptQuantityQum").value = result;
		document.getElementById("infoProductNum").innerText = result;


	}
	if(result == 1){
		var div = document.getElementById("redu");
		div.setAttribute("class", 'ui_quantity_redu ui_quantity_redu_dis')
	}
}

function add(){
	var price = document.getElementById("goodsPrice").value;
	var result = document.getElementById("iptQuantityQum").value;
	if(result > 0){
		var div = document.getElementById("redu");
		div.setAttribute("class", 'ui_quantity_redu')
	}
	result = parseInt(result) + 1;
	document.getElementById("iptQuantityQum").value = result;
	document.getElementById("infoProductNum").innerText = result;

}
