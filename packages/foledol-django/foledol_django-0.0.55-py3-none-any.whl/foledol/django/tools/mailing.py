import os
from io import BytesIO

from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from reportlab.pdfbase.pdfmetrics import stringWidth

from foledol.django.utils import image_ratio


class MailingItem:
    def __init__(self, key, label):
        self.key = key
        self.label = label

