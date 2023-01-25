#!/bin/bash
fswatch -o /Users/s/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/Genesis/01-99_Personal/30-49_Projects-Personal/40-blog/_posts/ \
| xargs -n1 -I{} /Users/s/local/miniconda3/envs/dev/bin/python ./convert.py