#!/bin/bash

ps aux | fgrep tools.py | fgrep python | fgrep -v fgrep | awk '{print $2}' | xargs kill -9
