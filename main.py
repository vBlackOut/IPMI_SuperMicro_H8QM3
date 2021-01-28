import requests
import BeautifulSoup
import time
import os
import subprocess
import psutil
import shlex 
import json
import base64
from secure import decode
from requests.packages.urllib3.exceptions import InsecureRequestWarning

print("Connection...")
s = requests.Session()

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
host = "IP_HERE"
password = "PASSWORD_HERE"


data = {'login': 'LOGIN_HERE', 'password': decode("1234", password), 'nickname': '', 'action_login.x': '0', 'action_login.y': '0'}

session = s.post("https://"+ str(host) +"/auth.asp", data=data, verify=False)
print "retry information..."
cookies = s.cookies.get_dict()
print cookies
if "The user is blocked" in session.text:
	print "Error - User is blocked"
	exit(1)
try:
   cookie = cookies["pp_session_id"]
except KeyError:
   print "max user connecting or error connection."
   exit(1)
time.sleep(2)
print("I'm Logged...")
print("I'm get the Token...")
token = cookie


generated_jnlp = """
<?xml version="1.0" encoding="UTF-8"?>
<jnlp codebase="http://{0}" spec="1.5+">
<information>
    <title>Sweet Home 3D</title>
    <vendor>eTeks</vendor>
    <homepage href="http://www.sweethome3d.com/"/>
    <description>Sweet Home 3D</description>
    <description kind="short">Arrange the furniture of your house</description>
    <icon href="SweetHome3DIcon.gif"/>
    <icon kind="splash" href="SweetHome3DSplashScreen.jpg"/>
    <offline-allowed/>
    <shortcut online="false">
      <desktop/>
      <menu submenu="eTeks Sweet Home 3D"/>
    </shortcut>
    <association extensions="sh3d sh3l sh3f sh3t sh3p" mime-type="application/SweetHome3D"/>
  </information>


<applet-desc main-class="nn.pp.rc.RemoteConsoleApplet.class" progress-class="nn.pp.rc.RemoteConsoleApplet.class" archive="rc.jar, drvredir.jar, rcsoftkbd.jar" name="Dynamic Tree Demo Applet" width="1024" height="768"> 
      <param name="progressbar" value="true"/>
      <param name="REAL_HOST" value=""/>
      <param name="BOARD_NAME" value="Board_SuperMicro_Java_Cuby-Hebergs"/>
      <param name="BOARD_TYPE" value="lara"/>
      <param name="HW_ID" value="22"/>
      <param name="SESSION_ID" value="{1}"/>
      <param name="PORT" value="443"/>
      <param name="SSLPORT" value="443"/>
      <param name="NORBOX" value="no"/>
      <param name="NORBOX_IPV4TARGET" value=""/>
      <param name="NORBOX_IPV6TARGET" value=""/>
      <param name="PROTOCOL_VERSION" value="01.16"/>
      <param name="HOTKEY_0" value="confirm Ctrl+Alt+Delete"/>
      <param name="HOTKEYCODE_0" value="36 f0 37 f0 4e "/>
      <param name="HOTKEYNAME_0" value=""/>

      <param name="KBD_LAYOUT" value="pc109"/>
      <param name="SOFTKBD_MAPPING" value="en_EN"/>
      <param name="MOUSESYNC_KEY" value="Alt+F12"/>
      <param name="EXCLUSIVE_MOUSE" value="no"/>
      <param name="MOUSESYNC_KEYCODE" value="37 47 "/>
      <param name="LOCAL_CURSOR" value=""/>      
      <param name="PORT_ID" value=""/>
      <param name="CLUSTER_PORT_ID" value=""/>
      <param name="HOTKEYPAUSE" value="100"/>
      
      <param name="DRIVE_REDIRECTION" value="yes"/>
      <param name="FORENSIC_CONSOLE" value="no"/>
      <param name="DRIVE_REDIRECTION_NO_DRIVES" value="2"/>
      <param name="VS_TYPE" value=""/>
      <param name="VS_PERM_STD" value="yes"/>
      <param name="VS_PERM_ADV" value="yes"/>
      <param name="USE_IIP" value="yes"/>
      <param name="MONITOR_MODE" value="no"/>
      <param name="logo" value="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Logo_TV_2015.png/280px-Logo_TV_2015.png"/>
      <param name="logo_off" value="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Logo_TV_2015.png/280px-Logo_TV_2015.png"/>
      <param name="EXCLUSIVE_PERM" value="on"/>
      <param name="SSL" value="on"/>
      <param name="HWENC" value="yes"/>
      <param name="SelEnc" value="auto"/>
      <param name="FixEnc" value="lanhi"/>
      <param name="AdvEncCR" value="uncompressed"/>
      <param name="AdvEncCD" value="color_16bpp"/>
      <param name="InFrame" value="no"/>
      <!--<param name="bgcolor" value="#a0c0d0"/>-->
    </applet>


 <security>
   <all-permissions/>
 </security>
 <update check="always" policy="always" />
 <resources>
   <j2se href="http://java.sun.com/products/autodl/j2se" version="1.5+"/>
  <!-- <jar href="http://localhost/app/get_jar.php&#63;session={1}&amp;url=/drvredir.jar&amp;host={0}" main="false"/> -->
   <jar href="http://localhost/app/get_jar.php&#63;session={1}&amp;url=/rc.jar&amp;host={0}" download="progress" />
   <property name="nn.pp.rc.RemoteConsoleApplet.class" value="true" />
   <!-- <nativelib href="http://localhost/app/get_jar.php&#63;session={1}&#38;url=/rcsoftkbd.jar&#63;host={0}" main="false"/> -->
 </resources>
</jnlp>""".format(host, cookie)

print("Generated JNLP File...")

with open('supermicro.jnlp', 'wb') as file:
    file.write(generated_jnlp)
#os.system("/usr/java/jre1.8.0_121/bin/javaws -offline supermicro.jnlp")
#p = subprocess.Popen(['/usr/java/jre1.8.0_121/bin/javaws', '-offline', 'supermicro.jnlp'])
#p = subprocess.Popen("/usr/java/jre1.8.0_121/bin/javaws -offline supermicro.jnlp", shell=True, preexec_fn=os.setsid)

def run_command(command):
	list_output = []
	process = subprocess.Popen(shlex.split(command), shell=False, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
	while True:
		output = process.stdout.readline()
		if output == '' and process.poll() is not None:
			break
		if output:
			list_output.append(output)
	rc = process.poll()
	return list_output


print("Open Process Java...") 
run_command('/usr/java/jre1.8.0_121/bin/javaws -offline supermicro.jnlp')
print("Logout for IPMI")
session2 = s.get("https://"+str(host)+"/logout", verify=False)
if session2.status_code == "200":
   exit()
