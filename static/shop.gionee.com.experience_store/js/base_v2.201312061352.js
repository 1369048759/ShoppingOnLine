function $addEvent(f, d, g) {
	if (!f || !d || !g) {
		return;
	}
	if (f instanceof Array) {
		for (var c = 0, a = f.length; c < a; c++) {
			$addEvent(f[c], d, g);
		}
		return;
	}
	if (d instanceof Array) {
		for (var c = 0, a = d.length; c < a; c++) {
			$addEvent(f, d[c], g);
		}
		return;
	}
	if (!$addEvent.createDelegate) {
		$addEvent.createDelegate = function(j, i) {
			return function() {
				return j.apply(i, arguments);
			};
		};
	}
	var e = $addEvent.createDelegate(g, f);
	var b = d.split("."),
		d = b[0],
		h = b.length > 1 ? b[1] : false;
	if (window.addEventListener) {
		f.addEventListener(d, e, false);
	} else {
		if (window.attachEvent) {
			f.attachEvent("on" + d, e);
		} else {
			alert("你的浏览器太out了");
		}
	}
	f.__eventHandle = f.__eventHandle || {};
	f.__eventHandle[d] = f.__eventHandle[d] || [];
	if (h) {
		f.__eventHandle[d].push({
			delegateHandle: e,
			handle: g,
			spaceId: h
		});
	} else {
		f.__eventHandle[d].push({
			delegateHandle: e,
			handle: g
		});
	}
	return e;
}

function $removeEvent(c, j, g, l) {
	if (arguments.length < 2) {
		return;
	}
	var e = j.split("."),
		j = e[0],
		k = e.length > 1 ? e[1] : false;
	if (!c.__eventHandle || !c.__eventHandle[j]) {
		return;
	}
	for (var d = 0, h = c.__eventHandle[j], f = h.length, a, b; d < f; d++) {
		a = false, b = h[d];
		if (!g || (g && (b.handle === g))) {
			if (!k || (k && (b.spaceId === k))) {
				if (!l || (l && l === b.delegateHandle)) {
					a = true;
				}
			}
		}
		if (a) {
			if (window.removeEventListener) {
				c.removeEventListener(j, b.delegateHandle, false);
			} else {
				c.detachEvent("on" + j, b.delegateHandle);
			}
			h.splice(d, 1);
			d--;
			f--;
			if (l) {
				break;
			}
		}
	}
}

function $DelayLoad(c, b) {
	var a = this;
	a._selfId = (++a.constructor._newNum);
	a._selfName = ".$DelayLoad" + a._selfId;
	if (c != b) {
		a.oContent = document.getElementById(c).getElementsByTagName("img");
	} else {
		a.oContent = document.images;
	}
}
$DelayLoad.prototype = {
	init: function() {
		var c = this;
		if (c.oContent.length == 0) {
			return false;
		}
		c.oLoadItems = new Array();
		var a = c.oContent.length;
		for (var b = 0; b < a; b++) {
			if (c.oContent[b].attributes.init_src) {
				c.oLoadItems.push($(c.oContent[b]));
			}
		}
		if (c.oLoadItems.length == 0) {
			return false;
		}
		$(window).bind("scroll" + c._selfName + " resize" + c._selfName, c, c.fnLoad);
		c.fnLoad();
	},
	fnLoad: function(l) {
		var a = (l && l.data) || this;
		var m = $(window),
			j = a.oLoadItems;
		var h = m.scrollTop(),
			f = m.height(),
			d = h + f;
		var k = j.length;
		for (var g = 0; g < k; g++) {
			if (j[g].attr("src") == j[g].attr("init_src")) {
				j.splice(g, 1);
				g--;
				k--;
				continue;
			}
			var c = parseInt(j[g].offset().top);
			var b = parseInt(c + (j[g].outerHeight() || a.height));
			if ((c >= h && c <= d) || (b >= h && b <= d || (c < h && b > d))) {
				j[g].attr("src", j[g].attr("init_src"));
				j.splice(g, 1);
				g--;
				k--;
			}
		}
		if (k == 0) {
			$(window).unbind("scroll" + a._selfName + " resize" + a._selfName);
		}
	}
};
$DelayLoad._newNum = 0;
$DelayLoad.prototype.constructor = $DelayLoad;

function $FocusBlur(a) {
	if (a == undefined) {
		return;
	}
	this.otxt = $id(a.otxt);
	this.config.cssFocus = a.config.cssFocus || this.config.cssFocus;
	this.config.defValue = a.config.defValue || this.config.defValue;
	this.callback = typeof callback == "function" ? callback : this.callback;
	this.init();
}
$FocusBlur.prototype = {
	config: {
		cssFocus: "focus",
		defValue: ""
	},
	callback: function() {},
	init: function() {
		var a = this,
			b = a.otxt;
		$(b).bind("focus", a, a.focusHandler);
		$(b).bind("blur", a, a.blurHandler);
		if (b.value.length == 0) {
			b.value = a.config.defValue;
			b.style.color = "#999999";
		} else {
			b.style.color = "#000000";
		}
	},
	focusHandler: function(d) {
		var c = d.data,
			b = false,
			a = c.config,
			f = c.otxt;
		$(f).addClass(a.cssFocus);
		f.style.color = "#000000";
		if (f.value == a.defValue) {
			b = true;
			f.value = "";
		}
		c.callback(true, b);
	},
	blurHandler: function(d) {
		var c = d.data,
			b = false,
			a = c.config,
			f = c.otxt;
		$(f).removeClass(a.cssFocus);
		if (f.value.length == 0) {
			b = true;
			f.value = a.defValue;
			f.style.color = "#999999";
		}
		c.callback(false, b);
	}
};
$FocusBlur.prototype.constructor = $FocusBlur;

function $FixedtoTop(b) {
	var a = this;
	a._selfID = ++a.constructor._newNum;
	a._selfName = ".$FixedtoTop" + a._selfID;
	if (!b || !b.obj) {
		return false;
	}
	a.config = $.extend({}, a.config, b.config);
	a.obj = $(b.obj);
	a.show();
}
$FixedtoTop.prototype = {
	config: {
		toTop: 0,
		start: 0,
		zIndex: 200
	},
	setPos: function(d) {
		var c = d.data,
			a = c.config,
			b = parseInt($(window).scrollTop());
		if (b < a.start) {
			c.obj.css({
				position: "relative",
				top: 0,
				"z-index": 0
			});
		} else {
			c.obj.css({
				position: "fixed",
				top: a.toTop,
				"z-index": a.zIndex
			});
		}
	},
	setPosIe6: function(d) {
		var c = d.data,
			a = c.config,
			b = parseInt($(window).scrollTop());
		if (b < a.start) {
			c.obj.css({
				position: "relative",
				top: 0,
				"z-index": 0
			});
		} else {
			c.obj.css({
				position: "absolute",
				top: b,
				"z-index": a.zIndex
			});
		}
	},
	hide: function(b) {
		var a = b.data;
		a.obj.slideUp(200);
		if ($.browser.msie && Number($.browser.version) <= 6) {
			$(window).unbind("scroll " + a._selfName);
		}
	},
	toNormal: function(b) {
		var a = b.data;
		a.obj.css({
			position: "relative",
			top: 0,
			"z-index": 1
		});
		alert(a.obj.css("z-index"));
		$(window).unbind("scroll " + a._selfName);
	},
	show: function(d) {
		var c = (d && d.data) || this,
			a = c.config;
		if (a.start == 0) {
			c.obj.css({
				position: "fixed",
				top: a.toTop,
				"z-index": a.zIndex
			});
			if ($.browser.msie && Number($.browser.version) <= 6) {
				var b = $(window);
				c.setPos = c.setPosIe6;
				b.bind("scroll " + c._selfName, c, c.setPos);
			}
		} else {
			var b = $(window);
			if ($.browser.msie && Number($.browser.version) <= 6) {
				c.setPos = c.setPosIe6;
			}
			b.bind("scroll " + c._selfName, c, c.setPos);
		}
		c.obj.slideDown(200);
	}
};
$FixedtoTop.prototype.constructor = $FixedtoTop;
$FixedtoTop._newNum = 0;

function $FixedFloatRight(b) {
	var a = this;
	a._selfID = ++a.constructor._newNum;
	a._selfName = ".$FixedFloatRight" + a._selfID;
	if (!b || !b.obj) {
		return false;
	}
	a.config = $.extend({}, a.config, b.config);
	a.obj = $(b.obj);
}
$FixedFloatRight.prototype = {
	config: {
		toRight: 10,
		toBottom: 10,
		toStart: 0,
		toEnd: 0
	},
	init: function() {
		var b = this,
			a = b.config;
		a.objH = a.objH || b.obj.outerHeight();
		if ($.browser.msie && Number($.browser.version) <= 6) {
			b.setPos = b.setPosIe6;
		}
		$(window).bind("scroll" + b._selfName + " resize" + b._selfName, b, b.setPos);
		b.setPos();
	},
	setPos: function(g) {
		var d = (g && g.data) || this,
			a = d.config;
		var c = $(window),
			b = c.scrollTop(),
			f = c.height();
		if (b + f - d.obj.outerHeight() - a.toBottom < a.toStart) {
			d.obj.css({
				position: "absolute",
				top: a.toStart
			});
		} else {
			if (b + f >= a.toEnd) {
				d.obj.css({
					position: "absolute",
					top: a.toEnd - d.obj.outerHeight() - a.toBottom
				});
			} else {
				d.obj.css({
					position: "fixed",
					top: f - d.obj.outerHeight() - a.toBottom
				});
			}
		}
	},
	setPosIe6: function(g) {
		var d = (g && g.data) || this,
			a = d.config;
		var c = $(window),
			b = c.scrollTop(),
			f = c.height();
		if (b + f - d.obj.outerHeight() - a.toBottom < a.toStart) {
			d.obj.css({
				position: "absolute",
				top: a.toStart
			});
		} else {
			if (b + f >= a.toEnd) {
				d.obj.css({
					position: "absolute",
					top: a.toEnd - d.obj.outerHeight() - a.toBottom
				});
			} else {
				d.obj.css({
					position: "absolute",
					top: b + f - d.obj.outerHeight() - a.toBottom
				});
			}
		}
	}
};
$FixedFloatRight.prototype.constructor = $FixedFloatRight;
$FixedFloatRight._newNum = 0;

function $Hover(b) {
	var a = this;
	if (b.obj == undefined) {
		return;
	} else {
		a.obj = $(b.obj);
		a.oPanel = a.obj.find(b.selectorPanel);
	}
	if (b.cssHover) {
		a.cssHover = b.cssHover;
	}
	a.config = $.extend({}, a.config, b.config);
	a.obj.bind("mouseenter", a, a.mouseenterHandler);
	a.obj.bind("mouseleave", a, a.mouseleaveHandler);
}
$Hover.prototype = {
	cssHover: "curr",
	config: {
		onBefore: null
	},
	mouseenterHandler: function(b) {
		var a = b.data;
		clearTimeout(a._timeout);
		if (!a.obj.hasClass(a.cssHover)) {
			a._timeout = setTimeout(function() {
				if (a.config.onBefore != null) {
					a.config.onBefore();
				}
				a.oPanel.stop(false, true);
				a.obj.addClass(a.cssHover);
				a.oPanel.slideDown(200);
			}, 200);
		}
	},
	mouseleaveHandler: function(b) {
		var a = b.data;
		clearTimeout(a._timeout);
		if (a.obj.hasClass(a.cssHover)) {
			a._timeout = setTimeout(function() {
				a.oPanel.stop(false, true);
				a.oPanel.slideUp(200, function() {
					a.obj.removeClass(a.cssHover);
				});
			}, 300);
		}
	}
};
$Hover.prototype.constructor = $Hover;

function $Quantity(c) {
	var b = this;
	if (!c || !c.obj) {
		return;
	}
	b.config = $.extend({}, b.config, c.config);
	var a = b.config;
	b.obj = $(c.obj);
	b.oTxt = b.obj.find(a.selectorTxt);
	b.oAdd = b.obj.find(a.selectorAdd);
	b.oRedu = b.obj.find(a.selectorRedu);
	b.oAdd.bind("click", b, b.addHandler);
	b.oRedu.bind("click", b, b.reduHandler);
	b.oTxt.bind("keypress", b, b.keypressHandler);
	b.oTxt.bind("blur", b, b.blurHandler);
	b.init();
}
$Quantity.prototype = {
	config: {
		selectorTxt: ".ui_quantity_num",
		selectorAdd: ".ui_quantity_add",
		selectorRedu: ".ui_quantity_redu",
		cssAddDis: "ui_quantity_add_dis",
		cssReduDis: "ui_quantity_redu_dis",
		minValue: 1,
		maxValue: 1000,
		colnum: 1,
		onAfter: null
	},
	init: function() {
		this.setStatus(this.oTxt.val());
	},
	addHandler: function(h) {
		var g = h.data,
			b = g.config,
			c = b.minValue,
			a = b.maxValue,
			d = b.colnum,
			f = parseInt(g.oTxt.val());
		if ($(this).hasClass(b.cssAddDis)) {
			h.stopPropagation();
			return false;
		}
		if (isNaN(f) || f < c) {
			f = c;
		} else {
			if (f >= a) {
				f = a;
			} else {
				f = f + d;
			}
		}
		g.oTxt.val(f);
		g.setStatus(f);
		if (g.config.onAfter != null) {
			g.onAfter = g.config.onAfter;
			g.onAfter();
		}
		h.stopPropagation();
	},
	blurHandler: function(d) {
		var c = d.data,
			a = c.config;
		var b = parseInt(c.oTxt.val());
		if (isNaN(b) || b < a.minValue) {
			b = a.minValue;
		} else {
			if (b > a.maxValue) {
				b = a.maxValue;
			}
		}
		c.oTxt.val(b);
		c.setStatus(b);
		if (c.config.onAfter != null) {
			c.onAfter = c.config.onAfter;
			c.onAfter();
		}
	},
	keypressHandler: function(b) {
		if (b.keyCode < 48 || b.keyCode > 57) {
			b.preventDefault();
			var a = b.data;
			a.oTxt.val(a.config.minValue);
		}
	},
	reduHandler: function(h) {
		var g = h.data,
			b = g.config,
			c = b.minValue,
			a = b.maxValue,
			d = b.colnum,
			f = parseInt(g.oTxt.val());
		if ($(this).hasClass(b.cssReduDis)) {
			h.stopPropagation();
			return false;
		}
		if (isNaN(f) || f - d < c || f > a) {
			f = c;
		} else {
			f = f - d;
		}
		g.oTxt.val(f);
		g.setStatus(f);
		if (g.config.onAfter != null) {
			g.onAfter = g.config.onAfter;
			g.onAfter();
		}
		h.stopPropagation();
	},
	setStatus: function(b) {
		var c = this,
			a = c.config,
			d = b;
		if (d <= a.minValue) {
			c.oRedu.addClass(a.cssReduDis);
		} else {
			c.oRedu.removeClass(a.cssReduDis);
		}
		if (d >= a.maxValue) {
			c.oAdd.addClass(a.cssAddDis);
		} else {
			c.oAdd.removeClass(a.cssAddDis);
		}
	}
};
$Quantity.prototype.constructor = $Quantity;

function $Slide(c, b) {
	var a = this,
		b;
	a.timeout = null;
	a._selfID = (++a.constructor._newNum);
	a._selfName = ".$Slide" + a._selfID;
	if (!c) {
		return;
	}
	if (c.config != b) {
		a.config = $.extend({}, a.config, c.config);
	}
	if (c.oslide != b) {
		a.oslide = $(c.oslide);
		a.oPanel = a.oslide.find(a.config.panelSelector);
		a.oItems = a.oPanel.find(a.config.itemsSelector);
		a.oOptionsCon = a.oslide.find(a.config.optionsSelector);
		a.oOptions = a.oOptionsCon.find(a.config.optionSelector);
	}
}
$Slide.prototype = {
	config: {
		pos: 0,
		isRandom: false,
		speed: 400,
		delay: 4000,
		auto: false,
		moveWay: "moveWidth",
		itemsSelector: ".ui_slide_item",
		panelSelector: ".ui_slide_panel",
		optionSelector: ".ui_slide_option",
		optionsSelector: ".ui_slide_options",
		optionCSSCurr: "ui_slide_option_curr",
		itemCSSCurr: "ui_slide_item_curr",
		itemWidth: 0,
		itemHeight: 0,
		onBeforeMove: null,
		isDelay: false
	},
	autoPlay: function() {
		var a = this;
		clearTimeout(a.timeout);
		a.config.pos++;
		a.move();
		a.timeout = setTimeout(function() {
			a.autoPlay();
			return a.timeout;
		}, a.config.delay);
	},
	setPos: function() {
		var a = this;
		a.config.pos >= a.sum ? a.config.pos = a.config.pos - a.sum : a.config.pos = a.config.pos;
	},
	itemsHandler: function(b) {
		var a = b.data;
		clearTimeout(a.timeout);
	},
	optionsEnterHandler: function(d) {
		var b = d.data,
			a = b.config,
			c = $(this);
		b.delayTimeout = setTimeout(function() {
			clearTimeout(b.timeout);
			var e = b.oOptions.index(c);
			a.pos = e;
			b.move();
		}, 200);
	},
	leaveHandler: function(b) {
		var a = b.data;
		clearTimeout(a.delayTimeout);
		if (a.config.auto) {
			clearTimeout(a.timeout);
			a.timeout = setTimeout(function() {
				a.autoPlay();
				return a.timeout;
			}, a.config.delay);
		}
	},
	init: function() {
		var c = this,
			a = c.config;
		var b = c.oOptions.length;
		c.sum = b;
		if (b == 0) {
			c.oslide.hide();
			return false;
		}
		if (b == 1) {
			c.oOptions.hide();
			c.oItems.addClass(a.itemCSSCurr);
			if (c.config.isDelay) {
				a.pos = 0;
				$(window).bind("resize" + c._selfName + " scroll" + c._selfName, c, c.fnDelay);
				c.fnDelay();
			}
			return false;
		}
		if (a.isRandom) {
			a.pos = Math.floor(c.sum * Math.random());
		}
		c.setMoveWay();
		if (c.config.isDelay) {
			c.config.onBeforeMove = c.fnDelay;
			$(window).bind("resize" + c._selfName + " scroll" + c._selfName, c, c.fnDelay);
			c.fnDelay();
		}
		c.oItems.mouseenter(c, c.itemsHandler);
		c.oOptions.mouseenter(c, c.optionsEnterHandler);
		c.oOptions.mouseleave(c, c.leaveHandler);
		if (a.auto) {
			c.oItems.mouseleave(c, c.leaveHandler);
			c.timeout = setTimeout(function() {
				c.autoPlay();
				return c.timeout;
			}, a.delay);
		}
	},
	move: function() {
		if (this.config.onBeforeMove) {
			this.onBeforeMove = this.config.onBeforeMove;
			this.onBeforeMove();
		}
		this.movefunc();
	},
	setMoveWay: function() {
		var b = this,
			a = b.config;
		b.oInitMoveWay[a.moveWay](b);
		b.movefunc = b.oMoveWays[a.moveWay];
	},
	setStatus: function() {
		var b = this,
			a = b.config;
		b.oItems.removeClass(a.itemCSSCurr);
		b.oItems.eq(a.pos).addClass(a.itemCSSCurr);
		b.oOptions.removeClass(a.optionCSSCurr);
		b.oOptions.eq(a.pos).addClass(a.optionCSSCurr);
	},
	oInitMoveWay: {
		moveWidth: function(c) {
			var b = c,
				a = b.config;
			b.itemValue = b.config.itemWidth || b.oItems.eq(0).outerWidth(true);
			b.oPanel.css({
				width: b.itemValue * b.sum
			});
			b.setPos();
			b.oPanel.css({
				left: -a.pos * b.itemValue
			});
			b.setStatus();
		},
		moveHeight: function(c) {
			var b = c,
				a = b.config;
			b.itemValue = b.config.itemHeight || b.oItems.eq(0).outerHeight(true);
			b.oPanel.css({
				height: b.itemValue * b.sum
			});
			b.setPos();
			b.oPanel.css({
				top: -a.pos * b.itemValue
			});
			b.setStatus();
		},
		moveNone: function(c) {
			var b = c,
				a = b.config;
			b.setPos();
			b.oItems.hide();
			b.oItems.eq(a.pos).show();
			b.setStatus();
		},
		moveOpacity: function(c) {
			var b = c,
				a = b.config;
			b.setPos();
			b.oItems.hide();
			b.oItems.eq(a.pos).show();
			b.setStatus();
		},
		moveHeightC: function(b) {
			var a = b;
			a.oItemsFirst = a.oItems.eq(0);
			a.oItemsFirst.css("position", "relative");
			a.itemValue = a.config.itemWidth || a.oItemsFirst.outerWidth(true);
			a.oPanel.css({
				width: a.itemValue * (a.sum + 1)
			});
			a.setPos();
			a.oPanel.css({
				left: -cfg.pos * a.itemValue
			});
			a.setStatus();
		}
	},
	oMoveWays: {
		moveWidth: function() {
			var b = this,
				a = b.config;
			b.oPanel.stop(false, true);
			b.setPos();
			b.setStatus();
			b.oPanel.animate({
				left: -a.pos * b.itemValue
			}, a.speed);
		},
		moveHeight: function() {
			var b = this,
				a = b.config;
			b.oPanel.stop(false, true);
			b.setPos();
			b.oPanel.animate({
				top: -a.pos * b.itemValue
			}, a.speed);
			b.setStatus();
		},
		moveNone: function() {
			var b = this,
				a = b.config;
			b.setPos();
			b.setStatus();
			b.oItems.hide();
			b.oItems.eq(a.pos).show();
		},
		moveOpacity: function() {
			var b = this,
				a = b.config;
			b.setPos();
			b.oItems.hide();
			b.oItems.eq(a.pos).fadeIn();
			b.setStatus();
		},
		moveHeightC: function() {
			var b = this,
				a = b.config;
			b.oPanel.stop(false, true);
			if (a.pos > b.sum - 1) {
				b.oItemsFirst.css({
					left: b.itemValue * b.sum
				});
				b.oPanel.animate({
					left: -a.pos * b.itemValue
				}, a.speed, function() {
					b.oPanel.css("left", 0);
					b.oItemsFirst.css("left", 0);
				});
				a.pos = a.pos - b.sum;
				b.setStatus();
			} else {
				if (b.pos < 0) {
					a.pos = a.pos + b.sum;
					b.setStatus();
					b.oPanel.css("left", -b.itemValue * b.sum);
					b.oItemsFirst.css({
						left: b.itemValue * b.sum
					});
					b.oPanel.animate({
						left: -(a.pos * b.itemValue)
					}, a.speed, function() {
						b.oItemsFirst.css("left", 0);
					});
				} else {
					b.setStatus();
					b.oPanel.animate({
						left: -a.pos * b.itemValue
					}, a.speed);
				}
			}
		}
	},
	fnDelay: function(g) {
		var a = (g && g.data) || this,
			j;
		if (!a.oDelayImgs) {
			j = a.oslide.find("img");
			a.oDelayImgs = new Array();
			j.each(function() {
				if ($(this).attr("orial_src")) {
					a.oDelayImgs.push(this);
				}
			});
		}
		var i = a.config.pos;
		if (i > a.oItems.length - 1) {
			i = i - a.oItems.length;
		}
		j = a.oItems.eq(i).find("img");
		var h = $(window);
		var d = h.scrollTop(),
			c = h.height(),
			b = d + c;
		var f = j.length;
		j.each(function() {
			var l = $(this);
			var e = parseInt(l.offset().top);
			var m = parseInt(e + (l.outerHeight() || 800));
			if ((e >= d && e <= b) || (m >= d && m <= b)) {
				l.attr("src", l.attr("orial_src"));
				for (var k = 0; k < a.oDelayImgs.length; k++) {
					if (a.oDelayImgs[k] == this) {
						a.oDelayImgs.splice(k, 1);
						k--;
						break;
					}
				}
			}
		});
		if (a.oDelayImgs.length == 0) {
			a.config.onBeforeMove = null;
			$(window).unbind("resize" + a._selfName + " scroll" + a._selfName);
		}
	}
};
$Slide.prototype.constructor = $Slide;
$Slide._newNum = 0;
$Slide.play = function(b) {
	var a = new $Slide(b);
	a.init();
	return a;
};

function $Tab(c, b) {
	var a = this;
	a._selfID = (++a.constructor._newNum);
	a._selfName = ".$Tab" + a._selfID;
	if (!c) {
		return;
	}
	if (c.config != b) {
		a.config = $.extend({}, a.config, c.config);
	}
	if (c.oTab != b) {
		a.oTab = $(c.oTab);
		a.oPanel = a.oTab.find(a.config.selectorPanel);
		a.oItems = a.oPanel.find(a.config.selectorItem);
		a.oOptionsCon = a.oTab.find(a.config.selectorOptions);
		a.oOptions = a.oOptionsCon.find(a.config.selectorOption);
	}
}
$Tab.prototype = {
	config: {
		pos: 0,
		isRandom: false,
		selectorItem: ".ui_tab_item",
		selectorPanel: ".ui_tab_panel",
		selectorOption: ".ui_tab_option",
		selectorOptions: ".ui_tab_options",
		cssOptionCurr: "ui_tab_option_curr",
		onBeforeMove: null,
		onAfterMove: null,
		isDelay: false
	},
	init: function() {
		var c = this,
			a = c.config;
		var b = c.oOptions.length;
		c.sum = b;
		if (b == 0) {
			c.oTab.hide();
			return false;
		}
		if (b == 1) {
			a.pos = 0;
		} else {
			if (a.isRandom) {
				a.pos = Math.floor(b * Math.random());
			}
			c.oOptions.mouseenter(c, c.optionsEnterHandler);
			c.oOptions.mouseleave(c, c.optionsLeaveHandler);
		}
		if (a.isDelay) {
			$(window).bind("resize" + c._selfName + " scroll" + c._selfName, c, c.fnDelay);
		}
		c.move();
	},
	move: function() {
		if (this.config.onBeforeMove) {
			this.onBeforeMove = this.config.onBeforeMove;
			this.onBeforeMove();
		}
		if (this.config.isDelay) {
			this.fnDelay();
		}
		this.movefunc();
		if (this.config.onAfterMove) {
			this.onAfterMove = this.config.onAfterMove;
			this.onAfterMove();
		}
	},
	movefunc: function() {
		var b = this,
			a = b.config;
		b.oItems.hide();
		b.oItems.eq(a.pos).show();
		b.oOptions.removeClass(a.cssOptionCurr);
		b.oOptions.eq(a.pos).addClass(a.cssOptionCurr);
	},
	optionsEnterHandler: function(d) {
		var b = d.data,
			a = b.config,
			c = $(this);
		b._delayTimeout = setTimeout(function() {
			clearTimeout(b._delayTimeout);
			var e = b.oOptions.index(c);
			a.pos = e;
			b.move();
		}, 200);
	},
	optionsLeaveHandler: function(a) {
		clearTimeout(a.data._delayTimeout);
	},
	fnDelay: function(g) {
		var a = (g && g.data) || this,
			j;
		if (!a.oDelayImgs) {
			j = a.oTab.find("img");
			a.oDelayImgs = new Array();
			j.each(function() {
				if ($(this).attr("orial_src")) {
					a.oDelayImgs.push(this);
				}
			});
		}
		var i = a.config.pos;
		j = a.oItems.eq(i).find("img");
		var h = $(window);
		var d = h.scrollTop(),
			c = h.height(),
			b = d + c;
		var f = j.length;
		j.each(function() {
			var l = $(this);
			if (!l.attr("orial_src")) {
				return;
			}
			var e = parseInt(l.offset().top);
			var m = parseInt(e + (l.outerHeight() || 800));
			if ((e >= d && e <= b) || (m >= d && m <= b) || (e < d && m > b)) {
				l.attr("src", l.attr("orial_src"));
				for (var k = 0; k < a.oDelayImgs.length; k++) {
					if (a.oDelayImgs[k] == this) {
						a.oDelayImgs.splice(k, 1);
						k--;
						break;
					}
				}
			}
		});
		if (a.oDelayImgs.length == 0) {
			a.config.isDelay = false;
			$(window).unbind("resize" + a._selfName + " scroll" + a._selfName);
		}
	}
};
$Tab.prototype.constructor = $Tab;
$Tab.play = function(b) {
	var a = new $Tab(b);
	a.init();
	return a;
};

function $trim(a) {
	return a.replace(/^\s+|\s$/g, "");
}

function $MinWin(d) {
	var b = this;
	b._selfId = ++b.constructor._newNum;
	b._spaceName = ".$Minwin" + b._selfId;
	if (!d) {
		return false;
	}
	if (d.obj) {
		b.obj = $(d.obj);
	}
	if (d.objWin) {
		b.objWin = b.obj.find(d.objWin);
	} else {
		b.objWin = b.obj.children();
	}
	if (d.oclose) {
		b.oclose = b.obj.find(d.oclose);
	} else {
		b.oclose = b.obj.find(".ui_minWin_close");
	}
	if (d.closeTime) {
		b.closeTime = parseInt(d.closeTime);
	}
	if ($isBrowser("ie6")) {
		var a = document.createElement("iframe");
		$extend(a.style, {
			position: "absolute",
			left: "0px",
			top: "0px",
			width: "100%",
			zIndex: -1,
			border: "none",
			backgroundColor: "#000000"
		});
		a.setAttribute("allowtransparency", "yes");
		try {
			a.document.body.style.backgroundColor = "#000000";
		} catch (c) {}
		b.coverIframe = b.obj.get(0).appendChild(a);
		b.coverIframe.style.position = "absolute";
		b.coverIframe.style.zIndex = "1";
		b.objWin.get(0).style.zIndex = "2";
	}
}
$MinWin.prototype.closeTime = 0;
$MinWin.prototype.show = function() {
	var b = this;
	b.obj.show();
	var c = parseInt(b.objWin.outerHeight());
	if ($.browser.msie && Number($.browser.version) <= 6) {
		b.obj.css({
			height: $(document).height()
		});
		b.coverIframe.height = $(document).height();
		b.posIE6();
		var a = $(window);
		a.bind("scroll" + b._spaceName, {
			ominwin: b
		}, function(d) {
			var e = d.data.ominwin;
			e.posIE6();
		});
		a.bind("resize" + b._spaceName, {
			ominwin: b
		}, function(d) {
			var e = d.data.ominwin;
			e.posIE6();
		});
	} else {
		b.objWin.css({
			marginTop: -parseInt(c / 2)
		});
	}
	b.oclose.bind("click" + b._spaceName, {
		ominwin: b
	}, function(d) {
		var e = d.data.ominwin;
		e.hide();
	});
	if (b.closeTime) {
		setTimeout(function() {
			b.hide();
		}, b.closeTime);
	}
};
$MinWin.prototype.hide = function() {
	var b = this;
	b.obj.hide();
	b.oclose.unbind("click" + b._spaceName);
	if ($.browser.msie && Number($.browser.version) <= 6) {
		var a = $(window);
		a.unbind("scroll" + b._spaceName);
		a.unbind("resize" + b._spaceName);
	}
};
$MinWin.prototype.posIE6 = function() {
	var b = this;
	var e = parseInt(b.objWin.outerHeight());
	var a = $(window);
	var d = parseInt(a.height());
	var c = parseInt(a.scrollTop());
	b.objWin.css({
		top: c + parseInt((d - e) / 2)
	});
};
$MinWin._newNum = 0;
(function(a) {
	var b = new Object();
	b.name = a.appName;
	if (b.name.indexOf("Microsoft") != -1) {
		b.version = a.appVersion.indexOf("MSIE");
		b.version = parseInt(a.appVersion.substring(b.version + 4));
		if (b.version <= 6) {
			document.execCommand("BackgroundImageCache", false, true);
		}
	}
})(window.navigator);

function $setCookie(b, d, a, f, c, e) {
	var g = new Date(),
		a = arguments[2] || null,
		f = arguments[3] || "/",
		c = arguments[4] || null,
		e = arguments[5] || false;
	a ? g.setMinutes(g.getMinutes() + parseInt(a)) : "";
	document.cookie = b + "=" + escape(d) + (a ? ";expires=" + g.toGMTString() : "") + (f ? ";path=" + f : "") + (c ? ";domain=" + c : "") + (e ? ";secure" : "");
}

function $getCookie(a) {
	var b = new RegExp("(^| |(?=;))" + a + "(?:=([^;]*))?(;|$)"),
		c = document.cookie.match(b);
	return c ? (c[2] ? unescape(c[2]) : "") : null;
}

function $delCookie(a, e, c, d) {
	var b = $getCookie(a);
	if (b != null) {
		var f = new Date();
		f.setMinutes(f.getMinutes() - 1000);
		e = e || "/";
		document.cookie = a + "=;expires=" + f.toGMTString() + (e ? ";path=" + e : "") + (c ? ";domain=" + c : "") + (d ? ";secure" : "");
	}
}
var $getLoginInfo = (function() {
	var a, d = [],
		c = 0;

	function b() {
		var l = "gn_is_login",
			g;
		var k = $getCookie(l);
		if (k === null || k.length == 0) {
			g = {
				status: 0
			};
			var f = d.length;
			for (var h = 0; h < f; h++) {
				try {
					d[h](g);
				} catch (j) {}
			}
			d.length = 0;
		} else {
			$.ajax({
				url: "/user.php?act=get_login_user",
				type: "get",
				dataType: "json",
				success: function(n) {
					g = {};
					g.status = n.status;
					if (g.status == 0) {
						var o = new Date();
						o.setMinutes(o.getMinutes() - 1000);
						document.cookie = l + "=;expires=" + o.toGMTString() + ";path=/;domain=.gionee.com;";
					} else {
						g.info = n.user_infor;
					}
					var e = d.length;
					if (e > 0) {
						for (var m = 0; m < e; m++) {
							d[m](g);
						}
						d.length = 0;
					}
				}
			});
		}
		c = 0;
	}
	return function(e) {
		if (a) {
			e(a);
		} else {
			if (c == 0) {
				c = 1;
				d.push(e);
				b();
			} else {
				d.push(e);
			}
		}
	};
})();
var $getCartInfo = (function() {
	return function(a) {
		$.ajax({
			url: "/flow.php?step=get_cart_goods",
			type: "POST",
			context: document.body,
			dataType: "json",
			success: function(b) {
				try {
					a(b);
				} catch (c) {}
			}
		});
	};
})();
var $addCartPro = (function() {
	return function(c, f) {
		var b = c.spec.length,
			e = "";
		for (var d = 0; d < b; d++) {
			e += ',"' + c.spec[d] + '"';
		}
		if (b > 0) {
			e = '"' + e.substr(2);
		}
		e = '{"quick":' + c.quick + ',"spec":[' + e + '],"goods_id":' + c.goods_id + ',"number":' + c.number + ',"parent":' + c.parent + "}";
		var a = {};
		a.goods = e;
		a[hex_md5($getCookie("gn_token_id") || "")] = 1;
		$.ajax({
			url: "/flow.php?step=add_to_cart",
			type: "POST",
			context: document.body,
			dataType: "json",
			data: a,
			success: function(g) {
				f(g);
			}
		});
	};
})();
var $addModAddress = (function() {
	return function(a, b) {
		b = typeof b == "function" ? b : function() {};
		$.ajax({
			url: "/flow.php?step=consignee",
			type: "GET",
			context: document.body,
			dataType: "json",
			data: a,
			success: function(c) {
				b(c);
			}
		});
	};
})();

function $id(a) {
	return typeof(a) == "string" ? document.getElementById(a) : a;
}
$getTpl = (function() {
	var a = /(.*?)\/\*(.*?)\*\/(.*)\1/i,
		c = /<!--(.*?)\/\*(.*?)\*\/(.*?)\1-->/gi;

	function b(k, j) {
		k = k.replace(/[\n\r]/g, "");
		var e = k.match(c);
		var d = {};
		if (!e) {
			return [];
		}
		for (var g = 0; g < e.length; g++) {
			var h = e[g];
			var f = (" " + h).substring(1).match(a);
			d[f[1]] = f[3].replace(/^\s*/, "").replace(/\d*$/, "");
		}
		return d;
	}
	return function(f) {
		var d = $id("tpl_" + f);
		var e = b(d ? d.innerHTML : "", true);
		return e;
	};
})();
$formatTpl = (function() {
	return function(a, c) {
		var b = new Function("obj", "var p=[],print=function(){p.push.apply(p,arguments);};with(obj){p.push('" + a.replace(/[\r\t\n]/g, " ").split("<%").join("\t").replace(/((^|%>)[^\t]*)'/g, "$1\r").replace(/\t=(.*?)%>/g, "',$1,'").split("\t").join("');").split("%>").join("p.push('").split("\r").join("\\'") + "');}return p.join('');");
		return c ? b(c) : b;
	};
})();
$getRegion = (function() {
	return function(b, a, c) {
		$.ajax({
			url: "/region.php?type=" + b + "&parent=" + a,
			type: "GET",
			context: document.body,
			dataType: "json",
			success: function(d) {
				c(d);
			}
		});
	};
})();
$editAddAddress = (function() {
	return function(a, b) {
		$.ajax({
			url: "/flow.php?step=consignee",
			type: "POST",
			context: document.body,
			dataType: "json",
			data: a,
			success: function(c) {
				b(c);
			}
		});
	};
})();
$delAddress = (function() {
	return function(a, b) {
		$.ajax({
			url: "/flow.php?step=drop_consignee",
			type: "GET",
			context: document.body,
			dataType: "json",
			data: {
				id: a
			},
			success: function(c) {
				b(c);
			}
		});
	};
})();

function $round(b, h) {
	var d = 1,
		g = h;
	for (; h > 0; d *= 10, h--) {}
	for (; h < 0; d /= 10, h++) {}
	var a = (Math.round(b * d) / d).toString();
	var f = a.match(/^\d+\.(\d*)$/);
	var j = 0;
	if (f == null) {
		a += ".";
		j = g;
	} else {
		j = g - f[1].length;
	}
	for (var c = 0; c < j; c++) {
		a += "0";
	}
	return a;
}

function $namespace(name) {
	for (var arr = name.split(","), r = 0, len = arr.length; r < len; r++) {
		for (var i = 0, k, name = arr[r].split("."), parent = {}; k = name[i]; i++) {
			i === 0 ? eval("(typeof " + k + ')==="undefined"?(' + k + '={}):"";parent=' + k) : (parent = parent[k] = parent[k] || {});
		}
	}
}
var $float = (function() {
	if (typeof $float != "undefined") {
		return $float;
	}
	var a = {},
		b = 0;
	return window.$float = function(d) {
		var k = {
			left: 0,
			top: 0,
			width: 400,
			height: 0,
			title: "",
			html: "",
			autoResize: false,
			cover: true,
			dragble: false,
			fix: false,
			showClose: true,
			cName: "module_box_normal",
			style: "stand",
			contentStyle: "",
			cssUrl: "https://shop.gionee.com/static/css/float.css",
			onInit: null,
			onClose: null
		};
		for (var h in d) {
			k[h] = d[h];
		}
		k.id = b++;
		$loadCss(k.cssUrl);
		k.setAutoResize = c;
		k.close = n;
		k.destruct = f;
		k.closeOther = g;
		k.keepFix = j;
		k.resize = e;
		k.show = m;
		k.setPos = o;
		a[k.id] = k;
		k.closeOther();
		k.show();
		k.setAutoResize();
		if (k.dragble) {
			$initDragItem({
				barDom: k.boxTitleHandle,
				targetDom: k.boxHandle
			});
		}
		return k;

		function n() {
			this.destruct();
			this.onClose && this.onClose(this);
		}

		function f() {
			if (this.cover) {
				$mask.remove();
			}
			if (this.sizeTimer) {
				clearInterval(this.sizeTimer);
			}
			if (this.fixTimer) {
				clearInterval(this.fixTimer);
			}
			this.boxHandle && document.body.removeChild(this.boxHandle);
			this.boxHandle = null;
			a[this.id] = undefined;
			delete a[this.id];
		}

		function m() {
			var s = document.createElement("div"),
				p = "",
				r = this.id;
			s.id = "float_box_" + r;
			s.style.position = "absolute";
			if ($isBrowser("ie6")) {
				p = '<iframe frameBorder="0" style="position:absolute;left:0;top:0;z-index:-1;border:none;" id="float_iframe_' + r + '"></iframe>';
			}
			s.className = k.cName;
			var q = {
				content: p,
				id: r,
				style: this.contentStyle ? ('style="' + this.contentStyle + '"') : "",
				html: this.html,
				title: this.title,
				showClose: this.showClose ? "" : "none"
			};
			switch (this.style) {
				case "stand":
					s.innerHTML = $formatStr('{#content#}<div class="box_title" id="float_title_{#id#}"><a href="javascript:;" style="display:{#showClose#};"  class="bt_close" id="float_closer_{#id#}">×</a><h4>{#title#}</h4></div><div class="box_content" {#style#}>{#html#}</div>', q);
					break;
				default:
					s.innerHTML = $formatStr('{#content#}<div class="box_content" {#style#} id="float_title_{#id#}">{#html#}</div>', q);
					break;
			}
			document.body.appendChild(s);
			s = null;
			this.boxHandle = $id("float_box_" + r);
			this.boxTitleHandle = $id("float_title_" + r);
			this.boxCloseHandle = $id("float_closer_" + r);
			if ($isBrowser("ie6")) {
				this.boxIframeHandle = $id("float_iframe_" + r);
			}
			this.boxHandle.style.zIndex = l(r);
			this.height && (this.boxHandle.style.height = (k.height == "auto" ? k.height : k.height + "px"));
			this.width && (this.boxHandle.style.width = (k.width == "auto" ? k.width : k.width + "px"));
			this.sw = parseInt(this.boxHandle.offsetWidth);
			this.sh = parseInt(this.boxHandle.offsetHeight);
			this.setPos();
			if (this.cover) {
				$mask.add();
			}
			var i = this;
			this.boxCloseHandle && (this.boxCloseHandle.onclick = function() {
				i.close();
				return false;
			});
			this.onInit && this.onInit(k);
		}

		function o(v, u) {
			var q = $getPageScrollWidth(),
				r = $getPageScrollHeight(),
				t = $getWindowWidth(),
				i = $getWindowHeight();
			var s = [0, 0];
			v && (this.left = v);
			u && (this.top = u);
			s[0] = parseInt(this.left ? this.left : (q + (t - this.sw) / 2));
			s[1] = parseInt(this.top ? this.top : (r + (i - this.sh) / 2));
			((s[0] + this.sw) > (q + t)) && (s[0] = q + t - this.sw - 10);
			((s[1] + this.sh) > (r + i)) && (s[1] = r + i - this.sh - 10);
			(s[1] < r) && (s[1] = r);
			(s[0] < q) && (s[0] = q);
			if ($isBrowser("ie6")) {
				this.boxIframeHandle.height = (this.sh - 2) + "px";
				this.boxIframeHandle.width = (this.sw - 2) + "px";
			}
			this.boxHandle.style.left = s[0] + "px";
			this.boxHandle.style.top = s[1] + "px";
			this.keepFix();
		}

		function j() {
			if (this.fix) {
				var i = this;
				if ($isBrowser("ie6")) {
					!this.fixTimer && (this.fixTimer = setInterval(function() {
						i.boxHandle.style.left = (i.left ? i.left : ($getPageScrollWidth() + ($getWindowWidth() - i.sw) / 2)) + "px";
						i.boxHandle.style.top = (i.top ? i.top : ($getPageScrollHeight() + ($getWindowHeight() - i.sh) / 2)) + "px";
					}, 30));
				} else {
					this.boxHandle.style.position = "fixed";
					this.boxHandle.style.left = (this.left ? this.left : ($getWindowWidth() - this.sw) / 2) + "px";
					this.boxHandle.style.top = (this.top ? this.top : ($getWindowHeight() - this.sh) / 2) + "px";
				}
			}
		}

		function e(i, p) {
			if (i && i.constructor === Number) {
				this.sw = i;
				this.boxHandle.style.width = this.sw + "px";
				if ($isBrowser("ie6")) {
					this.boxIframeHandle.width = (this.sw - 2) + "px";
				}
			}
			if (p && p.constructor === Number) {
				this.sh = p;
				this.boxHandle.style.height = this.sh + "px";
				if ($isBrowser("ie6")) {
					this.boxIframeHandle.height = (this.sh - 2) + "px";
				}
			}
			this.setPos();
		}

		function c() {
			if (this.autoResize) {
				var i = this;
				this.sizeTimer = setInterval(function() {
					i.sw = i.boxHandle.offsetWidth;
					i.sh = i.boxHandle.offsetHeight;
					if ($isBrowser("ie6")) {
						i.boxIframeHandle.height = (i.sh - 2) + "px";
						i.boxIframeHandle.width = (i.sw - 2) + "px";
					}
				}, 50);
			}
		}

		function g() {
			for (var i in a) {
				if (i == this.id) {
					continue;
				}
				a[i].close();
			}
		}

		function l(t) {
			var p = [];
			for (var u in a) {
				if (u != t) {
					p.push([u, a[u].zIndex]);
				}
			}
			if (p.length == 0) {
				return 9000;
			}
			p.sort(function(v, i) {
				return (v[1] < i[1]) ? -1 : (v[1] == i[1]) ? 0 : 1;
			});
			var s = p[0][1];
			if (s > 9999) {
				for (var q = p.length; q--;) {
					var r = a[p[q][0]];
					r.boxHandle.style.zIndex = r.zIndex = 9000 - q;
				}
			}
			return a[p[0][0]].zIndex + 1;
		}
	};
})();
var $loadCss = (function() {
	if (typeof $loadCss == "function") {
		return $loadCss;
	}
	var a = {};
	return window.$loadCss = function(c, d) {
		if (!c) {
			return;
		}
		var b;
		if (!a[c]) {
			b = document.createElement("link");
			b.setAttribute("type", "text/css");
			b.setAttribute("rel", "stylesheet");
			b.setAttribute("href", c);
			b.setAttribute("id", "loadCss" + Math.random());
			document.getElementsByTagName("head")[0].appendChild(b);
			a[c] = true;
		}
		b && (typeof d == "function") && (b.onload = d);
		return true;
	};
})();

function $isBrowser(d) {
	d = d.toLowerCase();
	var a = navigator.userAgent.toLowerCase();
	var c = false;
	switch (d) {
		case "chrome":
			c = a.indexOf("chrome") != -1;
			break;
		case "firefox":
			c = a.indexOf("firefox") != -1;
			break;
		case "safari":
			c = a.indexOf("safari") != -1 && a.indexOf("chrome") == -1;
			break;
		case "opera":
			c = a.indexOf("opera") != -1;
			break;
		case "ie":
			c = a.indexOf("msie") != -1;
			break;
		case "ie6":
			c = a.indexOf("msie 6") != -1;
			break;
		case "ie7":
			c = a.indexOf("msie 7") != -1;
			break;
		case "ie8":
			c = a.indexOf("msie 8") != -1;
			break;
		case "ie9":
			c = a.indexOf("msie 9") != -1;
			break;
		case "ie10":
			c = a.indexOf("msie 10") != -1;
			break;
		case "gecko":
			c = a.indexOf("opera") == -1 && a.indexOf("safari") == -1 && a.indexOf("chrome") == -1 && a.indexOf("gecko") > -1;
			break;
	}
	return c;
}

function $formatStr(c, b, a) {
	if (c) {
		if (typeof a == "undefined") {
			a = true;
		}
		c = c.replace(/{#([^#]+)#}/g, function(e, d) {
			return typeof b[d] != "undefined" ? b[d] : (a ? "" : e);
		});
		return c;
	}
	return "";
}

function $getPageScrollHeight() {
	var a = document.body;
	var b = document.compatMode == "BackCompat" ? a : document.documentElement;
	return b.scrollTop == 0 ? a.scrollTop : b.scrollTop;
}

function $getPageScrollWidth() {
	var a = document.body;
	var b = document.compatMode == "BackCompat" ? a : document.documentElement;
	return b.scrollLeft == 0 ? a.scrollLeft : b.scrollLeft;
}

function $getScrollPosition() {
	var b = document.documentElement.scrollLeft || document.body.scrollLeft || window.pageXOffset;
	var a = document.documentElement.scrollTop || document.body.scrollTop || window.pageYOffset;
	return [b ? b : 0, a ? a : 0];
}

function $getWindowHeight() {
	var a = document.body;
	return (document.compatMode == "BackCompat" ? a : document.documentElement).clientHeight;
}

function $getWindowWidth() {
	var a = document.body;
	return (document.compatMode == "BackCompat" ? a : document.documentElement).clientWidth;
}

function $getContentHeight() {
	var a = document.body;
	var b = document.compatMode == "BackCompat" ? a : document.documentElement;
	return (window.MessageEvent && navigator.userAgent.toLowerCase().indexOf("firefox") == -1) ? a.scrollHeight : b.scrollHeight;
}

function $getContentWidth() {
	var a = document.body;
	var b = document.compatMode == "BackCompat" ? a : document.documentElement;
	return (window.MessageEvent && navigator.userAgent.toLowerCase().indexOf("firefox") == -1) ? a.scrollWidth : b.scrollWidth;
}(function() {
	if (typeof $mask != "undefined") {
		return;
	}
	var c = 0,
		a, d = [0, 0],
		f;
	$mask = {
		add: function() {
			if (!a) {
				b();
			}
			if (!c) {
				e();
			}
			c++;
		},
		remove: function() {
			c--;
			if (!c) {
				a.style.display = "none";
			}
		}
	};

	function b() {
		var i = document.createElement("div");
		i.style.display = "none";
		i.style.width = "0px";
		i.style.height = "0px";
		i.style.backgroundColor = "#000000";
		i.style.zIndex = 250;
		i.style.position = "fixed";
		i.style.hasLayout = -1;
		i.style.left = "0px";
		i.style.top = "0px";
		i.style.filter = "alpha(opacity=20);";
		i.style.opacity = "0.2";
		if ($isBrowser("ie6")) {
			var h = document.createElement("iframe");
			$extend(h.style, {
				position: "absolute",
				left: "0px",
				top: "0px",
				width: "100%",
				zIndex: -1,
				border: "none",
				backgroundColor: "#000000"
			});
			h.setAttribute("allowtransparency", "yes");
			var g = setInterval(function() {
				try {
					h.contentWindow.document.body.style.backgroundColor = "#000000";
					clearInterval(g);
				} catch (j) {}
			}, 50);
			i.appendChild(h);
			i.style.position = "absolute";
			i.coverIframe = h;
		}
		a = i;
	}

	function e() {
		document.body.appendChild(a);
		a.style.display = "block";
		g();
		if (!f) {
			f = setInterval(function() {
				g();
			}, 50);
		}

		function g() {
			if (c > 0) {
				var k = $getContentHeight(),
					i = $getContentWidth(),
					h = $getWindowHeight(),
					l = $getWindowWidth(),
					j = [h, l];
				if ($isBrowser("ie6")) {
					a.style.top = $getPageScrollHeight() + "px";
				}
				if (j.toString() != d.toString()) {
					d = j;
					a.style.height = j[0].toFixed(0) + "px";
					a.style.width = j[1].toFixed(0) + "px";
					if (a.coverIframe) {
						a.coverIframe.style.height = j[0].toFixed(0) + "px";
						a.coverIframe.style.width = j[1].toFixed(0) + "px";
					}
				}
			}
		}
	}
})();

function $initDragItem(b) {
	var c = {
		barDom: "",
		targetDom: ""
	};
	for (var a in b) {
		c[a] = b[a];
	}
	var d = arguments.callee;
	d.option ? "" : d.option = {};
	c.barDom.style.cursor = "move";
	c.targetDom.style.position = "absolute";
	c.barDom.onmousedown = function(g) {
		var g = window.event || g;
		d.option.barDom = this;
		d.option.targetDom = c.targetDom;
		var f = [parseInt(c.targetDom.style.left) ? parseInt(c.targetDom.style.left) : 0, parseInt(c.targetDom.style.top) ? parseInt(c.targetDom.style.top) : 0];
		d.option.diffPostion = [$getMousePosition({
			evt: g
		})[0] - f[0], $getMousePosition({
			evt: g
		})[1] - f[1]];
		document.onselectstart = function() {
			return false;
		};
		window.onblur = window.onfocus = function() {
			document.onmouseup();
		};
		return false;
	};
	c.targetDom.onmouseup = document.onmouseup = function() {
		if (d.option.barDom) {
			d.option = {};
			document.onselectstart = window.onblur = window.onfocus = null;
		}
	};
	c.targetDom.onmousemove = document.onmousemove = function(f) {
		try {
			var f = window.event || f;
			if (d.option.barDom && d.option.targetDom) {
				d.option.targetDom.style.left = ($getMousePosition({
					evt: f
				})[0] - d.option.diffPostion[0]) + "px";
				d.option.targetDom.style.top = ($getMousePosition({
					evt: f
				})[1] - d.option.diffPostion[1]) + "px";
			}
		} catch (f) {}
	};
}

function $getMousePosition(a) {
	var a = window.event ? window.event : a;
	if (a.evt) {
		a = a.evt;
	}
	var b = [];
	if (typeof a.pageX != "undefined") {
		b = [a.pageX, a.pageY];
	} else {
		if (typeof a.clientX != "undefined") {
			b = [a.clientX + $getScrollPosition()[0], a.clientY + $getScrollPosition()[1]];
		}
	}
	return b;
}

function $extend() {
	var e = arguments[0] || {},
		c = 1,
		d = arguments.length,
		b;
	if (typeof e != "object" && typeof e != "function") {
		e = {};
	}
	for (; c < d; c++) {
		if ((b = arguments[c]) != null) {
			for (var a in b) {
				var f = b[a];
				if (e === f) {
					continue;
				}
				if (f !== undefined) {
					e[a] = f;
				}
			}
		}
	}
	return e;
}

function $login(b) {
	var g = {
		title: "登录后继续操作",
		callback: function() {}
	};
	var i = window.location.href,
		f = "https://shop.gionee.com";
	if (!i || i.indexOf(f) == -1) {
		i = "/";
	}
	g.skip = i;
	for (var c in b) {
		g[c] = b[c];
	}
	$setCookie("userReferer", g.skip);
	var h = $float({
		title: g.title,
		width: "700",
		html: '<iframe src="https://passport.gionee.com/cas/n/fl?service=https://shop.gionee.com/login_success.shtml" width="660px" height="470px" align="top" scrolling="no" frameborder="0"></iframe>'
	});
	try {
		var a = location.hostname,
			l = a.split(".");
		l.reverse(), l.length = 2, l.reverse();
		document.domain = l.join(".");
	} catch (j) {}
	window.loginsucess = function() {
		h.close();
		g.callback && g.callback();
	};
}

function $SlideOrgan(b) {
	this._selfId = (++this.constructor._newNum);
	this._selfName = ".SlideOrgan" + this._selfId;
	this.option = {
		width: 0,
		height: 0,
		navValue: 0,
		auto: false,
		delay: 2000,
		speed: 400,
		delayLoad: true,
		pos: 0,
		zIndex: 1,
		seleSlide: "",
		seleItem: ".ui_slide_item",
		seleNav: ".ui_slide_nav",
		cssCurrItem: "ui_slide_item_curr",
		onMoveBefore: null,
		onMoveAtfer: null
	};
	if (!b || !b.seleSlide) {
		return;
	}
	var c = this,
		a = c.option;
	for (var d in b) {
		a[d] = b[d];
	}
	c.init();
}
$SlideOrgan.prototype = {
	constructor: $SlideOrgan,
	init: function() {
		var b = this,
			a = b.option;
		b.domSlide = $(a.seleSlide);
		b.domItems = b.domSlide.children(a.seleItem);
		b.domNavs = b.domSlide.find(a.seleNav);
		b.initStatus();
		b.bindEvent();
		if (a.delayLoad) {
			a.onBeforeMove = b.fnDelay;
			$(window).bind("resize" + b._selfName + " scroll" + b._selfName, b, b.fnDelay);
			b.fnDelay();
		}
		if (a.auto) {
			b._timeout = setTimeout(function() {
				b.autoPlay();
			}, a.delay);
		}
	},
	initStatus: function() {
		var d = this,
			c = d.option;
		d.itemsLen = d.domItems.length;
		d.itemValue = d.domItems.eq(0).outerWidth(true);
		d.navValue = c.navValue || d.domNavs.eq(0).width();
		for (var b = 0, a = d.itemsLen; b < a; b++) {
			d.domItems.eq(b).css({
				zIndex: c.zIndex + (a - b),
				right: (a - b - 1) * d.navValue
			});
		}
		d.setStatus();
	},
	setStatus: function() {
		var b = this,
			a = b.option;
		b.domItems.removeClass(a.cssCurrItem);
		b.domItems.eq(a.pos).addClass(a.cssCurrItem);
	},
	bindEvent: function() {
		var b = this,
			a = b.option;
		b.domItems.bind("mouseenter", function() {
			clearTimeout(b.domItems._timeout);
			clearTimeout(b._timeout);
			b.domItems._timeout = setTimeout(function() {
				clearTimeout(b._timeout);
				clearTimeout(b.domItems._timeout);
				b.domItems.stop(false, true);
			}, a.speed);
		});
		b.domItems.bind("mouseleave", function() {
			clearTimeout(b.domItems._timeout);
			clearTimeout(b._timeout);
			b.domItems._timeout = setTimeout(function() {
				clearTimeout(b._timeout);
				clearTimeout(b.domItems._timeout);
				if (a.auto) {
					b._timeout = setTimeout(function() {
						b.autoPlay();
					}, a.delay);
				}
			}, a.speed);
		});
		b.domNavs.bind("mouseenter", function(f) {
			var d = $(this);
			var c = b.domNavs.index(d);
			if (c == b.option.pos) {
				return;
			}
			clearTimeout(b._timeout);
			b.domNavs._timeout = setTimeout(function() {
				clearTimeout(b._timeout);
				b.option.pos = c;
				b.move();
			}, 200);
		});
	},
	setPos: function() {
		var c = this,
			b = c.option,
			a = c.itemsLen;
		if (b.pos > a - 1 || b.pos < 0) {
			b.pos = 0;
		}
	},
	autoPlay: function() {
		var b = this,
			a = b.option;
		clearTimeout(b._timeout);
		a.pos++;
		b.setPos();
		b.move();
		b._timeout = setTimeout(function() {
			b.autoPlay();
		}, a.delay);
	},
	movefunc: function() {
		var e = this,
			d = e.option;
		e.domItems.stop(false, true);
		var a = e.itemsLen,
			g = e.itemValue,
			f = e.navValue;
		e.setStatus();
		for (var c = 0, b = 0; c < a; c++) {
			if (c < d.pos) {
				b = (a - c - 2) * f + g;
			} else {
				b = (a - c - 1) * f;
			}
			e.domItems.eq(c).animate({
				right: b
			}, d.speed, "easeInOut");
		}
	},
	move: function() {
		if (this.option.onBeforeMove) {
			this.onBeforeMove = this.option.onBeforeMove;
			this.onBeforeMove();
		}
		this.movefunc();
		if (this.option.onAfterMove) {
			this.onAfterMove = this.option.onAfterMove;
			this.onAfterMove();
		}
	},
	fnDelay: function(m) {
		var l = (m && m.data) || this,
			a = l.option;
		if (!l.delayImgs) {
			l.delayImgs = new Array(l.itemsLen);
			for (var h = 0, p; h < l.itemsLen; h++) {
				l.delayImgs[h] = l.delayImgs[h] || [];
				p = l.domItems.eq(h).find("img");
				p.each(function() {
					if ($(this).attr("orial_src")) {
						l.delayImgs[h].push(this);
					}
				});
			}
		}
		l.setPos();
		var o = a.pos;
		var n = $(window);
		var j = n.scrollTop(),
			f = n.height(),
			d = j + f;
		for (var h = 0, g = l.delayImgs[o], k = g.length; h < k; h++) {
			domjimg = $(g[h]);
			var c = parseInt(domjimg.offset().top);
			var b = parseInt(c + (domjimg.outerHeight() || 800));
			if ((c >= j && c <= d) || (b >= j && b <= d) || (c < j && b > d)) {
				domjimg.attr("src", domjimg.attr("orial_src"));
				g.splice(h, 1);
				h--;
				k--;
			}
		}
		for (var h = 0, k = l.delayImgs.length; h < k; h++) {
			if (l.delayImgs[h].length !== 0) {
				break;
			}
		}
		if (h === k) {
			a.onBeforeMove = null;
			$(window).unbind("resize" + l._selfName + " scroll" + l._selfName);
		}
	}
};
$SlideOrgan._newNum = 0;

function $SlideReview(b, d) {
	this._selfId = (++this.constructor._childNum);
	this._selfName = ".SlideReview" + this._selfId;
	this.option = {
		width: 0,
		height: 0,
		pos: 0,
		isRandom: false,
		speed: 400,
		delay: 6000,
		auto: true,
		delayLoad: true,
		col: 1,
		seleSlide: "",
		selePanel: ".ui_slide_panel",
		seleItems: ".ui_slide_item",
		seleOpts: ".ui_slide_opts",
		seleOpt: ".ui_slide_opt",
		selePrev: ".ui_slide_prev",
		seleNext: ".ui_slide_next",
		seleMaskPrev: ".ui_slide_maskPrev",
		seleMaskNext: ".ui_slide_maskNext",
		cssCurrItem: "ui_slide_item_curr",
		cssCurrOpt: "ui_slide_opt_curr",
		cssPrevHover: "ui_slide_prev_hover",
		cssNextHover: "ui_slide_next_hover",
		onBeforeMove: null,
		onAfterMove: null
	};
	if (!b || !b.seleSlide) {
		return;
	}
	var c = this,
		a = c.option;
	for (var e in b) {
		a[e] = b[e];
	}
	c.init();
}
$SlideReview.prototype = {
	constructor: $Slide,
	init: function() {
		var b = this,
			a = b.option;
		b.domSlide = $(a.seleSlide);
		b.domPanel = b.domSlide.find(a.selePanel);
		b.domItems = b.domPanel.find(a.seleItems);
		b.domOptCon = b.domSlide.find(a.seleOpts);
		b.domOptions = b.domOptCon.find(a.seleOpt);
		b.domPrev = b.domSlide.find(a.selePrev);
		b.domNext = b.domSlide.find(a.seleNext);
		b.domMaskPrev = b.domSlide.find(a.seleMaskPrev);
		b.domMaskNext = b.domSlide.find(a.seleMaskNext);
		b.itemsLen = b.domItems.length;
		if (b.itemsLen === 0) {
			b.domSlide.hide();
			return;
		}
		if (b.itemsLen === 1) {
			b.domOptCon.hide();
			b.domPrev.hide();
			b.domNext.hide();
			b.domMaskPrev.hide();
			b.domMaskNext.hide();
			if (a.delayLoad) {
				a.pos = 0;
				b.sumLen = 1;
				a.onBeforeMove = b.fnDelay;
				$(window).bind("resize" + b._selfName + " scroll" + b._selfName, b, b.fnDelay);
				b.fnDelay();
			}
			return;
		}
		if (b.itemsLen === 2) {
			b.domPrev.hide();
			b.domNext.hide();
			b.domMaskPrev.hide();
			b.domMaskNext.hide();
			b.domSlide.css({
				overflow: "hidden",
				width: b.domItems.eq(0).width(),
				"margin-left": "auto",
				"margin-right": "auto",
				"margin-top": "0",
				"margin-bottom": "0",
				height: "460px"
			});
		}
		b.domItems.clone().appendTo(b.domPanel);
		b.domItems = b.domPanel.find(a.seleItems);
		b.sumLen = b.domItems.length;
		if (b.sumLen < 4 * a.col + 1) {
			b.domItems.clone().appendTo(b.domPanel);
			b.domItems = b.domPanel.find(a.seleItems);
			b.sumLen = b.domItems.length;
		}
		b.initPos();
		b.initStatus();
		b.bindEvent();
		if (a.delayLoad) {
			a.onBeforeMove = b.fnDelay;
			$(window).bind("resize" + b._selfName + " scroll" + b._selfName, b, b.fnDelay);
			b.fnDelay();
		}
		if (a.auto) {
			b._timeout = setTimeout(function() {
				b.autoPlay();
			}, a.delay);
		}
	},
	initPos: function() {
		var b = this,
			a = b.option;
		if (a.isRandom) {
			a.pos = Math.floor(b.itemsLen * Math.random());
		}
	},
	initStatus: function() {
		var b = this,
			a = b.option;
		b.itemValue = a.width || b.domItems.eq(0).outerWidth(true);
		b.domPanel.css({
			width: b.itemValue * b.sumLen
		});
		b.setPos();
		b.domPanel.css({
			left: -a.pos * b.itemValue
		});
		b.setStatus();
	},
	setPos: function() {
		var d = this,
			b = d.option,
			a = d.itemsLen,
			c = d.sumLen;
		if (b.pos - b.col < 0) {
			b.pos = b.pos + a;
		}
		if (b.pos + b.col > c - 1) {
			b.pos = b.pos - a;
		}
	},
	setStatus: function() {
		var b = this,
			a = b.option;
		b.setPos();
		b.domItems.removeClass(a.cssCurrItem);
		b.domItems.eq(a.pos).addClass(a.cssCurrItem);
		b.domOptions.removeClass(a.cssCurrOpt);
		b.domOptions.eq(a.pos % b.itemsLen).addClass(a.cssCurrOpt);
	},
	autoPlay: function() {
		var b = this,
			a = b.option;
		clearTimeout(b._timeout);
		a.pos++;
		b.move();
		b._timeout = setTimeout(function() {
			b.autoPlay();
		}, a.delay);
	},
	movefunc: function(e) {
		var b = this,
			a = b.option;
		b.domPanel.stop(false, true);
		var d = parseInt(b.domPanel.css("left")) || 0;
		if (a.pos + a.col > b.sumLen - 1) {
			a.pos = a.pos - b.itemsLen;
			d = -(a.pos - 1) * b.itemValue;
		} else {
			if (a.pos - a.col < 0) {
				a.pos = a.pos + b.itemsLen;
				d = -(a.pos + 1) * b.itemValue;
			}
		}
		b.domPanel.css({
			left: d
		});
		b.setStatus();
		var c = -a.pos * b.itemValue;
		if (e) {
			b.domPanel.animate({
				left: c
			}, e);
		} else {
			b.domPanel.animate({
				left: c
			}, a.speed, "easeInOut");
		}
	},
	move: function(a) {
		if (this.option.onBeforeMove) {
			this.onBeforeMove = this.option.onBeforeMove;
			this.onBeforeMove();
		}
		this.movefunc(a);
		if (this.option.onAfterMove) {
			this.onAfterMove = this.option.onAfterMove;
			this.onAfterMove();
		}
	},
	bindEvent: function() {
		var b = this,
			a = b.option;
		if (b.itemsLen > 2) {
			b.domSlide.bind("mouseenter", function(c) {
				clearTimeout(b.domSlide._timeout);
				b.domSlide._timeout = setTimeout(function() {
					b.domPrev.show();
					b.domNext.show();
				}, 200);
			});
			b.domSlide.bind("mouseleave", function(c) {
				clearTimeout(b.domSlide._timeout);
				b.domSlide._timeout = setTimeout(function() {
					clearTimeout(b.domSlide._timeout);
					b.domPrev.hide();
					b.domNext.hide();
				}, 200);
			});
		}
		b.domItems.bind("mouseenter", function(c) {
			clearTimeout(b.domItems._timeout);
			clearTimeout(b._timeout);
			b.domItems._timeout = setTimeout(function() {
				clearTimeout(b._timeout);
				clearTimeout(b.domItems._timeout);
				b.domItems.stop(false, true);
			}, 200);
		});
		b.domItems.bind("mouseleave", function(c) {
			clearTimeout(b.domItems._timeout);
			clearTimeout(b._timeout);
			if (b.option.auto) {
				b._timeout = setTimeout(function() {
					b.autoPlay();
				}, a.delay);
			}
		});
		b.domOptions.bind("mouseenter", function(d) {
			clearTimeout(b.domOptions._timeout);
			var c = this;
			b.domOptions._timeout = setTimeout(function() {
				clearTimeout(b._timeout);
				clearTimeout(b.domOptions._timeout);
				b.domPanel.stop(false, true);
				var e = $(c).parent().children().index(c);
				if (a.pos % b.itemsLen !== e) {
					a.pos = e;
					b.move(1);
				}
			}, 200);
		});
		b.domOptions.bind("mouseleave", function(c) {
			clearTimeout(b._timeout);
			clearTimeout(b.domOptions._timeout);
			if (b.option.auto) {
				b._timeout = setTimeout(function() {
					b.autoPlay();
				}, a.delay);
			}
		});
		b.domPrev.bind("click", function(c) {
			b.movePrev();
		});
		b.domNext.bind("click", function(c) {
			b.moveNext();
		});
		b.domMaskPrev.bind("click", function(c) {
			b.movePrev();
		});
		b.domMaskNext.bind("click", function(c) {
			b.moveNext();
		});
	},
	movePrev: function() {
		var b = this,
			a = b.option;
		clearTimeout(b._timeout);
		a.pos--;
		b.move();
		b._timeout = setTimeout(function() {
			b.autoPlay();
		}, a.delay);
	},
	moveNext: function() {
		var b = this,
			a = b.option;
		clearTimeout(b._timeout);
		a.pos++;
		b.move();
		b._timeout = setTimeout(function() {
			b.autoPlay();
		}, a.delay);
	},
	fnDelay: function(x) {
		var o = (x && x.data) || this,
			f = o.option;
		if (!o.delayImgs) {
			o.delayImgs = new Array(o.itemsLen);
			for (var v = 0, c, t = 0; v < o.sumLen; v++) {
				c = o.domItems.eq(v).find("img");
				t = v % o.itemsLen;
				o.delayImgs[t] = o.delayImgs[t] || [];
				c.each(function() {
					if ($(this).attr("orial_src")) {
						o.delayImgs[t].push(this);
					}
				});
			}
		}
		var m = f.pos,
			q = [],
			l = m % o.itemsLen,
			h, g;
		q.push(l);
		m - f.col < 0 ? h = m - f.col + o.itemsLen : h = (m - f.col) % o.itemsLen;
		if (h !== l) {
			q.push(h);
		}
		m + f.col < o.sumLen ? g = m + f.col : g = m + f.col - o.itemsLen;
		g %= o.itemsLen;
		if (g !== l && g !== h) {
			q.push(g);
		}
		var u = $(window);
		var d = u.scrollTop(),
			s = u.height(),
			k = d + s;
		for (var v = 0, w = q.length, a; v < w; v++) {
			a = o.delayImgs[q[v]];
			for (var t = 0, n = a.length, r; t < n; t++) {
				r = $(a[t]);
				var p = parseInt(r.offset().top);
				var b = parseInt(p + (r.outerHeight() || 800));
				if ((p >= d && p <= k) || (b >= d && b <= k) || (p < d && b > k)) {
					r.attr("src", r.attr("orial_src"));
					a.splice(t, 1);
					t--;
					n--;
				}
			}
		}
		for (var v = 0, w = o.delayImgs.length; v < w; v++) {
			if (o.delayImgs[v].length !== 0) {
				break;
			}
		}
		if (v === w) {
			f.onBeforeMove = null;
			$(window).unbind("resize" + o._selfName + " scroll" + o._selfName);
		}
	}
};
$SlideReview._childNum = 0;
