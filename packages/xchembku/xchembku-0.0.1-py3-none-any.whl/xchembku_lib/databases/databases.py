# Use standard logging in this module.
import logging

# Exceptions.
from xchembku_api.exceptions import NotFound

# Class managing list of things.
from xchembku_api.things import Things

logger = logging.getLogger(__name__)


class Databases(Things):
    """
    List of available databases.
    """

    # ----------------------------------------------------------------------------------------
    def __init__(self, name=None):
        Things.__init__(self, name)

    # ----------------------------------------------------------------------------------------
    def build_object(self, specification):
        """"""

        database_class = self.lookup_class(specification["type"])

        try:
            database_object = database_class(specification)
        except Exception as exception:
            raise RuntimeError(
                "unable to build database object for type %s" % (database_class)
            ) from exception

        return database_object

    # ----------------------------------------------------------------------------------------
    def lookup_class(self, class_type):
        """
        Given the class type as string, return a class object.
        """

        if class_type == "xchembku_lib.xchembku_databases.aiosqlite":
            from xchembku_lib.databases.aiosqlite import Aiosqlite

            return Aiosqlite

        raise NotFound("unable to get database class for type %s" % (class_type))
