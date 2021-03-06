//翻页组件
function $page(opt) {
	var option = {
		keyId : Math.random(),
		pageCount : 0,
		currentPage : 0,
		itemCount : 0,
		more : false,
		domList : [],
		type : "full",
		action : "url",
		url : "http://www.xxx.com/?pid={#pageId#}",
		func : function(pageId, opt) {
			return true;
		},
		onInit : function(pageId, opt) {
			return true;
		}
	};
	for (var i in opt) {
		option[i] = opt[i];
	}
	var standStyle = ['', '{#goTo#}<a href="#nolink" pageTag="go" pageId="{#pageId#}">{#pageId#}</a>{#goTo/#} {#current#}<a class=\"ui_page_curr\" href=\"javascript:void(0);\">{#pageId#}</a>{#current/#}{#hide#}<span class="page-break">...</span>{#hide/#}{#next#}<a href="#nolink" class="page-next" pageTag="go" pageId="{#pageId#}">下一页</a>{#next/#}{#_next#}<a class=\"page-next\" href=\"javascript:void(0);\">下一页</a>{#_next/#}{#previou#}<a href="#nolink" pageTag="go" pageId="{#pageId#}" class="page-prev">上一页</a>{#previou/#}{#_previou#}<a class=\"page-next\" href=\"javascript:void(0);\">上一页</a>{#_previou/#}{#first#}{#first/#}{#_first#}{#_first/#}{#last#}{#last/#}{#_last#}{#_last/#}{#more#}<span class="page-break">...</span>{#more/#}{#_more#}{#_more/#}'];
	var templateList = {
		full : [standStyle[0], standStyle[1], '<div class="paginator">{#previousPage#}{#pageList#}{#morePage#}{#nextPage#}<span class="page-skip"> 到第<input type="text" name="inputItem" pageTag="input" value="{#currentPageId#}"  maxlength="{#maxlength#}" {#debugtag#} />页<button pageTag="jumper" value="go">确定</button></span></div>'],
		simple : [standStyle[0], standStyle[1], '<div class="paginator">{#previousPage#}{#pageList#}{#morePage#}{#nextPage#}</div>'],
		shortSimple : [standStyle[0], standStyle[1], '<div class="paginator">{#previousPage#}{#shortPageList#}{#morePage#}{#nextPage#}</div>'],
		miniSimple : [standStyle[0], standStyle[1], '<div class="paginator">{#previousPage#}{#miniPageList#}{#nextPage#}</div>'],
		noLastTmpl : [standStyle[0], standStyle[1], '<div class="paginator">{#previousPage#}{#noLastTmpl#}{#nextPage#}</div>']
	};
	var template = templateList[option.type][0] + templateList[option.type][1] + templateList[option.type][2];
	var pageCount = parseInt(option.pageCount);
	var currentPage = parseInt(option.currentPage);
	var itemCount = parseInt(option.itemCount);
	currentPage = (currentPage > pageCount) ? pageCount : currentPage;
	var pt = {
		next : "",
		_next : "",
		previou : "",
		_previou : "",
		first : "",
		_first : "",
		last : "",
		_last : "",
		more : "",
		_more : "",
		goTo : "",
		current : "",
		hide : ""
	};
	for (var i in pt) {
		var r = (new RegExp("{#" + i + "#}(.*){#" + i + "/#}", "ig")).exec(template);
		pt[i] = (r) ? RegExp.$1 : "";
	}
	pt.nextPageHtml = (currentPage < pageCount) ? (pt.next.replace(/{#pageId#}/g, (currentPage + 1))) : (pt._next);
	pt.previousPageHtml = (currentPage > 1) ? (pt.previou.replace(/{#pageId#}/g, (currentPage - 1))) : (pt._previou);
	pt.firstPageHtml = (currentPage > 1) ? (pt.first.replace(/{#pageId#}/g, 1)) : (pt._first);
	pt.lastPageHtml = (currentPage < pageCount) ? (pt.last.replace(/{#pageId#}/g, pageCount)) : (pt._last);
	pt.morePageHtml = (option.more) ? (pt.more.replace(/{#pageId#}/g, (pageCount + 1))) : (pt._more);
	pt.pagelistHtml = "";
	pt.shortPageListHtml = "";
	pt.noLastTmplHtml = "";
	pt.miniPageListHtml = "<span>" + currentPage + "/" + pageCount + "</span>";
	
	if (pageCount <= 10) {
		for (var i = 1; i <= pageCount; i++) {
			pt.pagelistHtml += (i == currentPage) ? (pt.current.replace(/{#pageId#}/g, i)) : (pt.goTo.replace(/{#pageId#}/g, i));
		}
	} else {
		var prePage = currentPage - 2;
		var frePage = currentPage + 2;
		prePage = (prePage <= 2) ? 1 : prePage;
		frePage = (frePage > pageCount - 2) ? pageCount : frePage;
		if (currentPage <= 4) {
			frePage = 6
		}
		pt.pagelistHtml += (currentPage > 4) ? (pt.goTo.replace(/{#pageId#}/g, 1) + pt.hide) : "";
		for ( i = prePage; i <= frePage; i++) {
			pt.pagelistHtml += (i == currentPage) ? (pt.current.replace(/{#pageId#}/g, i)) : (pt.goTo.replace(/{#pageId#}/g, i));
		}
		pt.pagelistHtml += (currentPage <= pageCount - 4) ? (pt.hide + pt.goTo.replace(/{#pageId#}/g, pageCount)) : "";
	}
	if (pageCount <= 8) {
		for (var i = 1; i <= pageCount; i++) {
			pt.shortPageListHtml += (i == currentPage) ? (pt.current.replace(/{#pageId#}/g, i)) : (pt.goTo.replace(/{#pageId#}/g, i));
		}
	} else {
		var prePage = currentPage - 2;
		var frePage = currentPage + 2;
		prePage = (prePage <= 2) ? 1 : prePage;
		frePage = (frePage > pageCount - 2) ? pageCount : frePage;
		if (currentPage <= 4) {
			frePage = 6;
		}
		pt.shortPageListHtml += (currentPage > 4) ? (pt.goTo.replace(/{#pageId#}/g, 1) + pt.hide) : "";
		for ( i = prePage; i <= frePage; i++) {
			pt.shortPageListHtml += (i == currentPage) ? (pt.current.replace(/{#pageId#}/g, i)) : (pt.goTo.replace(/{#pageId#}/g, i));
		}
		pt.shortPageListHtml += (currentPage <= pageCount - 4) ? (pt.hide + pt.goTo.replace(/{#pageId#}/g, pageCount)) : "";
	}
	if (pageCount <= 6) {
		for (var i = 1; i <= pageCount; i++) {
			pt.noLastTmplHtml += (i == currentPage) ? (pt.current.replace(/{#pageId#}/g, i)) : (pt.goTo.replace(/{#pageId#}/g, i));
		}
	} else {
		var prePage = currentPage - 2;
		var frePage = currentPage + 1;
		prePage = (prePage <= 3) ? 1 : prePage;
		frePage = (frePage > pageCount - 1) ? pageCount : frePage;
		pt.noLastTmplHtml += (currentPage > 5) ? (pt.goTo.replace(/{#pageId#}/g, 1) + pt.goTo.replace(/{#pageId#}/g, 2) + pt.hide) : "";
		for ( i = prePage; i <= frePage; i++) {
			pt.noLastTmplHtml += (i == currentPage) ? (pt.current.replace(/{#pageId#}/g, i)) : (pt.goTo.replace(/{#pageId#}/g, i));
		}
		pt.noLastTmplHtml += (currentPage <= pageCount - 2) ? pt.hide : "";
	}
	if (option.more) {
		pt.pagelistHtml = "";
		for (var i = 1; i <= pageCount; i++) {
			pt.pagelistHtml += (i == currentPage) ? (pt.current.replace(/{#pageId#}/g, i)) : (pt.goTo.replace(/{#pageId#}/g, i));
		}
		pt.shortPageListHtml = pt.pagelistHtml;
	}
	template = templateList[option.type][2].replace(/{#currentPageId#}/g, currentPage).replace(/{#pageCountNum#}/g, pageCount).replace(/{#itemCountNum#}/g, itemCount).replace(/{#firstPage#}/g, pt.firstPageHtml).replace(/{#previousPage#}/g, pt.previousPageHtml).replace(/{#nextPage#}/g, pt.nextPageHtml).replace(/{#lastPage#}/g, pt.lastPageHtml).replace(/{#pageList#}/g, pt.pagelistHtml).replace(/{#shortPageList#}/g, pt.shortPageListHtml).replace(/{#morePage#}/g, pt.morePageHtml).replace(/{#miniPageList#}/g, pt.miniPageListHtml).replace(/{#noLastTmpl#}/g, pt.noLastTmplHtml).replace(/{#maxlength#}/g, pageCount.toString().length);
	var frameList = [];
	var inputList = [];
	var buttomList = [];
	var linkList = [];
	frameList = frameList.concat(getItemFromArray(option.domList));
	function getItemFromArray(arr) {
		var array = [];
		for (var k = 0; k < arr.length; k++) {
			if (arr[k].length > 0) {
				array = array.concat(getItemFromArray(arr[k]));
			} else {
				array.push(arr[k]);
			}
		}
		return array;
	}

	var k = frameList.length;
	for (var i = 0; i < frameList.length; i++) {
		try {
			frameList[i].innerHTML = template.replace(/{#debugtag#}/g, i);
			var temp = frameList[i].getElementsByTagName("input");
			for (var j = 0; j < temp.length; j++) {
				if (temp[j].getAttribute("pageTag") == "input") {
					inputList.push(temp[j]);
				}
			}
			var temp = frameList[i].getElementsByTagName("button");
			for (var j = 0; j < temp.length; j++) {
				if (temp[j].getAttribute("pageTag") == "jumper") {
					buttomList.push(temp[j]);
				}
			}
			var temp = frameList[i].getElementsByTagName("a");
			for (var j = 0; j < temp.length; j++) {
				if (temp[j].getAttribute("pageTag") == "go") {
					linkList.push(temp[j]);
				}
			}
		} catch(e) {
		}
	}
	for (var i = 0; i < inputList.length; i++) {
		inputList[i].onblur = function() {
			this.value = this.value.replace(/[^0-9]/g, '');
			if (this.value > pageCount || this.value < 1) {
				this.value = "";
			}
			for (var j = 0; j < inputList.length; j++) {
				inputList[j].value = this.value;
			}
		};
		inputList[i].onfocus = function() {
			this.select();
		};
		inputList[i].onkeydown = function(e) {
			var e = window.event || e;
			if (e.keyCode != 13) {
				return true;
			} else {
				this.onblur();
				buttomList[0].onclick();
				return false;
			}
		};
	}
	for (var i = 0; i < buttomList.length; i++) {
		buttomList[i].onclick = function() {
			var input = (this.parentElement||this.parentNode).getElementsByTagName("input")[0];
			var goPage = parseInt(input.value, 10);
			input.onblur();
			if (goPage < 1 || !goPage) {
				input.focus();
				return;
			} else {
				goTo(goPage, option);
			}
		};
	}
	for (var i = 0; i < linkList.length; i++) {
		if (option.action == "url") {
			linkList[i].href = option.url.replace("{#pageId#}", linkList[i].getAttribute("pageId"));
		} else {
			linkList[i].onclick = function() {
				goTo(this.getAttribute("pageId"), option);
			};
		}
	}
	goTo = function(pageId, opt) {
		if (opt.action == "url") {
			location.href = opt.url.replace("{#pageId#}", pageId);
		}
		if (opt.action == "func") {
			return opt.func(pageId, opt);
		}
		return false;
	};
	option.onInit();
}
