# import-by-date

This is a tool I made in order to move pictures one by one to my Android phone. When I got a new phone I realized that I needed to restore my photos from Google Photos back to my phone in order to send pictures in 3rd party apps like Snapchat or Instagram. There is no easy way to do this as there is no download all from Google Photos.

I first used Google Takeout to download all of my Google Photos. When I moved all the photos over to my phone they were all out of order as Androids either sort by date created or date added, I'm not sure. Either way this means that I need to move my photos in order to my phone. I wrote this script to do that. However there is another problem, the photos from Takeout had the metadata put in another file with each picture, really stupid. So I had to use [this project](https://github.com/mattwilson1024/google-photos-exif) in order to combine the metadata back into the files.

Another issue is that Android devices connect as an MTP device and not a mass storage device so I can't move a file as I would any other file on a letter drive. After some digging the only solution I found was to host an FTP server on my phone using Solid Explorer and then connect to that using a python library.

PAIN IN THE ASS

Just kidding apparently there is ADB transfer...
