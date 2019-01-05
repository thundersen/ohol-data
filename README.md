# ohol-data

This code can be used to analyze Life Log files from the online game [One Hour One Life](https://onehouronelife.com/).

Here's some basic guidance. More may be added later, but for now I assume that you have some experience in using Python and a working environment on your computer.

Usage:
- Install requirements with `pip install -r requirements.txt` 
- Download data using the script `download_lifelogs.py`. Parameters for servers and time range can be set through constants at the top of that file.
- Run a script under `./plotting`. Take care to set the parameters in that script so that they match the data you downloaded. This should produce a html file containing a graph that will open up in the browser.
