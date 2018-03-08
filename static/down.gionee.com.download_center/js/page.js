function setPageBtn(name, b, val) {
	if (document.all[name]) {
		if (document.all[name].length) {
			for (var i = 0; i < document.all[name].length; i++) {
				if (b) {
					document.all[name][i].disabled = true;
				} else {
					document.all[name][i].href = val;
				}
			}
		} else {
			if (b) {
				document.all[name].disabled = true;
			} else {
				document.all[name].href = val;
			}
		}
	}
}
function disablePageBtn(name) {
	if (document.all[name]) {
		if (document.all[name].length) {
			for (var i = 0; i < document.all[name].length; i++) {
				document.all[name][i].disabled = true;
			}
		} else {
				document.all[name].disabled = true;
		}
	}
}
function setInnerHTML(name, val) {
	if (document.all[name]) {
		if (document.all[name].length) {
			for (var i = 0; i < document.all[name].length; i++) {
				document.all[name][i].innerHTML = val;
			}
		} else {
			document.all[name].innerHTML = val;
		}
	}
}
function pageInit() {
	recCnt = parseInt(recCnt);
	pageCnt = parseInt(pageCnt);
	currentPage = parseInt(currentPage);
	if (isNaN(currentPage)) {
		currentPage = 1;
	}
	if(cPageObj.selectedIndex){
		alert("ASdfsf");
		cPageObj.length=pageCnt;
		for(var i=0;i<cPageObj.length;i++){
			if(i==(currentPage-1)){
				cPageObj.selectedIndex=i;
			}
			cPageObj[i].value=cPageObj[i].text=(i*1)+1;
		}
		//cPageObj.onChange=submitPage;
	}
	setInnerHTML("RECCnt", recCnt);
	setInnerHTML("PageCnt", pageCnt);
	setInnerHTML("CPage", currentPage);
	setPageBtn("FirstPage", (currentPage < 2), "javascript:gotoPage(1)");
	setPageBtn("PrevPage", (currentPage < 2), "javascript:gotoPage(currentPage-1)");
	setPageBtn("NextPage", (currentPage >= pageCnt), "javascript:gotoPage(currentPage+1)");
	setPageBtn("LastPage", (currentPage >= pageCnt), "javascript:gotoPage(pageCnt)");
}
function setPageFormWait() {
}
function pageInputEnter(){
	if (window.event.keyCode==13){
		window.event.returnValue = false;
		submitPage();
	}
}

function submitPage() {
	if(!cPageObj.selectedIndex){
		if((cPageObj.value=="") || isNaN(cPageObj.value)){
			alert("��������ȷ��ҳ�롣");
			cPageObj.value=currentPage;
			return;
		}
		var p=parseInt(cPageObj.value);
		if(p<1){
			cPageObj.value=1;
		}
		if(p>pageCnt){
			cPageObj.value=pageCnt;
		}
		p=parseInt(cPageObj.value);
		if(currentPage==p){
			//return;
		}
	}
	setPageFormWait();
	submitPageForm();
}
function submitPageForm(){
	disablePageBtn("FirstPage", true, "javascript:gotoPage(1)");
	disablePageBtn("PrevPage", true, "javascript:gotoPage(currentPage-1)");
	disablePageBtn("NextPage", true, "javascript:gotoPage(currentPage+1)");
	disablePageBtn("LastPage", true, "javascript:gotoPage(pageCnt)");
	for(var i=0;i<cPageObj.form.elements.length;i++){
		cPageObj.form.elements[i].className="disablePageForm";
	}
	cPageObj.form.className="disablePageForm";
	cPageObj.form.submit();
}

function gotoPage(pageInx) {
	setPageFormWait();
	if(cPageObj.selectedIndex){
		cPageObj.selectedIndex=pageInx-1;
	}else{
		cPageObj.value = pageInx;
	}
	submitPageForm();
}

function isNum(e)
{
  if(e * 1 != e)
    {
       return false;
     }
   else
     {
        return true;
      }
}
String.prototype.trim = function () {
	return this.replace(/(^\s*)|(\s*$)/g, "");
};
