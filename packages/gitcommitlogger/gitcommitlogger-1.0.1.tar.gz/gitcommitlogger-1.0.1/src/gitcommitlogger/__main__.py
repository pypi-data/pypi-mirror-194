#!/usr/bin/env python 

import os
import subprocess
import re
import json
import logging
import logging.handlers
import argparse
from datetime import datetime
import pytz
import requests

def setup_logging(logfile):
  '''
  Setup logging to a file.
  @param logfile: The path to the log file.
  @return: The logger object.
  '''
  # delete any existing file
  if os.path.exists(logfile):
    os.remove(logfile)
  # Setup logging
  logger = logging.getLogger('log_commits')
  logger.setLevel(logging.DEBUG)
  # log to stdout
  # ch = logging.StreamHandler()
  # logger.addHandler(ch)
  # log to file
  fh = logging.handlers.RotatingFileHandler(logfile, maxBytes=1000000, backupCount=5)
  fh.setLevel(logging.DEBUG)
  logger.addHandler(fh)    
  return logger

def get_exclusions(filename):
  '''
  Get a list of files to exclude from analysis.
  @param filename: The path to the file containing the list of files to exclude.
  @return: A list of files to exclude.
  '''
  with open(filename) as file:
    lines = [line.strip() for line in file]
    return lines

def get_args():
  '''
  Parse command-line arguments.
  @return: The parsed arguments.
  '''

  # default files to exclude from analysis
  current_dir = os.path.dirname(os.path.realpath(__file__)) # the current directory
  exclusion_file = os.path.join(current_dir, '.logsignore')
  exclusions = get_exclusions(exclusion_file)

  # parse command-line arguments
  parser = argparse.ArgumentParser()
  parser.add_argument("-i", "--inputfile", help="filename of JSON array of commits (typically saved from GitHub Action context variable, github.event.commits)", default='', required=True)
  parser.add_argument("-o", "--outputfile", help="filename where to store the CSV output with git stats for each commit", default='', required=True)
  parser.add_argument("-u", "--url", help="The URL of the web app where the commit stats should be sent.", default='')
  parser.add_argument("-x", "--exclusions", help='A comma-separated string of files to exclude, e.g. --excusions "foo.zip, *.jpg, *.json" ', default=','.join(exclusions))
  parser.add_argument("-v", "--verbose", help="Whether to output debugging info", default=False, action="store_true")
  args = parser.parse_args()

  # fix up exclusions
  args.exclusions = re.split(r',\s*', args.exclusions) # split up comma-separated string into list
  return args

def get_commit_ids(commit_datafile):
  '''
  Load commit ids from file.
  @param commit_datafile: The path to the file containing the JSON array of commits.

  '''
  # load commit ids from file
  with open(commit_datafile, 'r') as commitfile:
    commits_list = json.loads(commitfile.read()) # convert to list
    # print(f'commits_list: {commits_list}')
    commit_ids = [commit['id'] for commit in commits_list if 'id' in commit.keys()] # extract commit ids from data from the GitHub Action context variable
    # print(f'commit_ids: {commit_ids}')
    return commit_ids

def get_commit_data(commit_id, exclusions):
  '''
  Get git stats for a commit.
  @param commit_id: The commit id.
  @param exclusions: The files to exclude from the git stats.
  @return: A dictionary containing the git stats for the commit.
  '''
  # print(f'commit id: {commit_id}')
  date_format = r'--date=unix' #format:"%m/%d/%Y %H:%M" # formatted in a way that works well in Google Sheets
  cmd = f"git show {date_format} --shortstat {commit_id} {exclusions}"
  # print(f'command: {cmd}')
  git_log = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  git_log_out, git_log_err = git_log.communicate()
  git_log_out = git_log_out.decode('UTF-8') # convert bytes to string
  # print(f'git output: {git_log_out}')
  # print(f'git error: {git_log_err}')

  # parse git commit log
  commit_data = {} # start off blank
  m = re.match(r"commit ([a-zA-Z0-9]+).*\nAuthor:\s(.*)\s<((.*))>.*\nDate:\s(.*)\n\n(.*)\n\n(.*?(\d+) file[s]? changed)?(.*?(\d+) insertion[s]?)?(.*?(\d+) deletion[s]?)?", git_log_out)
  if not m is None:
    # basic commit info
    commit_data['id'] = m.groups(0)[0].strip()
    commit_data['author_name'] = m.groups(0)[1].strip()
    commit_data['author_email'] = m.groups(0)[2].strip()
    commit_data['date'] = m.groups(0)[4].strip()
    commit_data['message'] = m.groups(0)[5].replace('[,"]', '').strip() # remove any quotes and commas to make a valid csv
    # fix the date
    local_tz = pytz.timezone("America/New_York")
    utc_time = datetime.utcfromtimestamp(int(commit_data['date'])) # convert unix time to utc datetime
    tz_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_tz) # convert to NY time
    commit_data['date'] = tz_time.strftime('%m/%d/%Y %H:%M') # formatted as nice string good for Google Sheets date field
    # stats
    commit_data['files'] = m.groups(0)[7].strip()
    commit_data['additions'] = m.groups(0)[9].strip() if len(m.groups(0)) > 9 and type(m.groups(0)[9])==str else 0
    commit_data['deletions'] = str(m.groups(0)[11]).strip() if len(m.groups(0)) > 11 and type(m.groups(0)[11])==str else 0
  # print(f'commit_data: {commit_data}')
  return commit_data

def verboseprint(verbose, *args):
  '''
  Print only if verbose flag is set.
  '''
  if verbose:
      v = print
  else:
      v = lambda *args: None
  v(*args)

def main():

  # set up command line arguments
  args = get_args()

  # set up logging
  logger = setup_logging(args.outputfile)

  commit_ids = get_commit_ids(args.inputfile) # get the ids of all commits from the json file

  # set up exclusions
  exclusions = '-- . ' + ' '.join(["':(exclude,glob){}'".format(x) for x in args.exclusions]) # put the exclusions in the format git logs uses
  # print(f'exclusions: {exclusions}')

  # write the CSV heading line
  logger.info('commit_id,commit_author_name,commit_author_email,commit_date,commit_message,commit_files,commit_additions,commit_deletions')
  
  # iterate over commit ids and add each to a list
  commits_list = [] # start it off blank
  for commit_id in commit_ids:
    
    # get git stats for this commit
    commit_data = get_commit_data(commit_id, exclusions) 

    # add this commit to the list
    commits_list.append(commit_data) 
    
    # log it to the csv data file
    logger.info(f'{commit_data["id"]},{commit_data["author_name"]},{commit_data["author_email"]},{commit_data["date"]},"{commit_data["message"]}",{commit_data["files"]},{commit_data["additions"]},{commit_data["deletions"]}')

  # debugging print
  verboseprint(args.verbose, f'commits_list: {commits_list}')

  # send the data to the web app URL, if any was supplied
  if args.url:
    # convert the list of commits to a JSON string
    commits_json = json.dumps(commits_list)
    # send the data to the web app in a POST request
    r = requests.post(args.url, json=commits_list)
    verboseprint(args.verbose, 'web app response: ', r.status_code, r.reason, r.content, r.text) # really the one

if __name__ == "__main__":
  main()
