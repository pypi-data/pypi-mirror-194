#  License: GNU GPLv3+, Rodrigo Schwencke (Copyleft) 

import re
import markdown
from markdown import Extension
from markdown.preprocessors import Preprocessor
from markdown.extensions.meta import MetaExtension, MetaPreprocessor
import yaml

DEFAULT_PRIORITY = '75'

class MkdocsRevealjsPreprocessor(Preprocessor):
    def __init__(self, md, config):
        super().__init__(md)
        self.config = config

    def run(self, lines):
        print(self.markdown)
        print("lines=", lines)
        return lines

class MkdocsRevealjsExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
            'priority' :        [DEFAULT_PRIORITY, 'Default Priority for this Extension']
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        """ Add MkdocsRevealjsPreprocessor to the Markdown instance. """
        # self.md = md
        md.registerExtension(self)
        md.preprocessors.register(MkdocsRevealjsPreprocessor(md, self.config), 'revealjs_block', int(self.config['priority'][0]))

def makeExtension(*args, **kwargs):
    return MkdocsRevealjsExtension(*args, **kwargs)
