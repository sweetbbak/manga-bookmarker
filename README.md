# manga-bookmarker
## a tool to dump manga from your browser history

## Usage
```bash
$ bookmarker -b -u
```

This is a huge WIP and needs to be refactored and improved.
The general idea is to use the bookmarker to dump manga from your browser history.
I often forget what I have read and recently had a website with a bookmarking capability 
remove every single account, losing 2 years worth of bookmarks. I found that the best
way to find all of those bookmarks was to dig through my search history and find the 
things that I have read and where I've left off.

This tool just dumps your history and matches them by domain names of your favorite reading
sites and then organizes them by removing duplicates, grouping them together, removing garbage links
and then dumping them into a json file. This way, you always have your relevant reading history on hand.

This optionally uses FZF and/or Gum to select a manga and open it in a browser. I want to connect this to 
the OpenWith extension so that I can use it from the browser to update my reading history.
