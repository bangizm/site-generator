
# An HTMLNode without a tag will just render as raw text
# An HTMLNode without a value will be assumed to have children
# An HTMLNode without children will be assumed to have a value
# An HTMLNode without props simply won't have any attributes
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag              # ("p", "a", "h1", "h2",)
        self.value = value          # 'string'
        self.children = children    # [HTMLNode(), ...]
        self.props = props          # {"href": "https://www.google.com", ...}

    def __repr__(self):
        return f'HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})'

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return ""

        #print("---debug---->>", " " + " ".join(f'{k}={v!r}' for k,v in self.props.items()))
        html = " " + " ".join(f'{k}={v!r}' for k,v in self.props.items())
        #html = ""
        #for k,v in self.props.items():
        #    html += f' {k}="{v}"'
        return html
 
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        #self.tag = tag       # Required. None is valid.
        #self.value = value   # Required 
        #self.children = None # NO CHILDREN allowed.

    def __repr__(self):
        return f'HTMLNode(tag={self.tag}, value={self.value}, props={self.props})'

    def to_html(self):
        if self.value is None:
            raise ValueError(type(LeafNode()).__name__, ".value==None UNEXPECTED")
        if self.tag is None:
            return f'{self.value}' 
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

        #if self.tag == "a":
        #    return f'<{self.tag}{self.props_to_html}>{self.value}</{self.tag}>'
        #    #return f'<{self.tag} {self.props}>{self.value}</{self.tag}>'
        ##if self.tag in ("p", "a", "h1", "h2",):  #"p", "a", "h1", etc.
        #return f'<{self.tag}>{self.value}</{self.tag}>'
             
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None ):
        super().__init__(tag, None, children, props)
        # tag, children - Required.
        # props - Optional
        # value - EXCLUDED

    def to_html(self):
        if self.tag is None or self.tag == "":
            raise ValueError(type(ParentNode()).__name__, ".tag==None UNEXPECTED")
        if self.children is None:
            raise ValueError(type(ParentNode()).__name__, ".children==None UNEXPECTED")
        # Check if self.children.value is None?
        #if len(self.children)==0:   # should be a list of HTMLNode()'s
        #    raise ValueError(type(ParentNode()).children.__name__, "=[] UNEXPECTED")

        ##### RECURSION ####
        #def conv(child):
        #    if child is None 
        #        return ""
        #    child_str = 
        #    txt = "".join(c.conv() for c in children)
        #    return txt

        #print("_____", self, " <> ", self.children )
        children_str = "".join(c.to_html() for c in self.children)
        #children_str = conv(self.children)
        #children_str = "".join(conv(c) for c in self.children)
        # RETURN string .to_html() and recurse its children
        return f'<{self.tag}{self.props_to_html()}>{children_str}</{self.tag}>'
