# SPDX-FileCopyrightText: Copyright 2023 xlogic <https://xlogic.dev> and contributors to the project
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileContributor: 2023 Tymoteusz Blazejczyk <tymoteusz.blazejczyk@tymonx.com>

import sys

def main(*args) -> int:
    if not args:
        args = sys.argv[1:]

    print('Hello', args)

    return 0

if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:]))
