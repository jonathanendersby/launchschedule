var launch_json = null;
var launch_html = '';

function updateComponents(){
	
	var badge_set = false;
	launch_html = '';
 	$.each( launch_json, function( i, launch ) {
	  
		launch_html = launch_html + '<div class="launch"><h1>' + launch.mission + '</h1><h2>' + launch.vehicle + '</h2>'
		
		if (launch.gmt_date){
			var thedate = new Date(launch.gmt_date);
			var ms = (thedate - Date.now())
						
			var x = 0
			x = ms / 1000
			seconds = x % 60
			x /= 60
			minutes = x % 60
			x /= 60
			hours = x % 24
			x /= 24
			days = x
		
			if (!badge_set & ms > -1080000){  // If we haven't yet set the badge and this launch no older than 3 hours

				if ( ms < 3600000){ // 1 hour
					chrome.browserAction.setBadgeBackgroundColor({color:[200, 0, 0, 200]}); // Bright green
					chrome.browserAction.setBadgeText({text:parseInt(minutes) + ' m'});
					badge_set = true;

				}else if( ms < 86400000 ){ // 1 day.
					chrome.browserAction.setBadgeBackgroundColor({color:[0, 150, 0, 200]}); // Green
					chrome.browserAction.setBadgeText({text:parseInt(hours) + ' h'});
					badge_set = true;

				}else if( ms < 604800000 ){ // 7 days
					chrome.browserAction.setBadgeBackgroundColor({color:[255, 178, 0, 200]}); // Orange
					chrome.browserAction.setBadgeText({text:parseInt(days) + ' d'});
					badge_set = true;						
	
				}else if( ms < 2678400000 ){ // 31 days
					chrome.browserAction.setBadgeBackgroundColor({color:[170, 178, 170, 200]}); // Grey
					chrome.browserAction.setBadgeText({text:parseInt(days) + ' d'});
					badge_set = true;		
				}
						
			}						
			
			launch_html = launch_html + '<div class="until">Launch in ' + parseInt(days) + ' days, ' + parseInt(hours) + ' hours, ' + parseInt(minutes) + ' minutes</div>'
		}
	
		launch_html = launch_html + '<div class="desc">' + launch.description + '</div> \
		<div class="launch_site">' + launch.launch_site + '</div>'
		
		if (launch.gmt_date){
			launch_html += '<div class="local_time">' + thedate.toString() + '</div>'
		}	
		
		launch_html += '</div>';	
	});
	
	if (!badge_set){  //Nothing set the badge, lets clear it.
		chrome.browserAction.setBadgeText({text:''});
	}
	
    chrome.runtime.sendMessage({ action: "rerender" });  // Send a message to popup.js instructing it to update popup.html.	
}


function fetchLaunchSchedule() {
	var ls_url = 'http://underground.co.za/launchschedule.json';
	
    $.getJSON(ls_url, {})
		.done(function( data ) {
			launch_json = data.launches
			updateComponents();
		});
}

fetchLaunchSchedule();
setInterval(fetchLaunchSchedule, 3600000); // Every 60 minutes.
setInterval(updateComponents, 59000); // Every 59 seconds.
