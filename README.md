
# Intro

This is a minimal script to convert markdown files created in Obsidian to ready-to-build markdown files for Jekyll (in particular using the Chirpy theme).  

In particular it converts _image_ wikilinks (`[[]]`) to markdown-style (`[]()`) and copies all of the images referenced in the markdown to the destination jekyll site directory. 

(!) - It does _not_ support linking to other posts at the moment (e.g.  `[[other post]]` → `[other post](other post.md)`)

Features Summary
- [x] converts  `![[image.png]]` to `![image](image.png)` =
- [x] as above, but for relative or full paths in either markdown or wikilink style (e.g. `![[/long/path/to/image.png]]` or `![alt-text](/long/path/to/image.png)`) 
- [x] supports in-line width resizing (e.g. `![[image | 300]]` → `{: width="300"}`)
- [x] finds and copies images used in markdown to the user-defined jekyll attachment folder

**Not** Supported Yet
- [ ] links to other posts (e.g. `[[other post]]` → `[Name of Link]({% post_url 2010-07-21-name-of-post %})`) 
- [ ] use of aliases (`[[post | alias ]]`)
- [ ] links to pdfs or csvs
- [ ] admonitions (`> [!INFO]` → `{: .prompt-info}`)
- [ ] auto generating correct page names without date given (e.g. "Example Post.md" → "YYYY-MM-DD-example-post.md")

This script assumes that we are using a specific folder holding all the markdown files that we want to pubish to our Jekyll blog. It does not traverse the whole vault, nor is it selective about which files to convert.

## Script Setup

It doesn't matter where you run the script, but a logfile will be created in the same directory. You can setup and run the `watch.sh` file to automatically run the script when files are changed (uses `fswatch` on macOS).

Setup your paths in `convert.py`.

**Example Tree**
```
.
├── Obsidian-Vault (SRC_BASE)
│   ├── attachments (SRC_IMG)
│   └── posts (SRC_POSTS)
│       └── 2001-01-01-example-post.md
└── Jekyll-Site (DEST_BASE)
    ├── _posts (DEST_POSTS)
    └── assets
        └── img (DEST_IMG)
```

Script Files

**Jekyll Site Paths**:
`DEST_BASE`: Jekyll site root directory
`DEST_POSTS`: Where the markdown pages ("posts") should be copied to. Default `DEST_BASE/_posts`
`DEST_IMG`: Where the images should be copied to. Default `DEST_BASE/assets/img`

> Note: `DEST_IMG` should match the YAML front matter `img:` path 

**Source Markdown Paths**:
`SRC_BASE`: Path to your Obsidian Vault
`SRC_SUBDIR_POSTS`: Directory holding source markdown files, relative to `SRC_BASE`
`SRC_SUBDIR_IMG`: Path relative to `SRC_BASE` that attachments are stored in.

## Writing Posts

### Jekyll Frontmatter

The frontmatter is just copied from our source markdown to the destination markdown. Currently there are no changes.

So we must follow the jekyll frontmatter requirements.

Caution: When indenting use two spaces instead of one tab. For example when assigning a banner image (note the valid white space in `  path:`)

Valid:
```
img: 
  path: assets/img/banner.png
```

Invalid:
```
img:
    path: assets/img/banner.png
```


## Markdown Compatability Guide

These are just some of my notes on markdown compatibility. It is not comprehensive.

### Jekyll Specific
- We can add classes onto the preceding block/paragraph/etc by adding a line with `{: .<classes> #<tags> <html_element>=<value>} 


### General Compatibility

Bold/Italitcs in the middle of a word
- bold/emphasis: use double asterisks in the middle of a word for bold (e.g. `I**am**bold`)
- italics: use single underscores (`I_am_italics`)
- bold + italics: use three asterisks (`I***am***both`)

Blockquotes
- put blank lines before and after
 