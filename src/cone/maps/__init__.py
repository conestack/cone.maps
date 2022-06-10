from cone.app import cfg
from cone.app import main_hook
from cone.maps.browser import configure_resources
import logging


logger = logging.getLogger('cone.maps')


@main_hook
def initialize_maps(config, global_config, settings):
    # application startup initialization

    # add translation
    config.add_translation_dirs('cone.maps:locale/')

    # static resources
    configure_resources(settings)

    # scan browser package
    config.scan('cone.maps.browser')
