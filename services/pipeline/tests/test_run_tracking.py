"""SCRUM-35 Pipeline run tracking
tests
"""

from datetime import datetime, timezone
from unittest.mock import Mock

import pytest

from pipeline.run_tracking import (
    INSERT_PIPELINE_RUN,
    UPDATE_PIPELINE_RUN,
    finish_pipeline_run,
    start_pipeline_run,
)

