import re
import os
import glob
from pkg_resources import resource_filename

from jinja2 import Markup
from markdown import markdown


def get_block_classes():
    # list is ordered for correct parsing
    return [
        HeadingBlock,
        ImageBlock,
        ParagraphBlock
    ]


class Block(object):

    def __init__(self, id, data):
        self.id = id
        self.data = data

    @classmethod
    def test(cls, raw_text):
        match = cls.pattern.search(raw_text)
        return bool(match)

    @classmethod
    def parse_data(cls, raw_text):
        match = cls.pattern.search(raw_text)
        if not match:
            raise ValueError('%r does not match %s' % (raw_text, cls.__name__))
        return match.groupdict()

    def update(self, new_data):
        data = self.data.copy()
        data.update(new_data)
        return self.__class__(self.id, data)

    def markdown(self):
        return self.template % self.data

    def html(self):
        return Markup(markdown(self.markdown()))


class ParagraphBlock(Block):
    type_name = 'paragraph'
    pattern = re.compile(r'^(?P<content>.*)$', re.DOTALL)
    template = '%(content)s'


class ImageBlock(Block):
    type_name = 'image'
    pattern = re.compile(r'^!\[(?P<image_caption>.*)\]\((?P<image_url>.*)\)$')
    template = '![%(image_caption)s](%(image_url)s)'


class HeadingBlock(Block):
    pattern = re.compile(r'^(?P<level>#{1,3})(?P<content>.*)$')
    levels = [(1, 'heading'), (2, 'subheading'), (3, 'subsubheading')]

    @property
    def level(self):
        return int(self.data['level'])

    @property
    def type_name(self):
        return dict(self.levels)[self.level]

    @property
    def template(self):
        hashes = '#' * self.level
        return '%s %(content)s' % (hashes, )


class Content(object):
    block_start_re = re.compile(r'<!-- block (?P<id>\d+) -->\s*\n')

    def __init__(self, id, raw_text):
        self.id = id
        self.blocks = self.__class__.parse_blocks(raw_text)

    @classmethod
    def parse_blocks(cls, raw_text):
        matches = list(cls.block_start_re.finditer(raw_text))
        if not matches:
            return []

        slices = [(m1.end(), m2.start())
                  for m1, m2 in zip(matches, matches[1:])]
        slices.append((matches[-1].end(), len(raw_text)))
        return [cls.parse_block(int(m.group('id')), raw_text[s[0]:s[1]])
                for m, s in zip(matches, slices)]

    @classmethod
    def parse_block(cls, id, block_text):
        for block_cls in get_block_classes():
            try:
                data = block_cls.parse_data(block_text)
                return block_cls(id, data)
            except ValueError:
                pass
        raise ValueError('%r block could not be parsed' % (block_text,))

    def get_block(self, block_id):
        block_id = int(block_id)
        [block] = filter(lambda block: block.id == block_id,
                         self.blocks)
        return block

    def move_block(self, current_index, new_index):
        if current_index == new_index:
            return
        block = self.blocks.pop(current_index)
        self.blocks.insert(new_index, block)

    def delete_block(self, block_id):
        block_id = int(block_id)
        [(index, block)] = [(i, block)
                            for i, block in enumerate(self.blocks)
                            if block.id == block_id]
        del self.blocks[index]
        return block

    def add_block(self, type, **kwargs):
        raw_text = Block.make_markdown(type, **kwargs)
        next_id = max(0, 0, *[block.id for block in self.blocks]) + 1
        self.blocks.append(Block(next_id, raw_text))

    def markdown(self):
        return '\n'.join('<!-- block %s -->\n%s' % (b.id, b.markdown())
                         for b in self.blocks)

    def html(self):
        return Markup(markdown(self.markdown()))


class TestContent(Content):
    '''
    TODO: replace this subclass with proper storage
    '''

    def __init__(self, id):
        filepath = resource_filename('poem', 'data/%s.md' % id)
        try:
            os.mkdir(os.path.dirname(filepath))
        except OSError:
            pass
        try:
            with open(filepath) as f:
                raw_text = f.read()
        except IOError:
            with open(filepath, 'w+') as f:
                raw_text = ''
        super(TestContent, self).__init__(id, raw_text)

    def save(self):
        filepath = resource_filename('poem', 'data/%s.md' % self.id)
        with open(filepath, 'w') as f:
            f.write(self.markdown())

    def rename(self, new_id):
        filepath = resource_filename('poem', 'data/%s.md' % self.id)
        filepath_new = resource_filename('poem', 'data/%s.md' % new_id)
        os.rename(filepath, filepath_new)
        self.id = new_id

    @classmethod
    def all(cls):
        filepath = resource_filename('poem', 'data/*.md')
        filenames = [os.path.splitext(os.path.basename(n))[0]
                     for n in glob.glob(filepath)]
        return [TestContent(fn) for fn in filenames]


if __name__ == '__main__':
    raw = '''<!-- block 1 -->
# title
<!-- block 2 -->
This is paragraph 1.
<!-- block 3 -->
## subtitle
<!-- block 4 -->
This is paragraph 2.

And it carries on here.
<!-- block 5 -->
![Cute doggie](http://i.imgur.com/rhd1TFF.jpg)
<!-- block 6 -->
This is paragraph 3.'''

    content = Content(raw)
    assert len(content.blocks) == 4
    assert content.markdown() == raw
    assert content.blocks[0].id == 1
    assert content.blocks[1].id == 2
    assert content.blocks[2].id == 3
    assert content.blocks[3].id == 4
    assert content.blocks[0].type == 'heading'
    assert content.blocks[1].type == 'paragraph'
    assert content.blocks[2].type == 'subheading'
    assert content.blocks[3].type == 'paragraph'
