import re

from markdown import markdown


class Block(object):
    types = {'heading', 'subheading', 'paragraph', 'image'}
    type_re = {
        re.compile(r'^# '): 'heading',
        re.compile(r'^## '): 'subheading',
        re.compile(r'^<img '): 'image',
    }

    def __init__(self, raw_text):
        self.raw_text = raw_text

    def markdown(self):
        return self.raw_text

    def html(self):
        return markdown(self.markdown())

    def type(self):
        for regex, type_ in Block.type_re.iteritems():
            if regex.search(self.raw_text):
                return type_
        return 'paragraph'


class Content(object):
    block_start_re = re.compile(r'<!-- start block -->\s*\n?')

    def __init__(self, raw_text):
        self.blocks = self.__class__.parse_blocks(raw_text)

    @classmethod
    def parse_blocks(cls, raw_text):
        return [Block(text) for text in cls.block_start_re.split(raw_text)]

    def move_block(self, current_index, new_index):
        block = self.blocks.pop(current_index)
        self.blocks.insert(new_index, block)

    def markdown(self):
        return '<!-- start block -->\n'.join(b.markdown() for b in self.blocks)

    def html(self):
        return markdown(self.markdown())


if __name__ == '__main__':
    raw = '''# title

<!-- start block -->
This is paragraph 1.

<!-- start block -->
## subtitle

<!-- start block -->
This is paragraph 2.

This is paragraph 3.'''

    content = Content(raw)
    assert len(content.blocks) == 4
    assert content.markdown() == raw
    assert content.blocks[0].type() == 'heading'
    assert content.blocks[1].type() == 'paragraph'
    assert content.blocks[2].type() == 'subheading'
    assert content.blocks[3].type() == 'paragraph'
