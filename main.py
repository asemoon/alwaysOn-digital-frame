from alwayson import always_on
from threading import Timer
import time
alwayson_obj=always_on()
alwayson_obj.get_settings()
def alwayson_timer(start, interval, count, alwayon):
	print "Reached restarting point"
	ticks = time.time()
	t = Timer(1- (ticks-start-count*interval), alwayson_timer, [start, interval, count+1, alwayon])
	alwayson_obj.create_playlist()
	keep_running=True
	alwayon.get_settings()
	if alwayon.can_i_download_now():
		print "Within allowed time, syncing in progress"
		dl_list,del_list=alwayon.get_list_of_incoming_and_deleting(alwayon.get_list_of_local_files(), alwayon.get_list_of_cloud_files())
		alwayon.sync_contents(dl_list, del_list) 
		if len(del_list)!=0 or len(dl_list)!=0:
			print "VLC needs to be restarted"
			keep_running=False
	alwayon.run_vlc(keepRunning=keep_running)
	time.sleep(float(alwayon.timer_interval)) # interval in sec
	t.start()   
if __name__ == "__main__":	
	t = Timer(1, alwayson_timer, [round(time.time()), 1, 0, alwayson_obj])
	t.start()