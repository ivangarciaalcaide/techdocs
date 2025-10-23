#!/bin/bash

export MKDOCS_WATCH_MODE=poll
mkdocs build --clean
mkdocs serve  --livereload --watch-theme -a 127.0.0.1:8080
