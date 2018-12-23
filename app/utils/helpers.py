#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
from math import ceil
from sendgrid import Email
from sendgrid.helpers.mail import Content, Mail
import sendgrid

from app import config
from app.utils import constants
from app import log

logger = log.get_logger()


def keys_exists(element, *keys):
    """
    Check if *keys (nested) exists in `element` (dict).
    """
    if type(element) is not dict:
        raise AttributeError(
            'keys_exists() expects dict as first argument.'
        )
    if len(keys) == 0:
        raise AttributeError(
            'keys_exists() expects at least two arguments, one given.'
        )

    _element = element
    for key in keys:
        try:
            _element = _element[key]
        except KeyError:
            return False
    return True


class Pagination:
    def __init__(self, items, page, item_per_page, total_items):
        self.items = items
        self.page = page
        self.total_items = total_items
        self.item_per_page = item_per_page
        self.total_pages = int(ceil(total_items / float(item_per_page)))

    @property
    def has_next(self):
        return self.page < self.total_pages

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def next_page(self):
        return self.page + 1

    @property
    def prev_page(self):
        return self.page - 1


def paginate(queryset, page=1, item_per_page=30):
    skip = (page-1)*item_per_page
    limit = item_per_page

    return Pagination(
        queryset.limit(limit).skip(skip),
        page=page,
        item_per_page=item_per_page,
        total_items=queryset.count()
    )


def send_email(to_email, subject, content):
    """
    send email
    :param to_email:
    :param subject:
    :param content:
    :return:
    """
    if config.EMAIL_PROVIDER == constants.SENDGRID:
        send_sendgrid_mail(to_email, subject, content)


def send_sendgrid_mail(to_email, subject, content):
    """
    send sendgrid mail
    :param to_email:
    :param subject:
    :param content:
    :return:
    """
    sg = sendgrid.SendGridAPIClient(apikey=config.EMAIL_API_KEY)

    from_email = Email(config.FROM_EMAIL)
    to_email = Email(to_email)
    content = Content("text/plain", content)
    mail = Mail(from_email, subject, to_email, content)

    # todo try except to log error if possible
    response = sg.client.mail.send.post(request_body=mail.get())
    logger.info(response.status_code)
    logger.info("mail sent")


def calculate_feedback(_subject):
    total_rating = len(_subject.feedbacks) if _subject.feedbacks else 0

    total_comments = len(
        [
            fb for fb in _subject.feedbacks if
            _subject.feedbacks and "comment" in fb
        ]
    ) if _subject.feedbacks else 0

    rating = numpy.average(
        [
            fb["rating"] for fb in _subject.feedbacks
            if _subject.feedbacks and "rating" in fb
        ]
    ) if _subject.feedbacks else 0

    return total_rating, total_comments, rating
