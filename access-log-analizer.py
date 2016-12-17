#!/usr/bin/python

import sys
import os
import glob



if __name__ == "__main__":
	for strFile in glob.glob("logs/*.log*"):
		print strFile



