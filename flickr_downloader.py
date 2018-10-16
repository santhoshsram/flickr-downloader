##
## App Name: flickr-downloader
## This product uses the Flickr API but is not endorsed or certified by SmugMug, Inc.
##

import flickr_api
import os
import argparse
import time
import sys


##
## Define Verbosity Levels
##
VERBOSE_HIGHEST = 0
VERBOSE_HIGH    = 1
VERBOSE_MEDIUM  = 2
VERBOSE_LOW     = 3

##
## Global Configs
##
config = {}
config['AUTH_TOKEN_FILE'] = os.path.join(os.path.expanduser("~"),
                                         ".flickroauthtoken")
config['VERBOSITY_THRESHOLD'] = VERBOSE_HIGHEST


##
## SetVerbosity(verbosity)
##
## Description
##      Sets the verbosity of the output messages
##
## Inputs
##      - verbosity
##          Description: Verbosity level threshold
##          Type: Integer
##
def SetVerbosity(verbosity):
    verbosity = min(verbosity, VERBOSE_LOW)
    config['VERBOSITY_THRESHOLD'] = verbosity


##
## VerbosePrint(level, *msgs)
##
## Description
##      Print messages based on current verbosity threshold
##
## Inputs
##      - level
##          Description: The verbosity level of the message. Message
##                       will be logged if level is less than or equal
##                       to verbosity threshold
##          Type: Integer
##      - *msgs
##          Description: Messages to be printed.
##          Type: Tuple of strings
##
def VerbosePrint(level, *msgs):
    threshold = config['VERBOSITY_THRESHOLD']
    if level <= threshold:
        for msg in msgs:
            print msg,
        print


##
## ParseCommandLineArgs()
##
## Description
##      Command handler for the download subcommand. Calls the appropriate
##      helper Download* helper function
##
## Output
##      - cmd_args
##          Description: Parsed command line arguments
##          Type: Namespace object containing all parsed arguments.
##
def ParseCommandLineArgs():
    # Create the root parser
    root_parser = argparse.ArgumentParser(description="Download Photos from a flickr account.")
    root_parser.add_argument('--api-key', '-k', help='Flickr API access key.')
    root_parser.add_argument('--api-secret', '-s', help='Flickr API access secret.')
    root_parser.add_argument('--verbose', '-v', default=0, action='count',
                             help='Verbosity. For increased verbosity use -vv, -vv, -vvv.')
    subparsers = root_parser.add_subparsers(dest="cmd", help='Available commands')

    # Create a sub parser for creating login tokens
    login_parser = subparsers.add_parser('login', help='Login to flickr (optional).')
    login_parser.add_argument('--overwrite', '-o', action='store_true',
                              help='Overwrite existing login tokens.')
    login_parser.add_argument('--auth-token', '-n', help='Flickr account access OAuth token.')
    login_parser.add_argument('--auth-secret', '-t', help='Flickr account access OAuth secret.')

    # Create sub parser for removing login tokens (logout)
    logout_parser = subparsers.add_parser('logout', help='Logout. Clear existing login tokens.')

    # Create a sub parser for downloading
    dl_parser = subparsers.add_parser('download', help='Download photos from flickr.')
    dl_parser.add_argument('--location', '-l',
                           help='Location to which photos will be downloaded.  '+
                                'Default is the current working directory.')
    dl_parser.add_argument('--flickr-email', '-e', required=True,
                           help='Email id of the flickr account from which photos need to be ' +
                                'downloaded. To download photos that are not public, authtoken ' +
                                'should be generated and saved for this flickr account. ' +
                                'Use the login command to do so.')
    dl_group = dl_parser.add_mutually_exclusive_group(required=True)
    dl_group.add_argument('--all', '-a', action='store_true', help='Donwload all photos.')
    dl_group.add_argument('--album', '-m', help='Download photos from specified album.')
    dl_group.add_argument('--all-albums', '-b', action='store_true',
                          help='Download all albums. Photos that not part of any albums will '+
                               'not be downloaded. Photos part of multiple albums will be '+
                               'duplicated accordingly.')
    dl_parser.add_argument('--dry-run', '-d', action='store_true',
                           help='Do not download files to disk. Use this option to verify the ' +
                                'content to be downloaded is correct.')

    cmd_args = root_parser.parse_args()
    if VERBOSE_LOW <= cmd_args.verbose:
        print("Command Line Arguments: %s" % str(cmd_args))
    return cmd_args


##
## IsPython3OrMore()
##
## Description
##      Checks if current python version is 3.0 or greater.
##
## Return Values
##      True: If current python version is 3.0 or greater
##      False: If current python version is less than 3.0
##
def IsPython3OrMore():
    python3 = (3,0)
    python_cur_ver = sys.version_info

    VerbosePrint(VERBOSE_LOW, "Working with python version %s.%s.%s" %
                              sys.version_info[:3])
    if python_cur_ver >= python3:
        return True
    else:
        return False

##
## SetAPIKeys(api_key, api_secret, auth_token_file)
##
## Description
##      Set the API keys and the OAuth token (optional) to access flickr.
##      If OAuth token is not set, only public content can be accessed.
##
## Inputs
##      - api_key
##          Description: API key to access Flickr APIs
##          Type: String
##      - album
##          Description: API secret to access Flickr APIs
##          Type: String
##
def SetAPIKeys(api_key, api_secret):

    if api_key is None:
        if os.environ.has_key("FLICKR_API_KEY"):
            VerbosePrint(VERBOSE_MEDIUM,
                         "API Key found from env var FLICKR_API_KEY: %s" %
                         os.environ['FLICKR_API_KEY'])
            api_key = os.environ['FLICKR_API_KEY']
        else:
            VerbosePrint(VERBOSE_HIGHEST,
                         "Flickr API Key is not available. Either pass it as " +
                         "an argument or set it in the FLICKR_API_KEY env var.")
            exit(1)

    if api_secret is None:
        if os.environ.has_key("FLICKR_API_SECRET"):
            VerbosePrint(VERBOSE_MEDIUM,
                         "API Secret found from env var FLICKR_API_SECRET: %s" %
                         os.environ['FLICKR_API_SECRET'])
            api_secret = os.environ['FLICKR_API_SECRET']
        else:
            VerbosePrint(VERBOSE_HIGHEST,
                         "Flickr API Secret is not available. Either pass it as "+
                         "an argument or set it in the FLICKR_API_SECRET env var.")
            exit(1)

    flickr_api.set_keys(api_key = api_key, api_secret = api_secret)


##
## SetAuthKeys()
##
## Description
##      Set the flickr account oauth tokens if the token token
##      file exists.
##
def SetAuthKeys():
    auth_token_file = config['AUTH_TOKEN_FILE']

    if os.path.isfile(auth_token_file):
        VerbosePrint(VERBOSE_MEDIUM,
                     "Fetching auth tokens from file: %s" % auth_token_file)
        flickr_api.set_auth_handler(auth_token_file)
    else:
        VerbosePrint(VERBOSE_HIGHEST,
                     "\nWarning: OAuth token file not created. You will proceed\n" +
                     "without login and will not be able to download any private\n" +
                     "content that requires login.\n")


##
## CreateLocation(location, dry_run)
##
## Description
##      Create the directory / folder specified by location on
##      the filesystem, with appropriate exception handling.
##
## Inputs
##      - location
##          Description: Directory/folder to create
##          Type: String
##      - dry_run
##          Description: Don't create the directory / folder if this
##                       is set to True
##          Type: Boolean
##
def CreateLocation(location, dry_run):
    if dry_run == False:
        try:
            os.makedirs(location)
        except OSError as err:
            VerbosePrint(VERBOSE_HIGHEST, "Error: Failed to create folder %s" %
                         location)
            exit(1)

    VerbosePrint(VERBOSE_LOW, "Created folder %s" % location)

##
## WritePhotos2Disk(photos, location, dry_run)
##
## Description
##      Write the photos to disk at the specified location.
##
## Inputs
##      - photos
##          Description: The photos to be written to disk
##          Type: Array of flickr_api.Photo
##      - location
##          Description: Directory/folder to write photo to
##          Type: String
##      - dry_run
##          Description: Flag to turn off real download. Only loop through all
##                       available photos.
##          Type: Boolean
##
def WritePhotos2Disk(photos, location, dry_run):
    for photo in photos:
        ##
        ## Let's get the photo file's extention and append
        ## it to the photo id to make the file name.
        ##
        ## getPhotoFile() returns the full URL of the file
        ## along with the extension, but the file name looks
        ## ugly! So let's just get the extension by splitting
        ## the URL by '.' and then getting the last piece of
        ## this split.
        ##
        ext = '.' + photo.getPhotoFile().split('.')[-1]
        abs_file_path = os.path.join(location, photo.id)
        VerbosePrint(VERBOSE_HIGH,
                     "Downloading photo %s..." % (abs_file_path + ext))
        
        if dry_run == False:
            photo.save(abs_file_path)


##
## DownloadAlbum(user, album, location, dry_run)
##
## Description
##      Download photos from the specified album of the flickr account
##      of user. Download will create a folder for the album at the
##      specified location.
##
## Inputs
##      - user
##          Description: Flickr user whose photos to download
##          Type: flickr_api.Person
##      - album
##          Description: Flickr album of the user from which to download photos
##          Type: String
##      - location
##          Description: Local directory/folder where the photos will be downloaded
##          Type: String
##      - dry_run
##          Description: Flag to turn off real download. Only loop through all
##                       available photos.
##          Type: Boolean
##
def DownloadAlbum(user, album, location, dry_run):
    photosets = user.getPhotosets()
    photoset_pages = photosets.info.pages
    found = False

    for page in range(1, photoset_pages+1):
        photosets = user.getPhotosets(page=page)
        for photoset in photosets:
            if photoset.title == album:
                found = True
                photos = photoset.getPhotos()
                photos_pages = photos.info.pages
                total  = photos.info.total

                location = os.path.join(location, album)
                CreateLocation(location, dry_run)

                VerbosePrint(VERBOSE_HIGHEST,
                            "Downloading album %s (%d photos) to %s" %
                            (album, total, location))

                for page in range(1, photos_pages+1):
                    photos = photoset.getPhotos(page=page)
                    WritePhotos2Disk(photos, location, dry_run)

    if found == False:
        VerbosePrint(VERBOSE_HIGHEST,
                     "Album %s not found." % album)
        exit(1)


##
## DownloadAllAlbums(user, location, dry_run)
##
## Description
##      Download photos from all albums of the flickr account of user.
##      Download will create a folder for each album at the specified location.
##      Photos that are not part of any albums will not be downloaded. Photos
##      part of multiple albums will be duplicated.
##
## Inputs
##      - user
##          Description: Flickr user whose photos to download
##          Type: flickr_api.Person
##      - location
##          Description: Local directory/folder where the photos will be downloaded
##          Type: String
##      - dry_run
##          Description: Flag to turn off real download. Only loop through all
##                       available photos.
##          Type: Boolean
##
def DownloadAllAlbums(user, location, dry_run):
    photosets = user.getPhotosets()
    photoset_pages = photosets.info.pages

    for page in range(1, photoset_pages+1):
        photosets = user.getPhotosets(page=page)
        for photoset in photosets:
            photos = photoset.getPhotos()
            photos_pages = photos.info.pages
            total = photos.info.total

            location = os.path.join(location, photoset.title)
            CreateLocation(location, dry_run)

            VerbosePrint(VERBOSE_HIGHEST,
                         "Downloading album %s (%d photos) to %s" %
                         (photoset.title, total, location))

            for page in range(1, photos_pages+1):
                photos = photoset.getPhotos(page=page)
                WritePhotos2Disk(photos, location, dry_run)


##
## DownloadAll(user, location, dry_run)
##
## Description
##      Download all photos from the flickr account identified by the
##      specified email.
##
## Inputs
##      - user
##          Description: Flickr user whose photos to download
##          Type: flickr_api.Person
##      - location
##          Description: Local directory/folder where the photos will be downloaded
##          Type: String
##      - dry_run
##          Description: Flag to turn off real download. Only loop through all
##                       available photos.
##          Type: Boolean
##
def DownloadAll(user, location, dry_run):
    photos = user.getPhotos()
    pages = photos.info.pages
    total = photos.info.total

    CreateLocation(location, dry_run)

    VerbosePrint(VERBOSE_HIGHEST,
                 "Downloading %d photos to %s" %
                 (total, location))

    for page in range(1, pages+1):
        photos = user.getPhotos(page=page)
        WritePhotos2Disk(photos, location, dry_run)


##
## DownloadCommandHandler(cmd_args)
##
## Description
##      Command handler for the download subcommand. Calls the appropriate
##      helper Download helper function
##
## Inputs
##      - cmd_args
##          Description: Parsed command line arguments to this python script
##          Type: Namespace object containing all parsed arguments.
##
def DownloadCommandHelper(cmd_args):
    flickr_email = cmd_args.flickr_email
    location = cmd_args.location
    
    SetAuthKeys()

    # If location is set, then default to current working directory
    if location is None:
        location = os.getcwd()

    try:
        user = flickr_api.Person.findByEmail(flickr_email)
    except flickr_api.flickrerrors.FlickrAPIError:
        VerbosePrint(VERBOSE_HIGHEST, "Invalid flickr email. User not found.")
        exit(1)

    VerbosePrint(VERBOSE_LOW,
                 "Downloading from flickr account with id: %s, username: %s" %
                 (user.id, user.username))

    # Add path to a new folder (which we will create now) for this download.
    timestamp = time.strftime('%Y%m%d%H%M%S')
    folder_name = user.username.replace(" ", "_") + "_" + timestamp
    location = os.path.join(location, folder_name)

    if cmd_args.all == True:
        DownloadAll(user, location, cmd_args.dry_run)
    elif cmd_args.all_albums == True:
        DownloadAllAlbums(user, location, cmd_args.dry_run)
    elif cmd_args.album is not None:
        DownloadAlbum(user, cmd_args.album, location, cmd_args.dry_run)
    else:
        VerbosePrint(VERBOSE_HIGHEST,
                     "We shouldn't have gotten here. Possible bug in argparse module.")

    VerbosePrint(VERBOSE_HIGHEST, "Done.")


##
## AuthTokens2File(auth_token, auth_secret)
##
## Description
##      Write the login auth tokens to the auth token file.
##
## Inputs
##      - auth_token
##          Description: The auth token/key
##          Type: String
##      - auth_secret
##          Description: The auth secret
##          Type: String
##
def AuthTokens2File(auth_token, auth_secret):
    auth_token_file = config['AUTH_TOKEN_FILE']

    with open(auth_token_file, "w") as fh:
        fh.write("\n".join([auth_token, auth_secret]))


##
## LoginHandler()
##
## Description
##      Command handler for login subcommand. If the OAuth tokens are
##      specified either in the environment variables or through command
##      line argument, set it in the auth token file. Else generate new
##      token and save it in the auth token file.
##
def LoginHandler(auth_token, auth_secret, overwrite):
    auth_token_file = config['AUTH_TOKEN_FILE']

    if os.path.isfile(auth_token_file):
        if overwrite == False:
            VerbosePrint(VERBOSE_HIGHEST,
                         "Login auth token already exists. To overwrite existing auth "+
                         "token, use --overwrite option.")
            exit(0)

    if auth_token is None:
        if os.environ.has_key("FLICKR_AUTH_TOKEN"):
            VerbosePrint(VERBOSE_MEDIUM,
                    "AUTH Key found from env var FLICKR_AUTH_TOKEN: %s" %
                    os.environ['FLICKR_AUTH_TOKEN'])
            auth_token = os.environ['FLICKR_AUTH_TOKEN']

    if auth_secret is None:
        if os.environ.has_key("FLICKR_AUTH_SECRET"):
            VerbosePrint(VERBOSE_MEDIUM,
                         "AUTH Secret found from env var FLICKR_AUTH_SECRET: %s" %
                         os.environ['FLICKR_AUTH_SECRET'])
            auth_secret = os.environ['FLICKR_AUTH_SECRET']

    if (auth_token is None) or (auth_secret is None):
        VerbosePrint(VERBOSE_HIGHEST,
                     "Login auth tokens not found. Generating new login tokens.")

        ah = flickr_api.auth.AuthHandler()
        auth_url = ah.get_authorization_url("read")
        VerbosePrint(VERBOSE_HIGHEST, "\nAuthorization URL: %s\n" % auth_url)
        VerbosePrint(VERBOSE_HIGHEST,
                     "Navigate to above URL, login and authorize access to the\n" +
                     "flickr account. On successful authorization you will be\n" +
                     "redirected to an xml page. Note down the <oauth_token> and\n" +
                     "<oauth_verifier> from this page, you will need this info\n" +
                     "to login.\n")

        oauth_verifier = ""
        if IsPython3OrMore():
            oauth_verifier = input("Enter the OAuth Verifier: ")
        else:
            oauth_verifier = raw_input("Enter the OAuth Verifier: ")

        VerbosePrint(VERBOSE_LOW, "OAuth Verifier: %s" % oauth_verifier)

        if not oauth_verifier:
            VerbosePrint(VERBOSE_HIGHEST, "Fatal version check error. Bye.")
            exit(1)

        ah.set_verifier(oauth_verifier)
        flickr_api.set_auth_handler(ah)
        ah.save(auth_token_file)
    else:
        AuthTokens2File(auth_token, auth_secret)

    VerbosePrint(VERBOSE_HIGHEST, "Login tokens successfull created.")


##
## LogoutHandler()
##
## Description
##      Command handler for logout subcommand. Removes login oauth
##      tokens, if they exist
##
def LogoutHandler():
    auth_token_file = config['AUTH_TOKEN_FILE']

    if os.path.isfile(auth_token_file):
        os.remove(auth_token_file)
        VerbosePrint(VERBOSE_HIGHEST, "Logout successful. Auth tokens removed.")
    else:
        VerbosePrint(VERBOSE_HIGHEST, "No auth tokens found. Logout not required.")


##
## Main
##
cmd_args = ParseCommandLineArgs()
SetVerbosity(cmd_args.verbose)
SetAPIKeys(cmd_args.api_key, cmd_args.api_secret)

if cmd_args.cmd == "download":
    DownloadCommandHelper(cmd_args)
    exit(0)
elif cmd_args.cmd == "login":
    LoginHandler(cmd_args.auth_token, cmd_args.auth_secret, cmd_args.overwrite)
    exit(0)
elif cmd_args.cmd == "logout":
    LogoutHandler()
    exit(0)

exit(0)
