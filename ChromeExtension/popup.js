function rerender(){
	document.getElementById('launches').innerHTML = chrome.extension.getBackgroundPage().launch_html;
}

document.addEventListener('DOMContentLoaded', function() {
	rerender();
});

chrome.runtime.onMessage.addListener(
	function(request, sender, sendResponse) {
		
		if (request.action == "rerender"){
			rerender();	
		}
		
	});