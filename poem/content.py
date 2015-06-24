import re
import os
from pkg_resources import resource_filename

from jinja2 import Markup
from markdown import markdown


class Block(object):
    # TODO - these should probably be subclasses
    types = {'heading', 'subheading', 'paragraph', 'image'}
    type_re = {
        re.compile(r'^# '): 'heading',
        re.compile(r'^## '): 'subheading',
        re.compile(r'^<img '): 'image',
    }

    def __init__(self, id, raw_text):
        self.raw_text = raw_text
        self.id = id
        self.type = self.__class__.parse_type(raw_text)
        self.data = self.__class__.parse_data(raw_text, self.type)

    @classmethod
    def parse_type(cls, raw_text):
        for regex, type_ in Block.type_re.iteritems():
            if regex.search(raw_text):
                return type_
        return 'paragraph'

    @classmethod
    def parse_data(self, raw_text, type):
        if type == 'heading':
            return {'content': raw_text[2:]}
        if type == 'subheading':
            return {'content': raw_text[3:]}
        if type == 'image':
            match = re.match(
                r'^<img src="([^"]*)" alt="([^"]*)" />$', raw_text)
            return {'image_url': match.group(1),
                    'image_caption': match.group(2)}
        return {'content': raw_text}

    @classmethod
    def make_markdown(cls, type, content=None, image_url=None,
                      image_caption=None):
        if type == 'heading':
            return '# %s\n' % content
        if type == 'subheading':
            return '## %s\n' % content
        if type == 'image':
            return '<img src="%s" alt="%s" />\n' % (image_url, image_caption)
        return '%s\n' % content

    def update(self, raw_text=None, content=None, image_url=None,
               image_caption=None):
        if raw_text:
            self.raw_text = raw_text
            self.data = self.__class__.parse_data(raw_text, self.type)
        else:
            self.raw_text = self.__class__.make_markdown(
                self.type, content, image_url, image_caption)
            self.data = self.__class__.parse_data(self.raw_text, self.type)

    def markdown(self):
        return self.raw_text

    def html(self):
        return Markup(markdown(self.markdown()))


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
        return [Block(int(m.group('id')), raw_text[s[0]:s[1]])
                for m, s in zip(matches, slices)]

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
        return ''.join('<!-- block %s -->\n%s' % (b.id, b.markdown())
                       for b in self.blocks)

    def html(self):
        return Markup(markdown(self.markdown()))


class TestContent(Content):

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
            raw_text = '''<!-- block 1 -->
# title

<!-- block 2 -->
This is paragraph 1.

<!-- block 3 -->
## subtitle

<!-- block 4 -->
This is paragraph 2.

This is paragraph 3.'''
            with open(filepath, 'w') as f:
                f.write(raw_text)
        super(TestContent, self).__init__(id, raw_text)

    def save(self):
        filepath = resource_filename('poem', 'data/%s.md' % self.id)
        with open(filepath, 'w') as f:
            f.write(self.markdown())


if __name__ == '__main__':
    raw = '''<!-- block 1 -->
# title

<!-- block 2 -->
This is paragraph 1.

<!-- block 3 -->
## subtitle

<!-- block 4 -->
This is paragraph 2.

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
