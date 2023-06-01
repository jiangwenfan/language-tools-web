import hashlib
import json
import os
import time
import uuid

import requests
from django.conf import settings
from django.db.models import QuerySet
from ielts.models import WordModel

from ..models import TranslateProviderModel, TranslateWordDataModel
