#!/bin/bash
thera -s css
thera mypage.md -t templates/main.html -c demo.yaml
thera -b blog/*.md -t templates/blog.html -c demo.yaml
