import backoff
import base64
import math
from collections import OrderedDict, defaultdict
from datetime import datetime
from docker import auth as docker_auth
import functools
import json
import logging
import random
import re
import requests
import string
import time
from itertools import groupby
from urllib.parse import urljoin

from django.conf import settings
from django.db import models
from rest_framework.exceptions import ValidationError, NotFound
from jsonfield import JSONField

from api.models import get_session
from api.models import UuidAuditedModel, AlreadyExists, DryccException, ServiceUnavailable
from api.models.config import Config
from api.models.domain import Domain
from api.models.release import Release
from api.models.tls import TLS
from api.models.appsettings import AppSettings
from api.models.volume import Volume
from api.utils import generate_app_name, apply_tasks
from scheduler import KubeHTTPException, KubeException

logger = logging.getLogger(__name__)


# http://kubernetes.io/v1.1/docs/design/identifiers.html
def validate_app_id(value):
    """
    Check that the value follows the kubernetes name constraints
    """
    match = re.match(r'[a-z]([a-z0-9-]*[a-z0-9])?$', value)
    if not match:
        raise ValidationError("App name must start with an alphabetic character, cannot end with a"
                              + " hyphen and can only contain a-z (lowercase), 0-9 and hyphens.")


def validate_app_structure(value):
    """Error if the dict values aren't ints >= 0"""
    try:
        if any(int(v) < 0 for v in value.values()):
            raise ValueError("Must be greater than or equal to zero")
    except ValueError as err:
        raise ValidationError(str(err))


def validate_reserved_names(value):
    """A value cannot use some reserved names."""
    if value in settings.DRYCC_RESERVED_NAMES:
        raise ValidationError('{} is a reserved name.'.format(value))


class Pod(dict):
    pass

