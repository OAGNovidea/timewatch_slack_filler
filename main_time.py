#!/usr/bin/python
"""For TimeWatch Version 5.069"""
# under parameters, put as below:
# Last updated at 23/12/19

import argparse
import datetime
import logging

import timewatch

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Automatic work hours reporting for timewatch.co.il')

  parser.add_argument('company', type=int, help='Company ID')
  parser.add_argument('user', help='user name/id')
  parser.add_argument('password', help='user password')

  today = datetime.date.today()
  parser.add_argument('-y', '--year', default=today.year, type=int, help='Year number to fill')
  parser.add_argument('-m', '--month', default=today.month, help='Month number or name')

  parser.add_argument('-v', '--verbose', default=0, action='count', help='increase logging level')

  parser.add_argument('-o', '--override', default='incomplete',
                       choices=['all', 'incomplete', 'regular'],
                       help='Control override behavior. all - override all '
                            'working days, unsafe to vacation/sick days. '
                            'incomplete = only override days with partial '
                            'records. regular - override regular days '
                            '(without absence reason) only')

  parser.add_argument('-s', '--starttime', default='09:00', help='punch-in time')
  parser.add_argument('-d', '--daysoff', default=['friday', 'saturday'], help='''Days you're off, not working,
   the defaults are Friday and Saturday''')

  parser.add_argument('-j', '--jitter', default=10, type=int,
                       help='punching time random range in minutes.')

  parser.add_argument('-r', '--retries', default=9, help='amount of times to retries on failed punchin')

  args = parser.parse_args()

  verbosity_levels = [logging.WARNING, logging.INFO, logging.DEBUG]
  verbosity = min(args.verbose, len(verbosity_levels)-1)
  logging_level = verbosity_levels[verbosity]

  tw=timewatch.TimeWatch(loglevel = logging_level,
                         override = args.override,
                         starttime = args.starttime,
                         jitter = args.jitter,
                         retries = args.retries,
                         daysoff = args.daysoff)

  tw.login(args.company, args.user, args.password)
  tw.edit_month(args.year, args.month)