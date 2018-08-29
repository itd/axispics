axispics README
=================

This captures a series of images from one or more AXIS
cameras, and saves then to a specified directory. It's a
very minimal application. Add features and functionality
as your need or desire dictates.

AXIS software can be configured to throw jpg images at a web server.
Edit the .cfg file(s) then fire-up this application to get
a web server running. Then, point all the cameras at this app.
No additional server-side configuration should be necessary.

Images from each camera are saved to disk in per-camera-ip-date
directories:

  $axis_pic_path/$CAMERA_IP_ADDRESS_$DATE

For example:

  /path/to/images/192.168.0.102_2012-11-30

More info about AXIS cameras can be found at:
  http://www.axis.com/


Requirements
===============
This is a Pyramid app. It's an embarrassingly simple
and most likely awful app, but it does the job for
what I needed. At least for now.

You'll want Pyramid 1.3+. To get it working,
set up a python 2.7.x or better virtualenv.
For example::

  cd $your_dev_dir
  virtualenv venv-vid

source the virtualenv::

  $ source venv-vid/bin/activate

Since this runs under Pyramid, install Pyramid.
I don't know the "standard" install method, but if I did,
it would look something like this::

  $ pip install -r requirements.txt
  $ git clone git@github.com:itd/axispics.git
  $ cd ./axispics
  $ python setup.py develop
  # Configure the app
    * Edit the value for "axis_pic_path" in both
      the production.ini and development.ini files.
      (Make sure your <axis_pic_path> exists.)
  * Fire up your Pyramid app.

  $ ../venv-axis/bin/pserve development.ini --reload

Your app *should* now be running on port 6543.
Did it work? if so, shove this into cron:

 # crontab -e
 # run it every 10 minutes, just to make sure it's running.
 # m   h   dom  mon  dow   command
 */10   *   *    *    *    /opt/axispics/venv-axis/bin/pserve /opt/axispics/axispics/production.ini > /dev/null 2>&1


It's rude, but it works.

Configure your AXIS camera
==============================
I'll assume you've hacked around with your AXIS camera and
figured out how to set up the password, IP address, and date/time.
I'm using a couple of the Axis 5512 IP cameras. The software on those
seems to deliver a reasonable image quality for what I need.
Now, on to getting it to talk to this cheezy little app...


Create an Event Server
-----------------------

Under [Events > Event Servers] select [Add HTTP...]

Give it a name, and point it at the pyramid app.
Assuming your server's IP address is 192.168.0.11
and you use the default Pyramid port of 6543,
you'll add the /pics view controller to the URL.

Example::
  **Event Server Setup**
  **HTTP Server**
  Name: axis_pic_server
  URL: http://192.168.0.11:6543/pics

Click [OK]

NOTE: My cameras are on a closed private network
(only the cameras and the server), so at the moment
I'm not too terribly concerned about security. If you
want to add password security into this app, go for it.


Configure an Event Type (HTTP)
----------------------------------------

Do this under [Events > Event Types]

For Motion Detection, select [Add Triggered...]
For a timer, select [Add scheduled...]

I'm using Motion Detection.
You'll have to create a "Motion Detection" window
under [Events > Motion Detection] first if you want
to play with that option.

Also, I'm lazy and letting the camera define the file names.
So make sure you set the date/time correctly on your cameras.

Tip: prefix your file names with something consistent and identifiable,
e.g., "cam-102-"., and do that consistently per camera. If you need to
script something against the files, you'll have something to work with.


Example Scheduled Event set up
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is probably the event type most often used. These are just general
ideas for settings. Roll your own.

* Fill in the <Name> field
* click the Save stream checkbox
* Set your Image frequency to some reasonable numbers,
  maybe 1 per second to start
* Select upload type: HTTP
* Set the *Upload to HTTP server* to the Event Server you created earlier
* Set the *Base file name:* I set mine to something unique, like cam-02-.jpg
* Click the Add date/time suffix
* click the [OK] button

At this point, your AXIS camera should be hurling images at the Pyramid app.

It's all pretty simple. If it doesn't work, well...
let me know and I'll see if I can fix it.


Encoding jpg into a movie
=========================
I'm still working on this. In linux, ffmpeg/avconv wants files in a consistent
number format. Since I was using the stock AXIS date formatting doesn't work
(However, I believe the date formatting can be tweaked to work.)

mencoder seems to work for now. Here's a stab at getting
something working that gets all the .jpg files in the current directory
and writes them to "/out/path/outputfile.mp4". I've read there may be
issues with the mp4 container. I'm still working with this.

mencoder mf://*.jpg -mf fps=30:type=jpg -ovc x264 -x264encopts \
  bitrate=1400:threads=2 -lavfopts format=mp4 -o /out/path/outputfile.mp4

