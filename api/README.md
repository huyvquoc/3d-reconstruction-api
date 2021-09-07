# Web API

There are 3 app files:

- ```app.py```: a full API with progress for 3D reconstruction displayed directly on the web page. It has 2 buttons: "Download output file" and "Reconstruct another 3D model".
- ```app_noprogress.py```: an API which returns the output zip file to download after the reconstruction completes (this condition is required by ShadesOfThings) and shows no progress on the web page.
- ```app_sot.py```: a modified version of ```app_noprogress.py``` which is succesfully used on the machine of ShadesOfThings. There are some small modifications for suitable with their settings.
- ```app_multi.py``` (works along with folder ```proj3d```): an API that runs 3D reconstruction processes as background jobs.