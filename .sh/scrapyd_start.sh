#!/bin/bash
EGGS_DIR=eggs
SPIDER_PROJECT_DIR=src/Services/crawler
# if [[ ! ${SERVICE_DIR+x} ]]; then
#     echo "envrionment variable SPIDER_APP_DIR is unset."
#     exit 1
# fi

# clean old stuffs
cd $SPIDER_PROJECT_DIR || exit 1

if [ -d "$EGGS_DIR" ]; then
    rm -r $EGGS_DIR/$p
fi

SPIDER_PROJECTS=$(python get_deployable_project.py)
for p in $SPIDER_PROJECTS;
    do
        mkdir -p $EGGS_DIR/$p
        scrapyd-deploy --build-egg $EGGS_DIR/$p/$(date +%s).egg
    done

scrapyd
