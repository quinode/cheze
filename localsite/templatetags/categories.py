from django.template import Library, Node, Variable, VariableDoesNotExist
from product.models import Category
import logging

log = logging.getLogger('shop.templatetags')

try:
    from xml.etree.ElementTree import Element, SubElement, tostring
except ImportError:
    from elementtree.ElementTree import Element, SubElement, tostring

register = Library()

def recurse_for_children(current_node, parent_node, active_categories = [], show_empty=True, deep = -1, current_deep = 0):
    child_count = current_node.child.count()

    if show_empty or child_count > 0 or current_node.product_set.count() > 0:
        temp_parent = SubElement(parent_node, 'li')
        attrs = {'href': current_node.get_absolute_url()}
        if current_node in active_categories:
            attrs["class"] = "current" 
        link = SubElement(temp_parent, 'a', attrs)
        link.text = current_node.translated_name()
        if current_deep == deep: return
        if not child_count: return
        new_parent = SubElement(temp_parent, 'ul')
        children = current_node.child.all()
        for child in children:
            recurse_for_children(child, new_parent, active_categories, show_empty, deep, current_deep + 1)

class SubcategoryTree(Node):
    def __init__(self, active = None, from_level = 0, deep = -1, select_parents = 0):
        self.active = active
        self.from_level = int(from_level)
        self.deep = int(deep)
        self.select_parents = bool(select_parents)

    def render(self, context):
        root = Element("ul")
        active_categories = []
        root_categories = None
        if self.active:
            active_cat = Variable(self.active).resolve(context)
            active_categories = [active_cat]
            if self.select_parents: active_categories.extend(active_cat.parents())
            if self.from_level:
                parents = active_cat.parents()
                parents.append(active_cat)
                index = self.from_level - 1
                if index > len(parents): return ("")
                root_categories = parents[index].child.all()
            else:
                root_categories = Category.objects.root_categories()
        else:
            root_categories = Category.objects.root_categories()
        for cats in root_categories:
            recurse_for_children(cats, root, active_categories, deep = self.deep)
        return tostring(root, 'utf-8')        

@register.tag                
def categories(parser, token):
    """ 
    Creates an unnumbered list of the categories. It allows to specify deep and start level.
    If select_parents all parent categories would have class="current" - this is suitable for main categories.

    Examples: 

    {% categories %}
    {% categories active=category from_level=1%}
    {% categories active=category deep=0 select_parents=1 %}
    """ 
    kwargs = {}
    for bit in token.split_contents()[1:]:
        arg, val = bit.split("=")
        kwargs[str(arg)] = val
    return (SubcategoryTree(**kwargs))