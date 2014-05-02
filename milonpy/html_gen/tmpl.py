#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#######################################################
'''
module: html.tmpl
Created:Apr 10, 2012
author: nickmilon
Description:    html template                        
'''
#######################################################

### 
#Ref http://code.activestate.com/recipes/496743/
#Ref http://code.activestate.com/recipes/576663/
#Ref http://code.activestate.com/recipes/496702/
import re 
from milonpy.utils.basic import fl_read_or_str   
#! TO DO: "get rid of import re if posible"
def expandTxtWithURL (txt):  #! improvement set it to use a tag -
    r1 = r"(\b(http|https)://([-A-Za-z0-9+&@#/%?=~_()|!:,.;]*[-A-Za-z0-9+&@#/%=~_()|]))"
    r2 = r"((^|\b)www\.([-A-Za-z0-9+&@#/%?=~_()|!:,.;]*[-A-Za-z0-9+&@#/%=~_()|]))"
    return re.sub(r2,r'<a rel="nofollow" target="_blank" href="http://\1">\1</a>',re.sub(r1,r'<a rel="nofollow" target="_blank" href="\1">\1</a>',txt))


_html_mapping = (
    ("&", "&amp;"),
    ("  ", "&nbsp;&nbsp;"),
    (">", "&gt;"),
    ("<", "&lt;"),
    ('"', "&quot;"),
)
_nbsp='&nbsp;'
def escape(val):return escSpc(val)
def escSpc(val):return val.replace(' ', _nbsp)
def encode_html(obj):
    text = str(obj)
    for chr1, enc in _html_mapping:
        text = text.replace(chr1, enc)
    return text
def tmplSimple(template, dic, sectionNumber=None): 
    """this is a simple template system minimal in features but fast {$var_name$} for variables to be compatible with DJango templates
    '|||' section separation
    """
    exten = ['.html', '.js'] 
    delimiter=re.compile(r"""(\{\$.*?\$\})""",   re.MULTILINE|re.DOTALL|re.UNICODE) 
    tmp=fl_read_or_str(template, exten)
    #if tmp[1]:  dir = ''.join(template.rpartition('/')[0:2])  #@attention:  recheck this
    template=tmp[0]
    template=unicode(template, "utf-8") 
    if not sectionNumber is None:template=template.split(u'|||')[sectionNumber] 
    
    fa=re.findall(delimiter,template) 
    for el in fa:
        key=el[2:-2]
        val= dic.get(key, None)  
        if not val is None:template=template.replace(el,val)  
    return  template 
  
class NMtmpl(object):
    """
    teplate  can be a string or (a pathname if it endswith exten) 
    emitIncl argument 1 can be a NMtmpl object or a string or pathname  if pathname  starts with @ then @ is replaced with directory of current template
    emitIncl argument 2 is the namespace  of the include - if None defaults to parents namespace
    i.e ${emitIncl('@header_map_actions.html',None)}$  
    """
    exten = ['.html', '.js']
    start = '${'
    end   = '$}'
    dir = ''
    auto_emit = re.compile('(^[\'\"])|(^[a-zA-Z0-9_\[\]\'\"]+$)') 
    #delimiter = re.compile('%s(.*?)%s' % (re.escape('${'), re.escape('}$')), re.DOTALL)
    delimiter = re.compile(r"\$\{(.*?)\}\$", re.DOTALL) 
    #if len(start) != 2 or len(end) != 2:raise ValueError('delimiters must be 2 chrs')
    def __init__(self, template):
        self._template = fl_read_or_str(template, self.exten)
        if self._template[1]:self.dir = ''.join(template.rpartition('/')[0:2])
        self._template=self._template[0]
        self._code = None 
    def jotc(self):
        template=self._template
        offset = 0
        tokens = []
        for i, part in enumerate(self.delimiter.split(template)):
            part = part.replace('\\'.join(list(self.start)), self.start)
            part = part.replace('\\'.join(list(self.end)), self.end)
            if i % 2 == 0:
                if not part: continue
                part = part.replace('\\', '\\\\').replace('"', '\\"')
                part = '\t' * offset + 'emit("""%s""")' % part
            else:
                part = part.rstrip()
                if not part: continue
                if part.lstrip().startswith(':'):
                    if not offset:
                        raise SyntaxError('no block statement to terminate: ${%s}$' % part)
                    offset -= 1
                    part = part.lstrip()[1:]
                    if not part.endswith(':'): continue
                elif self.auto_emit.match(part.lstrip()):
                    part = 'emit(%s)' % part.lstrip()
                lines = part.splitlines()
                margin = min(len(l) - len(l.lstrip()) for l in lines if l.strip())
                part = '\n'.join('\t' * offset + l[margin:] for l in lines)
                if part.endswith(':'):
                    offset += 1
            tokens.append(part)
        if offset:
            raise SyntaxError('%i block statement(s) not terminated' % offset)
        self._code = compile('\n'.join(tokens), '<templite %r>' % template[:20], 'exec') 
        self.NMcodeorg=('\n'.join(tokens), '<templite %r>' % template[:20], 'exec')        #debug
        self.NMcodeanal=[tokens,'<templite %r>' , template[:20], 'exec' ]                  #debug 
    def render(self, __namespace=None, **kw):
        """
        renders the template according to the given namespace. 
        __namespace - a dictionary serving as a namespace for evaluation
        **kw - keyword arguments which are added to the namespace
        """
        if self._code is None:self.jotc()
        self.namespace = {}
        if __namespace: self.namespace.update(__namespace)
        if kw: self.namespace.update(kw)
        if 'emit' not in self.namespace:
            self.namespace['emit'] = self.emiter
            self.namespace['emitIncl'] = self.emiterIncl 
        self._output = []
        eval(self._code, self.namespace)  
        return ''.join(self._output)
    def emiterIncl(self, subcontents, nspace=None):  
        if nspace == None: nspace=self.namespace
        if not isinstance(subcontents,  NMtmpl):
            subcontents=subcontents[0].replace('@',self.dir)+subcontents[1:]  
            subcontents=NMtmpl(subcontents) 
            if len(self._output) > 0:
                shiftchrs=self._output[-1].rpartition('\n')[2]   
                subcontents._template= subcontents._template.replace('\n', '\n'+ shiftchrs)
        subcontents.render(nspace)
    def emiter(self, *args): 
        for a in args:  
            self._output.append(str(a))