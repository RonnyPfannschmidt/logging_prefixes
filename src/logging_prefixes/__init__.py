# -*- coding: utf-8 -*-
from __future__ import unicode_literals


import logging
from .funcwrap import logged, call_unlogged, call_sig


__all__ = ["logged", "call_unlogged", "call_sig"]


class PrependParentsAdapter(logging.LoggerAdapter):
    """This class ensures the path to the widget is represented in the log records."""

    def process(self, msg, kwargs):
        # Sanitizing %->%% for formatter working properly
        sanitized_path = self.extra["widget_path"].replace("%", "%%")
        return "[{}]: {}".format(sanitized_path, msg), kwargs

    def __repr__(self):
        return "{}({!r}, {!r})".format(
            type(self).__name__, self.logger, self.extra["widget_path"]
        )


def create_widget_logger(widget_path, logger):
    """Create a logger that prepends the ``widget_path`` to the log records.

    Args:
        widget_path: A string indicating the path to the widget
        logger: Specify a logger if you want some output

    Returns:
        A logger instance.
    """
    return PrependParentsAdapter(logger, {"widget_path": widget_path})


def _create_logger_appender(parent_logger, suffix):
    """Generic name-append logger creator."""
    if isinstance(parent_logger, PrependParentsAdapter):
        widget_path = "{}{}".format(parent_logger.extra["widget_path"], suffix)
        logger = parent_logger.logger
    else:
        widget_path = suffix
        logger = parent_logger
    return PrependParentsAdapter(logger, {"widget_path": widget_path.lstrip("/")})


def create_child_logger(parent_logger, child_name):
    """Creates a logger for a standard child widget.

    Args:
        parent_logger: Logger of the parent widget (or can be plain,
            in that case this is thetop-level widget then.
        child_name: Name under which this child widgets is represented.

    Returns:
        A :py:class:`PrependParentsAdapter` logger instance.
    """
    return _create_logger_appender(parent_logger, "/{}".format(child_name))


def create_item_logger(parent_logger, item):
    """Creates a logger for a widget that is inside iteration - referred to by index or key.

    Args:
        parent_logger: Logger of the parent widget (or can be plain,
            in that case this is the top-level widget then.
        item: Index or key name under which this widget is represented.

    Returns:
        A :py:class:`PrependParentsAdapter` logger instance.
    """
    return _create_logger_appender(parent_logger, "[{!r}]".format(item))
