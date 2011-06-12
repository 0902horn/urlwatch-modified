# -*- coding: cp936 -*-
#
# Example hooks file for urlwatch
#
# Copyright (c) 2008-2011 Thomas Perl <thp.io/about>
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. The name of the author may not be used to endorse or promote products
#    derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

# You can decide which filter you want to apply using the "url"
# parameter and you can use the "re" module to search for the
# content that you want to filter, so the noise is removed.


# Needed for regular expression substitutions
import re

# Additional modules installed with urlwatch
from urlwatch import ical2txt
from urlwatch import html2txt

import htmllib
import formatter
import StringIO

class MyParser(htmllib.HTMLParser):

    def __init__(self, datacache, verbose = 0):
        fmt = formatter.AbstractFormatter(formatter.DumbWriter(datacache))
        htmllib.HTMLParser.__init__(self, fmt, verbose)
    def start_style(self, attrs):
        self.save_bgn()
    def end_style(self):
        self.save_end()
    def start_script(self, attrs):
        if attrs and "src" in attrs[0]:
            pass
        else:
            self.save_bgn()
    def end_script(self):
        if self.savedata:
            self.save_end()
    def anchor_end(self):
            if self.anchor:
                self.anchor = None
    def handle_image(self, src, alt, *args):
        #self.handle_data(alt)
        pass
    def convert_entityref(self, name):
        if name is 'nbsp':
            return chr(0x0020)
        elif name is 'apos':
            return chr(0x0027)
        else:
            return

def filter(url, data):
    datacache = StringIO.StringIO()
    par = MyParser(datacache)
    par.feed(data)
    par.close()
    return datacache.getvalue()

