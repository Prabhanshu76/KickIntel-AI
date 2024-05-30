from __future__ import annotations
from typing import Generator
import sys
import numpy as np
import cv2
from dataclasses import dataclass, field
from typing import Tuple, Optional, List, Dict, Any
import torch
from tqdm.notebook import tqdm
from yolox.tracker.byte_tracker import BYTETracker, STrack
from onemetric.cv.utils.iou import box_iou_batch
import io
import os
