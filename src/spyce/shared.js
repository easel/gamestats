function toggleTrash(item_id, element_id) {
    var callback =
    {
	success: function(o) {
	    document.getElementById(element_id).innerHTML=o.responseText;
	},
	scope: this
    }
    var cObj = YAHOO.util.Connect.asyncRequest('GET','item.spy?toggle_trash&item_id='+item_id,callback,null);
}

function setItemType(item_id, element_id) {
    var callback =
    {
	success: function(o) {
	    document.getElementById(element_id).value=o.responseText;
	},
	scope: this
    }
    type=document.getElementById(element_id).value
    var cObj = YAHOO.util.Connect.asyncRequest('GET','item.spy?set_item_type=' 
	+ type + '&item_id=' + item_id,callback,null);
}

