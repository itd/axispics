axispics README
=================

This captures a series of images from one or
more AXIS cameras, and saves then to a specified
directory ($axis_pic_path).

AXIS software will throw/put jpg images at a
web server. All you should have to do is fire-up
this service and point all the cameras at this app.
No additional server side configuration is necessary.

Images from each camera are saved to disk in
individual directories:

  $axis_pic_path/$CAMERA_IP_ADDRESS

For example:

  /path/to/images/192.168.0.102


Requirements
===============
This is a Pyramid app. It's an embarrassingly simple
and most likely awful app, but it does the job for
what I needed. At least for now.

You'll want Pyramid 1.3+. To get it working,
set up a python 2.7.x or better virtualenv.
For example::

  virtualenv venv-axis

source the virtualenv::

  $ source venv-axis/bin/activate

Since this runs under Pyramid, install Pyramid.
I don't know the "standard" install method, but if I did,
it would look something like this::

  $ cd venv-axis
  $ easy_install pyramid
  $ mkdir src
  $ cd src
  $ git clone
  $ cd axispics
  $ python setup.py develop
  # Configure the app
  * Edit the value for "axis_pic_path" in both
    the production.ini and development.ini files.
    (Make sure your <axis_pic_path> exists.)
  * Fire up your Pyramid app.

  $ ../bin/pserve development.ini reload

Your app *should* now be running on port 6543.
Did it work? if so, shove this into cron:

# crontab -e
# run it every minute, just to make sure it's running.
# m   h   dom  mon  dow   command
  *   *   *    *    *    /opt/cam/axis-pics/venv-axis/bin/pserve /opt/cam/axis-pics/axis-pics/production.ini > /dev/null 2>&1

It's rude, but it works.

Configure your AXIS camera
==============================
I'll assume you've hacked around with your AXIS camera and
figured out how to set up the password, IP address, and date/time.
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

I've done either a timer or using Motion Detection.
You'll have to create a "Motion Detection" window
under [Events > Motion Detection] first if you want
to play with that option.

Also, I'm lazy and letting the camera define the file names.
So make sure you set the date/time correctly on your cameras.


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

