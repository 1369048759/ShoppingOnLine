var popDialog = function(s, c){
	
	var dialog = $(s);
	
	var closeDialog = function(){
		dialog.fadeOut();
	}
	
	if(!dialog.data('inited')){
		if(!c){
			dialog.on('click', closeDialog);
			dialog.find('.pop_close').on('click', closeDialog);
			dialog.find('.pop_body').on('click', function(e){
				e.stopPropagation();
			});
		}
		dialog.data('inited', true);
	}
	
	dialog.fadeIn();
	
	var wh = $(window).innerHeight();
	var ch = dialog.find('.pop_con').outerHeight();
	var t = Math.max((wh - ch) * 0.5 + $(window).scrollTop(), 0);
	dialog.find('.pop_con').css('margin-top', t);
	
}

var getStatusText = function(status){
	var s = status.toString();
	if(status=="0")
		return "未激活";
	else if(status=="1")
		return "保障中";
	else if(status=="2")
		return "已使用";
	else if(status=="3")
		return "已过保";
	else if(status=="4")
		return "已退保";
	else if(status=="5")
		return "已转移";
	else if(status=="6")
		return "待支付";
	else if(status=="7")
		return "退保待审核";
	else if(status == '8'){
		return '已作废';
	}
}