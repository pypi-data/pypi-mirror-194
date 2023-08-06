# Copyright (c) 2021 Matteo Redaelli
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import re
import logging
import qsAPI
import time
from datetime import date
from datetime import timedelta

def reloadtask_count(qrs, status):
    param = {"filter": f"operational.lastExecutionResult.status eq {status}"}
    resp = qrs.driver.get(f"/qrs/reloadtask/count", param=param).json()
    return resp


def old_reloadtasks(qrs, lastreload_days, status, id="full"):

    today = date.today()
    modified_date = (today - timedelta(days=lastreload_days)).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    logging.debug("Modified date = " + modified_date)
    pFilter = f"operational.lastExecutionResult.startTime lt '{modified_date}'"
    if status:
        pFilter += f" and operational.lastExecutionResult.status eq {status}"
    logging.debug("Searching reloadtasks with pFilter= " + str(pFilter))
    param = {"filter": pFilter}
    resp = qrs.driver.get(f"/qrs/reloadtask/{id}", param=param)

    result = {}
    if resp.ok:
        result = resp.json()
    else:
        logging.error(resp)
    return result
