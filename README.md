# meme-mosaic

Makes a meme out of memes.

Given an image to use as a tile

<img src="/images/tile.jpg" width="200">
 
And an image to fill

<img src="/images/meme.jpg" width="200">

It extracts the pixel values of the larger fill image to tint tile images and uses that to re-create the fill image.

<img src="/images/output.jpg" width="800">

Zooming in on that created image you can see the tile image.

<img src="/images/zoomed_in_1.png" width="200">

<img src="/images/zoomed_in_2.png" width="200">

# Running it

You need `python3` and `Pillow` installed, running it in PyCharm runs it in a virtual environemnt (which has everything insallted) `dowload_path/venv`, you can also run it on command line `python3 dowload_path/meme-moasic/memify.py`.

# Things I need to do

1. Feed image paths by cmd line args.
2. Turn it into a REST API (venv will be great for this).
