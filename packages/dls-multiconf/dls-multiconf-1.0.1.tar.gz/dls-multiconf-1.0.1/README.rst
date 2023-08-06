===========================
dls-multiconf
===========================

Python class for runtime configuration coordinating multiple services.


Converting from old Configurator usage:
- in project.yaml depedencies add dls_multiconf
- from src delete configurators directory
- from tests delete test_configurator.py
- change all xchembku_lib.configurators.configurators to dls_multiconf_lib.multiconfs
- change all Configurators to Multiconfs
- change all xchembku_configurators_set_default to multiconfs_set_default
- change all configurator to multiconf
- change all chimpflow_datafaces_get_default to xchembku_datafaces_get_default
- change all "xchembku_lib.xchembku_multiconfs.yaml" to MulticonfThingTypes.YAML
- add from dls_multiconf_lib.constants import ThingTypes as MulticonfThingTypes

---------------------------
Table of contents
---------------------------

..
    Anything below this line is used only when viewing README.rst on Gitlab.
    It will be ingored when included in index.rst

---------------------------
Viewing the docs
---------------------------

https://diamondlightsource.github.io/dls_multiconf
