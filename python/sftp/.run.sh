#!/bin/bash

set -ex

bin/qgtunnel python app.py
cat readme.txt
