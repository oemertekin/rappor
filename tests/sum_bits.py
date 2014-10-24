#!/usr/bin/python
#
# Copyright 2014 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Read the output of the RAPPOR simulation, and sum the bits by cohort to produce
a Counting Bloom filter.  This can then be analyzed by R.
"""

import csv
import sys


def main(argv):
  """Returns an exit code."""
  # TODO: need to read params file?
  num_cohorts = 64
  num_bloombits = 16
  sums = [[0] * num_bloombits for _ in xrange(num_cohorts)]
  num_reports = [0] * num_cohorts

  csv_in = csv.reader(sys.stdin)
  for i, (user_id, cohort, irr) in enumerate(csv_in):
    if i == 0:
      continue  # skip header

    cohort = int(cohort)
    num_reports[cohort] += 1

    assert len(irr) == 16, len(irr)
    for i, c in enumerate(irr):
      bit_num = num_bloombits - i - 1  # e.g. char 0 = bit 15, char 15 = bit 0
      if c == '1':
        sums[cohort][bit_num] += 1
      else:
        if c != '0':
          raise RuntimeError('Invalid IRR -- digits should be 0 or 1')

  for cohort in xrange(num_cohorts):
    # First column is the total number of reports in the cohort.
    row = [num_reports[cohort]] + sums[cohort]
    print ','.join(str(cell) for cell in row)


if __name__ == '__main__':
  try:
    main(sys.argv)
  except RuntimeError, e:
    print >>sys.stderr, e.args[0]
    sys.exit(1)
