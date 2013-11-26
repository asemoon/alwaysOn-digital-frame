AlwaysOn Digital Frame
========

![AlwaysOn Digital Photo Frame](/images/alwayson_digital_frame_workflow.jpg)

This script slideshows media residing on a specific folder in a Dropbox account. It was initially targeted to be enlisted on OS boot up to slideshow the media on the cloud using VLC(so you need VLC installed). It automatically syncs itself with a Dropbox folder in the intervals that the user defines and continuously runs VLC with the media (pictures, videos, and audio). Think of it as a fancy digital photo frame that gets automatically updated! 


Settings
========
1. Install Dropbox Python SDK either via https://www.dropbox.com/developers/core/sdks/python 
or if you are comfortable using easy_install, do a `easy_install dropbox`

2. Clone the AlwaysOn Frame repository 
```bash
git clone https://github.com/asemoon/alwaysOn-digital-frame.git
```
3. Visit http://www.dropbox.com/developers/apps, create a new Dropbox app, and obtain an app_key and an app_secret
Open alwaysOn.py and set the global variables app_key and app_secret with what you have obtained (they are set to ' ' by default). Run main.py and paste the URL into your browser, follow the instructions and press allow. Then copy the string the Dropbox provides you and paste it at the prompt where it says, "Enter the authorization code here". The script will then give you a user_id and an access_token. Copy those values and paste as values of user_id and access_token in alwaysOn.py accordingly. (Note that what you are doing right now is letting a Dropbox account to be accessed using the SDK so you need to be signed in to your Dropbox account). The good news is you only do this step once!
4. For smoother slideshow, set the following settings in VLC:      
A)Repeat the playlist (Playback->Repeat all) B)in Video section of VLC options, check fullscreen C)Turn off "show unimportant error messages"

5. Create a file named config.txt where the alwaysOn script resides. The first line is the location that you want to keep your pictures; the second line is the location of VLC executable.     
For instance:    
```bash
C:\ Users\ Mehdi\ pix    
C:\ Program Files (x86)\ VideoLAN \ VLC\ vlc.exe
```
6. In alwayson.py file set the global variables for your images folder and the config file path on the cloud (the config file should be named settings.cfg)
The default values are:   
pix_root_folder_on_cloud='/pix/'   
settings_path_on_cloud='/'   

7. The settings.cfg on the cloud, controls the settings of the slideshow. here is an example with descriptions:    
```bash
[global]   
system_on=1 #Whether the system should be on or not   
timer_interval=3600 # The interval to check for syncs (in seconds)   
slide_show_duration=10 #Duration of photo slideshow   
wipe_pix=0 #Will delete the contents of the pictures folder if set to 1   
start_time=01:00 # The start of the time which syncing is allowed   
end_time=23:00  # The end of the time which syncing is allowed   
longitude=51.4231 # the longitude to use for obtaining the time   
latitude=35.6961 # the latitude to use for obtaining the time   
```

All the settings are done once and then you are all set! just run main.py from then on.   


Nov 2013, Mehdi Karamnejad