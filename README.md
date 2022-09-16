# x-plane-coordinates-server

This Python script can be run on the same system as x-plane, and will stand-up a server that outputs the same co-ordinates that the `FSWebService` component of <https://github.com/MoMadenU/msfs2020-skyvector> returns.

That enables you to use the same Chrome Extension `SkyVectorMovingMap` provided by <https://github.com/MoMadenU/msfs2020-skyvector> to display your X-Plane position on the SkyVector website.

## Instructions

### On your X-Plane computer

```bash
./serve_xplane_coordinates.py
```

Expected output:

```
No coords seen in a while, re-registering with x-plane...
... (above repeats until a flight starts, and X-Plane begins sending coordinates)
Received: {'coordinates': [-37.00676039135794, 174.80528696817325]}
... (above is updated once per second)
```

To verify it's running:

```bash
curl http://localhost:8001
```

Expected output:

```json
{"coordinates": [-37.00676039131409, 174.80528696817325]}
```

### On your computer to show the moving map

I wanted to display the SkyVector map on a separate ChromeOS laptop I have. To do this, I did the following from my Mac workstation:

1. I downloaded the released ZIP file for the Chrome Extension from: <https://github.com/MoMadenU/msfs2020-skyvector/releases/tag/v003>
2. I edited `SkyVectorMovingMap/moving-map-content.js` to change the reference to `localhost` to the IP address of my X-Plane computer (`192.168.x.y` on my LAN)
3. (skip if not using ChromeOS) I uploaded that entire directory (`SkyVectorMovingMap`) to my Google Drive.

Now, on my ChromeOS laptop (or whichever computer):

1. Go to `chrome://extensions/` in Chrome
2. Enable developer mode (toggle on right)
3. Click `Load unpacked` button on left
4. Select the `SkyVectorMovingMap` directory (in ChromeOS, it let me select a directory in Google Drive)
5. Visit <https://skyvector.com/> - and you should see your position displayed

NOTE: if you are using a different computer (not `localhost`) to show the moving map, you will need to consider doing the following:

1. Click the "Pad-lock" icon in the URL bar to the left of `skyvector.com`.
2. Click `Site settings` in the menu
3. Scroll to `Insecure content`
4. Select `Allow`
5. Refresh <https://www.skyvector.com>

This is necessary because Chrome (rightly) regards the call to your coordinates server as not secure.

If you use SkyVector for real things, then you probably shouldn't do the above.

## Credits

Thanks to `MoMadenU` for this useful extension! It was fun getting this to work with X-Plane.
