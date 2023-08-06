"""
todo: remove
"""
import logging
from abc import ABCMeta, abstractmethod

from pytest_xlsx.file import XlsxItem

logger = logging.getLogger(__name__)


class Runner(metaclass=ABCMeta):
    @abstractmethod
    def execute(self, item: XlsxItem):
        """
        :param item: pytest用例对象
        :return:
        """
