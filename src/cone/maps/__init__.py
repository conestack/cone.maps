from cone.app import main_hook
from cone.maps.browser import configure_resources
import logging


logger = logging.getLogger('cone.maps')


@main_hook
def initialize_maps(config, global_config, settings):
    # application startup initialization

    # static resources
    configure_resources(settings)

    # add translation
    config.add_translation_dirs('cone.maps:locale/')

    # scan browser package
    config.scan('cone.maps.browser')
