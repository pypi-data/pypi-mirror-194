# Use standard logging in this module.
import logging
import os

# Utilities.
from dls_utilpack.callsign import callsign
from dls_utilpack.require import require

# Class managing list of things.
from dls_utilpack.things import Things

from dls_multiconf_lib.constants import ThingTypes

# Environment variables with some extra functionality.
from dls_multiconf_lib.envvar import Envvar

# Exceptions.
from dls_multiconf_lib.exceptions import NotFound

logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------------------
__default_dls_multiconf = None


def multiconfs_set_default(dls_multiconf):
    global __default_dls_multiconf
    __default_dls_multiconf = dls_multiconf


def multiconfs_get_default():
    global __default_dls_multiconf
    if __default_dls_multiconf is None:
        raise RuntimeError("multiconfs_get_default instance is None")
    return __default_dls_multiconf


def multiconfs_has_default():
    global __default_dls_multiconf
    return __default_dls_multiconf is not None


# -----------------------------------------------------------------------------------------


class Multiconfs(Things):
    """
    Configuration loader.
    """

    # ----------------------------------------------------------------------------------------
    def __init__(self, name=None):
        Things.__init__(self, name)

    # ----------------------------------------------------------------------------------------
    def build_object(self, specification):
        """"""

        dls_multiconf_class = self.lookup_class(
            require(f"{callsign(self)} specification", specification, "type")
        )

        try:
            dls_multiconf_object = dls_multiconf_class(specification)
        except Exception as exception:
            raise RuntimeError(
                "unable to instantiate dls_multiconf object from module %s"
                % (dls_multiconf_class.__module__)
            ) from exception

        return dls_multiconf_object

    # ----------------------------------------------------------------------------------------
    def lookup_class(self, class_type):
        """"""

        if class_type == ThingTypes.YAML:
            from dls_multiconf_lib.yaml import Yaml

            return Yaml

        raise NotFound("unable to get dls_multiconf class for type %s" % (class_type))

    # ----------------------------------------------------------------------------------------
    def build_object_from_environment(self, environ=None):

        # Get the explicit name of the config file.
        dls_multiconf_configfile = Envvar(Envvar.MULTICONF_CONFIGFILE, environ=environ)

        # Config file is explicitly named?
        if dls_multiconf_configfile.is_set:
            # Make sure the path exists.
            configurator_filename = dls_multiconf_configfile.value
            if not os.path.exists(configurator_filename):
                raise RuntimeError(
                    f"unable to find {Envvar.MULTICONF_CONFIGFILE} {configurator_filename}"
                )
        # Config file is not explicitly named?
        else:
            raise RuntimeError(
                f"environment variable {Envvar.MULTICONF_CONFIGFILE} is not set"
            )

        dls_multiconf = self.build_object(
            {
                "type": ThingTypes.YAML,
                "type_specific_tbd": {"filename": configurator_filename},
            }
        )

        dls_multiconf.substitute(
            {"configurator_directory": os.path.dirname(configurator_filename)}
        )

        return dls_multiconf
