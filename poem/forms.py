import colander
from deform import Button, Form, widget


@colander.deferred
def block_type_validator(node, kwargs):
    return colander.Regex(r'^%s$' % kwargs.get('block_type', ''))


class BlockSchema(colander.MappingSchema):
    block_type = colander.SchemaNode(
        colander.String(),
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
        super(BlockEditForm, self).__init__(
            schema, buttons=(Button('save', 'Save'),))


@colander.deferred
def block_position_validator(node, kwargs):
    return colander.Range(kwargs['min_pos'], kwargs['max_pos'])


@colander.deferred
def block_position_widget(node, kwargs):
    return widget.SelectWidget(
        values=map(
            lambda num: (num, str(num)),
            range(kwargs['min_pos'], kwargs['max_pos'] + 1)))


class BlockPositionSchema(colander.MappingSchema):
    position = colander.SchemaNode(
        colander.Integer(),
        validator=block_position_validator,
        title='Set position',  # TODO trans
        widget=block_position_widget)


class BlockPositionForm(Form):

    def __init__(self, max_pos, min_pos=1):
        schema = BlockPositionSchema().bind(min_pos=min_pos, max_pos=max_pos)
        # TODO trans
        super(BlockPositionForm, self).__init__(
            schema, buttons=(
                Button('move_up', 'Move one up'),
                Button('move_down', 'Move one down'),
                Button('save', 'Save')))
