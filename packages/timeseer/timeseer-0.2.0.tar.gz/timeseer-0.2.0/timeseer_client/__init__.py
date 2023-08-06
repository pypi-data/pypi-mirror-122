"""Timeseer Client provides convenient remote access to Timeseer.

Data, metadata and event frames are exposed as Python objects."""

from kukur import DataType, Dictionary, InterpolationType, Metadata, ProcessType, SeriesSelector

from .base import AugmentationStrategy, TimeseerClientException
from .client import Client, filter_event_frames, filter_series

__all__ = [
    'AugmentationStrategy',
    'Client',
    'DataType',
    'Dictionary',
    'InterpolationType',
    'Metadata',
    'ProcessType',
    'SeriesSelector',
    'TimeseerClientException',
    'filter_event_frames',
    'filter_series',
]
