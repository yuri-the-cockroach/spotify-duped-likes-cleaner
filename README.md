# Spotify duped likes cleaner

### What?
This is a utility that will find duplicated songs in your spotify saved playlist and remove them if you choose to do so.

### Why?
Because spotify is too stupid to recognize that they're the same fucking song

### How?
There's an identifier that is called ISRC. It is a legal identifier that is given to each legally distinct song. Thus it is almost perfect for this purpose. We basically get an ISRC id for each song, see if there's more than one match for each ISRC, check that they have the same authors and title, and if all of the above it true, take the more recent addition and delete it from liked songs. Just in case it also makes a backup into a json file for all the songs it deletes.

### The rant
This script was written in like 3 hours. There's no good reason why spotify can't handle this properly. This've been a well known issue for years now and I have no idea why they can't make a random junior fix it in a day... But hey, at least we have useless shows in our music player

## To run this:
1. clone this repo where-ever you want
2. cd into it
3. create an env via `python -m venv env`
4. source the appropriate activate file, i.e. `source env/bin/activate` for bash/zsh or whatever else you use (weirdo)
5. Create an app in [spotify dashboard](https://developer.spotify.com/dashboard)
6. Get it's client id and secret and put them into `CLID` and `SECRET` environment variables respectively
7. Install the requirements via `pip install -r requirements.txt`
8. Run the script via `make` or by hand via `python main.py` and follow it's instructions...
9. ...
10. Profit!

If something went wrong and you want to revert the deletion, pleaes refer to [temp.py](./temp.py) file, but keep in mind that you WILL have to alter it to your requirements.

For any modifications please refer to [the license](./LICENSE.md)
