
from . import otopi_constants as constants

from .import util

@util.export
def parseTypedValue(value):
    """Parse type:value string into python object."""
    try:
        vtype, value = value.split(':', 1)
    except ValueError:
        raise ValueError(_("Missing variable type"))

    if vtype == constants.Types.NONE:
        value = None
    elif vtype == constants.Types.BOOLEAN:
        value = value not in (0, 'f', 'F', 'false', 'False')
    elif vtype == constants.Types.INTEGER:
        value = int(value)
    elif vtype == constants.Types.STRING:
        pass
    elif vtype == constants.Types.MULTI_STRING:
        value = value.splitlines()
    else:
        raise KeyError(
            _('Invalid variable type {type}').format(
                type=vtype
            )
        )
    return value


