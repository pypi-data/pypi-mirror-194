import os

elements = [
    "a",
    "abbr",
    "acronym",
    "address",
    "applet",
    "area",
    "article",
    "aside",
    "audio",
    "b",
    "base",
    "basefont",
    "bdi",
    "bdo",
    "bgsound",
    "big",
    "blink",
    "blockquote",
    "body",
    "br",
    "button",
    "canvas",
    "caption",
    "center",
    "cite",
    "code",
    "col",
    "colgroup",
    "content",
    "data",
    "datalist",
    "dd",
    "decorator",
    "del",
    "details",
    "dfn",
    "dir",
    "div",
    "dl",
    "dt",
    "element",
    "em",
    "embed",
    "fieldset",
    "figcaption",
    "figure",
    "font",
    "footer",
    "form",
    "frame",
    "frameset",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "head",
    "header",
    "hgroup",
    "hr",
    "html",
    "i",
    "iframe",
    "img",
    "input",
    "ins",
    "isindex",
    "kbd",
    "keygen",
    "label",
    "legend",
    "li",
    "link",
    "listing",
    "main",
    "map",
    "mark",
    "marquee",
    "menu",
    "menuitem",
    "meta",
    "meter",
    "nav",
    "nobr",
    "noframes",
    "noscript",
    "object",
    "ol",
    "optgroup",
    "option",
    "output",
    "p",
    "param",
    "plaintext",
    "pre",
    "progress",
    "q",
    "rp",
    "rt",
    "ruby",
    "s",
    "samp",
    "script",
    "section",
    "select",
    "shadow",
    "small",
    "source",
    "spacer",
    "span",
    "strike",
    "strong",
    "style",
    "sub",
    "summary",
    "sup",
    "table",
    "tbody",
    "td",
    "template",
    "textarea",
    "tfoot",
    "th",
    "thead",
    "time",
    "title",
    "tr",
    "track",
    "tt",
    "u",
    "ul",
    "var",
    "video",
    "wbr",
    "xmp"
]

class Element:
    def __init__(self, children=[], **kwargs):
        self.tag_name = self.__class__.__name__
        self.children = children
        self.attributes = kwargs
        self.elements = []
        for child in self.children:
            if child.__class__.__name__ in elements:
                self.elements.append(child)
                
        if 'id' not in self.attributes:
            self.attributes['id'] = os.urandom(4).hex()
            
        child_ids = [child.id() for child in self.elements]
        if len(child_ids) != len(set(child_ids)) or self.attributes['id'] in child_ids:
            raise Exception("Duplicate ID")
        del child_ids
        self.attributes['id'] = self.attributes['id'].replace(' ', '_')
            
    def id(self):
        return self.attributes['id']

    def getElementsByTagName(self, tag_name):
        return [child for child in self.children if child.tag_name == tag_name]

    def getElementById(self, id):
        return [child for child in self.children if child.id() == id]

    def render(self):
        return f"""<{self.tag_name}{''.join([((((f' {k}="{v}"' if type(v) == str else f' {k}={v}') if type(k) == str else f' {v}') if type(v) != list else f' {k}={" ".join(v)}') if type(v) in [str, int, bool, list] else f'') for k, v in self.attributes.items()])}>\n{"".join([(child.render() if type(child) != str else child) for child in self.children])}\n</{self.tag_name}>"""

    def render_pretty(self, indent=0):
        return f"""{indent * "  "}<{self.tag_name}{''.join([((((f' {k}="{v}"' if type(v) == str else f' {k}={v}') if type(k) == str else f' {v}') if type(v) != list else f' {k}={" ".join(v)}') if type(v) in [str, int, bool, list] else f'') for k, v in self.attributes.items()])}>\n{"".join([(child.render_pretty(indent + 1) if type(child) != str else f"{(indent + 1) * '  '}{child}") for child in self.children])}\n</{self.tag_name}>"""

els = {}
for element in elements:
    els[element] = type(element, (Element,), {})

class Style:
    def __init__(self, style_dict):
        self.style_dict = style_dict

    def render(self):
        return f"""<style>{"".join([f"{selector} {{{''.join([f'{key}: {value};' for key, value in style.items()])}}}" for selector, style in self.style_dict.items()])}</style>"""
    
    def render_pretty(self, indent=0):
        return f"""{indent * "  "}<style>{"".join([f"{selector} {{{''.join([f'{key}: {value};' for key, value in style.items()])}}}" for selector, style in self.style_dict.items()])}</style>"""

    def __str__(self):
        return self.render()

    def __repr__(self):
        return self.render()
els['style'] = Style

class Accessor:
    def __getattr__(self, name):
        return els[name]

ui = Accessor()