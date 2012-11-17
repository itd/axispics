axis-pics README
=================

This captures a series of images from one or
more AXIS cameras, and saves then to a specified
directory ($axis_pic_path).

Images from each camera are saved to
$axis_pic_path/$CAMERA_IP_ADDRESS, e.g.,
/path/to/images/192.168.0.102

* Edit the value for "axis_pic_path" in both
  the production.ini and development.ini files.

* Make sure your <axis_pic_path> exists.

* Fire up your Pyramid app.


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




