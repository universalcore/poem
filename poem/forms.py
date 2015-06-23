import colander
from deform import Form, widget


@colander.deferred
def block_type_validator(node, kwargs):
    return colander.Regex(r'^%s$' % kwargs.get('block_type', ''))


@colander.deferred
def block_type_default(node, kwargs):
    return kwargs.get('block_type', '')


class BlockSchema(colander.MappingSchema):
    block_type = colander.SchemaNode(
        colander.String(),
        default=block_type_default,
        validator=block_type_validator,
        widget=widget.HiddenWidget())


class ParagraphBlockSchema(BlockSchema):
    content = colander.SchemaNode(
        colander.String(),
        missing='',
        title='Add your copy',  # TODO trans
        widget=widget.TextAreaWidget())


class HeadingBlockSchema(BlockSchema):
    content = colander.SchemaNode(
        colander.String(),
        missing='',
        title='Heading text')  # TODO trans


class ImageBlockSchema(BlockSchema):
    image_url = colander.SchemaNode(
        colander.String(),
        missing='',
        title='Image URL')  # TODO trans
    image_caption = colander.SchemaNode(
        colander.String(),
        missing='',
        title='Image caption')  # TODO trans


class BlockEditForm(Form):

    def __init__(self, block=None, block_type=None):
        if block:
            block_type = block.type
        schema_cls = {
            'paragraph': ParagraphBlockSchema,
            'heading': HeadingBlockSchema,
            'subheading': HeadingBlockSchema,
            'image': ImageBlockSchema
        }[block_type]
        schema = schema_cls().bind(block_type=block_type)
        # TODO trans
        super(BlockEditForm, self).__init__(schema, buttons=('save', ))
