"""Dialog plugin."""


from otopi import util


from . import chklicense


@util.export
def createPlugins(context):
    chklicense.Plugin(context=context)


#
