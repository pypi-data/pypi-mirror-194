from functools import partial

from sphinx.ext.autosummary import import_by_name, ImportExceptionGroup


def make_pyobj_role(make_node):
    return partial(pyobj_role, make_node)


def pyobj_role(make_node, name, rawtext, text, lineno, inliner, options=None, content=None):
    """Include Python object value, rendering it to text using str.

    Returns 2 part tuple containing list of nodes to insert into the
    document and a list of system messages.  Both are allowed to be
    empty.

    :param make_node: A callable which accepts (rawtext, app, prefixed_name, obj, parent, modname, options) and which returns a node
    :param name: The role name used in the document.
    :param rawtext: The entire markup snippet, with role.
    :param text: The text marked with the role.
    :param lineno: The line number where rawtext appears in the input.
    :param inliner: The inliner instance that called us.
    :param options: Directive options for customization.
    :param content: The directive content for customization.
    """
    if options is None:
        options = {}

    if content is None:
        content = []

    try:
        prefixed_name, obj, parent, modname = import_by_name(text)
    except (ImportError, ImportExceptionGroup):
        msg = inliner.reporter.error("Could not locate Python object {}".format(text), line=lineno)
        prb = inliner.problematic(rawtext, rawtext, msg)
        return [prb], [msg]
    app = inliner.document.settings.env.app
    node = make_node(rawtext, app, prefixed_name, obj, parent, modname, options)
    new_nodes = node if isinstance(node, list) else [node]
    return new_nodes, []


def formatted_role(make_node, inliner, rawtext, text, lineno, options=None):
    if options is None:
        options = {}

    name, _, format_spec = tuple(field.strip() for field in text.partition(","))
    try:
        prefixed_name, obj, parent, modname = import_by_name(name)
    except ImportError:
        message = inliner.reporter.error("Could not locate Python object {}".format(text),
                                         line=lineno)
        problem_node = inliner.problematic(rawtext, rawtext, message)
        new_nodes = [problem_node]
        messages = [message]
    else:
        try:
            formatted_value = format(obj, format_spec)
        except ValueError as value_error:
            message = inliner.reporter.error(
                "Format error in {}: {}".format(text, value_error), line=lineno
            )
            prb = inliner.problematic(rawtext, rawtext, message)
            new_nodes = [prb]
            messages = [message]
        else:
            node = make_node(text=formatted_value, rawsource=rawtext)
            new_nodes = node if isinstance(node, list) else [node]
            messages = []
    return new_nodes, messages