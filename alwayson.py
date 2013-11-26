#AlwaysOn by Mehdi Karamnejad
#Nov 2013
import dropbox
import glob
import os
import ConfigParser
from xml.dom import minidom
from urllib import urlopen
from datetime import time,datetime
import subprocess
import sys

app_key = ''
app_secret = ''
access_token=''
user_id=''
pix_root_folder_on_cloud='/pix/'
settings_path_on_cloud='/'
class always_on():
	def authorize(self):
		flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
		authorize_url = flow.start()
		print "Get an authorization code from the following url \n"+authorize_url
		code = raw_input("Enter the authorization code here: ").strip()
		access_token, user_id = flow.finish(code)
		print "Access token is:"+access_token
		print "User ID is:"+user_id
		raise SystemExit
	def __init__(self):	

		if access_token=="":
			print "It seems that you have not set the access token yet; calling authorize method..."
			self.authorize()			
		else:
			self.client = dropbox.client.DropboxClient(access_token)		
			f = open('config.txt')
			self.local_pix_folder=f.readline().strip()	
			if self.local_pix_folder[-1] !=os.sep : self.local_pix_folder=self.local_pix_folder+os.sep
			self.vlc_location=f.readline().strip()
			self.vlc_location.replace("\\","\\\\")
			self.vlc_process=None
	def __del__(self):
		try:
			if self.vlc_process != None and self.vlc_process.pid != 0:
				self.vlc_process.terminate()
		except Exception, error:
			print "I'm sorry I couldn't terminate VLC because:"+str(error)
	def run_vlc(self, keepRunning=False):
		if not getattr(__builtins__, "WindowsError", None):			
			class WindowsError(OSError): pass					
		try:
			if self.vlc_process != None and self.vlc_process.pid != 0 and keepRunning and self.vlc_process.poll()==None:
				return#everything is going well and no need to restart vlc
			if self.vlc_process != None and self.vlc_process.pid != 0:
				self.vlc_process.terminate()
			self.vlc_process = subprocess.Popen([self.vlc_location, 'playlist.m3u'], shell=False)
		except WindowsError:
			print "VLC seems to be closed, starting another one..."
			self.vlc_process = subprocess.Popen([self.vlc_location, 'playlist.m3u'], shell=False)
		except OSError:
			print "VLC seems to be closed, starting another one..."
			self.vlc_process = subprocess.Popen([self.vlc_location, 'playlist.m3u'], shell=False)			
		except Exception, error :
			print "sth went wrong:"+str(error)
	def create_playlist(self):
		playlist_file=open('playlist.m3u','w')
		for i in self.get_list_of_local_files():
			playlist_file.write(i+"\n")
		playlist_file.close()	
		print "Playlist for VLC created"
	def get_time(self):#default location is Tehran, IRAN
		xmldoc = minidom.parse(urlopen("http://www.earthtools.org/timezone/"+self.latitude+"/"+self.longitude))
		raw_tehran_date_time=xmldoc.getElementsByTagName('localtime')[0].childNodes[0].nodeValue
		tehran_time=raw_tehran_date_time[raw_tehran_date_time.rfind(" ")+1:]		
		return tehran_time
	def can_i_download_now(self):									 	
		start_time=time(int(self.start_time[0:2]),int(self.start_time[3:5]))
		end_time= time(int(self.end_time[0:2]),int(self.end_time[3:5]))
		time_str=self.get_time()
		current_time=time(int(time_str[0:2]),int(time_str[3:5]))					
		return True if start_time<= current_time<= end_time else False
	def get_list_of_local_files(self):						
		raw_list_of_files=glob.glob(self.local_pix_folder+"*")
		return raw_list_of_files
	def get_list_of_cloud_files(self):		
		folder_metadata = self.client.metadata(pix_root_folder_on_cloud)		
		list_of_files=[]
		for i in folder_metadata['contents']:
			list_of_files.append(i['path'])			
		return list_of_files
	def get_list_of_incoming_and_deleting(self, local_files, cloud_files):		
		local_tmp=list(local_files)
		cloud_tmp=list(cloud_files)		
		for i in cloud_files:
			if any(e for e in local_files if e.endswith(i[i.rfind('/')+1:])):
				cloud_tmp.remove(i)
		for i in local_files:
			if any(e for e in cloud_files if e.endswith(i[i.rfind(os.sep)+1:])):
				local_tmp.remove(i)
		return cloud_tmp, local_tmp #download from the cloud, # delete from the local respectively
	def sync_contents(self, downloading_list, deleting_list):
		print "Syncing now...."
		for i in downloading_list:
			print "Downloading "+i
			f, metadata = self.client.get_file_and_metadata(i)
			out = open(self.local_pix_folder+i[i.rfind("/")+1:], 'wb')
			out.write(f.read())
			out.close()
		for i in deleting_list:
			try:
				os.remove(i)
			except:
				print "Couldn't remove "+i+" probably because VLC is using it"
				pass
		self.create_playlist()
	def get_settings(self):			
		f, metadata = self.client.get_file_and_metadata(settings_path_on_cloud+"settings.cfg")
		out = open('tmpsettings.cfg', 'w')		
		out.write(f.read())
		out.close()
		self.config = ConfigParser.ConfigParser()
		self.config.readfp(open('tmpsettings.cfg'))		
		if self.config.get('global','wipe_pix')=='1':						
			files = glob.glob(self.local_pix_folder+"*")			
			for f in files:				
				os.remove(f)
		if self.config.get('global','system_on')=='0':
			print "The system has been deactivted, contact the content manager!"
			raise SystemExit			
		self.start_time=self.config.get('global','start_time')
		self.end_time=self.config.get('global','end_time')
		self.slide_show_duration=self.config.get('global','slide_show_duration')
		self.longitude=self.config.get('global','longitude')
		self.latitude=self.config.get('global','latitude')
		self.timer_interval=self.config.get('global','timer_interval')
		os.remove('tmpsettings.cfg')
