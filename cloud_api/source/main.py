# -*- coding: utf-8 -*-
import logging

from app import create_app

logger = logging.getLogger(__name__)

app, _ = create_app()
