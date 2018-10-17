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
1. Go to [Flickr Apps page](https://www.flickr.com/services/api/keys),  create a new set of keys.
2. Choose **APPLY FOR A NON-COMMERCIAL KEY** and enter appropriate info.
3. Copy the **Key** and **Secret**
4. Set the key and secret in the **FLICKR_API_KEY** and **FLICKR_API_SECRET** environment variables respectively. A linux example is shown below.
    ```
    export FLICKR_API_KEY=<KEY>`
    export FLICKR_API_SECRET=<SECRET>
    ```
5. *flickr-downloader.py* is ready to be used
    ```
    python flickr-downloader.py -h
    usage: flickr-downloader.py [-h] [--api-key API_KEY] [--api-secret API_SECRET]
                                [--verbose]
                                {login,logout,download} ...
    
    Download Photos from a flickr account.
    
    positional arguments:
      {login,logout,download}
                            Available commands
        login               Login to flickr (optional).
        logout              Logout. Clear existing login tokens.
        download            Download photos from flickr.
    
    optional arguments:
      -h, --help            show this help message and exit
      --api-key API_KEY, -k API_KEY
                            Flickr API access key.
      --api-secret API_SECRET, -s API_SECRET
                            Flickr API access secret.
      --verbose, -v         Verbosity. For increased verbosity use -vv, -vv, -vvv.
    ```
6. (Optional) Authorize access to flickr account if you need to download content that is not public. Use the *login* command as shown below
    ```
    $ python flickr-downloader.py login
    Login auth tokens not found. Generating new login tokens.
    
    Authorization URL: https://www.flickr.com/services/oauth/authorize?oauth_token=72157702330694904-63a45bdd5146c035&perms=read
    
    Navigate to above URL, login and authorize access to the
    flickr account. On successful authorization you will be
    redirected to an xml page. Note down the <oauth_token> and
    <oauth_verifier> from this page, you will need this info
    to login.
    
    Enter the OAuth Verifier: <paste/type the oauth verifier here and hit enter/return-key>
    Login tokens successfull created.
    ```
## Downloading Photos
Photos from a flickr account can be downloaded using the *download* command. You will need the *Email Id* tied to the flickr account from which you would like to download the photos. If you want to download non-public photos you will need to have authorized access to the flickr account as shown above. The largest sized photos will always be downloaded.
    
Three options are available for donwloading photos.
1. Download all photos from the flickr account.
2. Download photos from a specified albums in the flickr account.
3. Download all albums from the flickr account. If there are photos that are not in any albums then these photos will not be downloaded. If there are photos that are part of multiple albums then these photos will be downloaded multiple times.

```
$ python flickr-downloader.py download -h
usage: flickr-downloader.py download [-h] [--location LOCATION] --flickr-email
                                     FLICKR_EMAIL
                                     (--all | --album ALBUM | --all-albums)
                                     [--dry-run]

optional arguments:
  -h, --help            show this help message and exit
  --location LOCATION, -l LOCATION
                        Location to which photos will be downloaded. Default
                        is the current working directory.
  --flickr-email FLICKR_EMAIL, -e FLICKR_EMAIL
                        Email id of the flickr account from which photos need
                        to be downloaded. To download photos that are not
                        public, authtoken should be generated and saved for
                        this flickr account. Use the login command to do so.
  --all, -a             Donwload all photos.
  --album ALBUM, -m ALBUM
                        Download photos from specified album.
  --all-albums, -b      Download all albums. Photos that not part of any
                        albums will not be downloaded. Photos part of multiple
                        albums will be duplicated accordingly.
  --dry-run, -d         Do not download files to disk. Use this option to
                        verify the content to be downloaded is correct.
```

## Gotchas
1. The tool has not be tested on Windows but is expected to work. Happy to fix issues if reported.
2. Downloaded files are placed in a directory/folder whose name is derived from the flickr account's display name (flickr calls this username in the Flickr APIs), which may contain spaces or special characters. If the display name contains special characters then *flickr-downloader* may run into issues. Hoping to take care of this soon.

## Disclaimer
This product uses the Flickr API but is not endorsed or certified by SmugMug, Inc.
