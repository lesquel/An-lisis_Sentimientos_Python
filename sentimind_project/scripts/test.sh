#!/usr/bin/env bash

set -euo pipefail

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lib.sh"

compose -f "$(compose_file_for_mode dev)" run --rm backend python manage.py test
