# POEM
Publishing On Everyone's Mobile

## Demo

The demo site is up at http://poem.qa-hub.unicore.io.

## Functionality

At the moment POEM implements the core content authoring functionality. That is creating new content blocks, editing the content blocks and moving them around. The content block types that have been implemented are:

* paragraph
* image links
* heading
* subheading

Block types that have not been implemented yet are image file uploads and related content.

## Technical notes

A content item is currently stored as a simple Markdown file in the data/ folder. The content id is the file name. Blocks are delineated by block comments, e.g. ``<!-- block 2 -->``. Here is a complete sample:

```Markdown
<!-- block 1 -->
# Dogs

<!-- block 2 -->
![Cute doggie](http://i.imgur.com/rhd1TFF.jpg)

<!-- block 3 -->
This is some text about a dog
```

### Noteworthy classes

The subclasses of `poem.content.Block` implement parsing and rendering of individual blocks. The `poem.content.Content` class parses and renders Markdown containing multiple blocks. It also exposes methods to access and manipulate these blocks.

Note that the `poem.content.TestContent` subclass is responsible for the current storage implementation.
