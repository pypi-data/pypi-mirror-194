# umbraSnscrpe
umbraSnscrpe is a scraper for social networking services (SNS). It scrapes things like user profiles, hashtags, or searches and returns the discovered items, e.g. the relevant posts.

The following services are currently supported:

* Facebook: user profiles, groups, and communities (aka visitor posts)
* Instagram: user profiles, hashtags, and locations
* Mastodon: user profiles and toots (single or thread)
* Reddit: users, subreddits, and searches (via Pushshift)
* Telegram: channels
* Twitter: users, user profiles, hashtags, searches, tweets (single or surrounding thread), list posts, and trends
* VKontakte: user profiles
* Weibo (Sina Weibo): user profiles

## Requirements
umbraSnscrpe requires Python 3.8 or higher. The Python package dependencies are installed automatically when you install umbraSnscrpe.

Note that one of the dependencies, lxml, also requires libxml2 and libxslt to be installed.

## Usage
### CLI
The generic syntax of umbraSnscrpe's CLI is:

    umbraSnscrpe [GLOBAL-OPTIONS] SCRAPER-NAME [SCRAPER-OPTIONS] [SCRAPER-ARGUMENTS...]

`umbraSnscrpe --help` and `umbraSnscrpe SCRAPER-NAME --help` provide details on the options and arguments. `umbraSnscrpe --help` also lists all available scrapers.

The default output of the CLI is the URL of each result.

Some noteworthy global options are:

* `--jsonl` to get output as JSONL. This includes all information extracted by umbraSnscrpe (e.g. message content, datetime, images; details vary by scraper).
* `--max-results NUMBER` to only return the first `NUMBER` results.
* `--with-entity` to get an item on the entity being scraped, e.g. the user or channel. This is not supported on all scrapers. (You can use this together with `--max-results 0` to only fetch the entity info.)

#### Examples
Collect all tweets by Jason Scott (@textfiles):

    umbraSnscrpe twitter-user textfiles

It's usually useful to redirect the output to a file for further processing, e.g. in bash using the filename `twitter-@textfiles`:

```bash
umbraSnscrpe twitter-user textfiles >twitter-@textfiles
```

To get the latest 100 tweets with the hashtag #archiveteam:

    umbraSnscrpe --max-results 100 twitter-hashtag archiveteam

### Library
It is also possible to use umbraSnscrpe as a library in Python, but this is currently undocumented.

## Issue reporting
If you discover an issue with umbraSnscrpe, please report it at <https://github.com/JustAnotherArchivist/umbraSnscrpe/issues>. If possible please run umbraSnscrpe with `-vv` and `--dump-locals` and include the log output as well as the dump files referenced in the log in the issue. Note that the files may contain sensitive information in some cases and could potentially be used to identify you (e.g. if the service includes your IP address in its response). If you prefer to arrange a file transfer privately, just mention that in the issue.

## License
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.
