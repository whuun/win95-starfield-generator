# Windows 95 Starfield Screensaver Perfect Loop Generator
This is python script that I wrote, that generates perfect loops of Windows 95 Starfield Screensaver. 
Maybe it's not most performant nor best looking code, but it works good (at least @1920x1080).

Example (config: 1920x1080@30 10 sec, downscaled in ffmpeg):
![bruh](https://github.com/user-attachments/assets/fa18a9a7-2e99-4a01-a5e2-16127b680f8e)


# How to use
You can change constants in `main.py` file, such as amount of stars: `STARS_AMOUNT`, warp speed: `SPEED` and other stuff, you'll understand what do what.
**And then just run the file.**

All requirements you can find, in `requirements.txt`, but its just **opencv** and **numpy**.

I wanted to turn it to `.webp` automatically, but some bastards realy can't accept superiority of WebP, so I left it raw (in .avi), as opencv give it to us.

But if you really want, you can convert it in any format you like with ffmpeg:
```
ffmpeg -i output.avi -q:v 100 out.webm
```
Note: FFmpeg for some reason do 100 the best quality for WebP, while for other 100 is worst and 0 is best. Also, it wouldn't show you progress on completing the ecoding of WebP, but it still do it. At least on my current version (n7.1).

PRO TIP: If you want to make wallpaper out of it (like me), you don't really need to do 1920x1080@240 60 seconds long, 1920x1080@30 for 10 seconds will do.
