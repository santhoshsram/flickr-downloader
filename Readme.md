# flickr-downloader
A simple python script that uses the Flickr APIs (through the [flickr_api](https://github.com/alexis-mignon/python-flickr-api) python SDK) to bulk download photos from Flickr.

## Requirements
1. Python 2.7.10 or above. Tested on Python 2.7.10. Should work with Python 3 as well.
2. flick_api Python module. Can be installed from pip.

## Getting Started
After cloning this git repo or downloading the python file follow below steps to get started.

### 1. Install flickr_api module
```pip install flickr_api```

### 2. Get Flickr API access key and secret
1. Go to [Flickr Apps page](https://www.flickr.com/services/api/keys) create a new set of keys.
2. Choose **APPLY FOR A NON-COMMERCIAL KEY** and enter appropriate info.
3. Copy the **Key** and **Secret**
4. Set the key and secret in the **FLICKR_API_KEY** and **FLICKR_API_SECRET** environment variables respectively. A linux example is shown below.
    ```
    export FLICKR_API_KEY=<KEY>`
    export FLICKR_API_SECRET=<SECRET>
    ```
