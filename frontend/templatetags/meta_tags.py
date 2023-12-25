import warnings
from collections import OrderedDict

from django import template
from django.apps import apps
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()

from django.conf import settings as django_settings
from django.utils.translation import gettext_lazy as _

META_SITE_PROTOCOL = None
META_SITE_DOMAIN = None
META_SITE_TYPE = None
META_SITE_NAME = None
META_INCLUDE_KEYWORDS = []
META_DEFAULT_KEYWORDS = []
META_IMAGE_URL = django_settings.STATIC_URL
META_USE_OG_PROPERTIES = False
META_USE_TWITTER_PROPERTIES = False
META_USE_FACEBOOK_PROPERTIES = False
META_USE_SCHEMAORG_PROPERTIES = False
META_USE_JSON_LD_SCHEMA = False
META_USE_SITES = False
META_USE_TITLE_TAG = False
META_OG_NAMESPACES = None


OBJECT_TYPES = (
    ("Article", _("Article")),
    ("Website", _("Website")),
)
TWITTER_TYPES = (
    ("summary", _("Summary Card")),
    ("summary_large_image", _("Summary Card with Large Image")),
    ("product", _("Product")),
    ("photo", _("Photo")),
    ("player", _("Player")),
    ("app", _("App")),
)
FB_TYPES = OBJECT_TYPES
SCHEMAORG_TYPES = (
    ("Article", _("Article")),
    ("Blog", _("Blog")),
    ("WebPage", _("Page")),
    ("WebSite", _("WebSite")),
    ("Event", _("Event")),
    ("Product", _("Product")),
    ("Place", _("Place")),
    ("Person", _("Person")),
    ("Book", _("Book")),
    ("LocalBusiness", _("LocalBusiness")),
    ("Organization", _("Organization")),
    ("Review", _("Review")),
)

META_OG_SECURE_URL_ITEMS = ("image", "audio", "video")
META_DEFAULT_IMAGE = ""
META_DEFAULT_TYPE = OBJECT_TYPES[0][0]
META_FB_TYPE = OBJECT_TYPES[0][0]
META_FB_TYPES = FB_TYPES
META_FB_APPID = ""
META_FB_PROFILE_ID = ""
META_FB_PUBLISHER = ""
META_FB_AUTHOR_URL = ""
META_FB_PAGES = ""
META_TWITTER_TYPE = TWITTER_TYPES[0][0]
META_TWITTER_TYPES = TWITTER_TYPES
META_TWITTER_SITE = ""
META_TWITTER_AUTHOR = ""
META_SCHEMAORG_TYPE = SCHEMAORG_TYPES[0][0]
META_SCHEMAORG_TYPES = SCHEMAORG_TYPES

params = {param: value for param, value in locals().items() if param.startswith("META_")}


def get_setting(name):
    """Get setting value from django settings with fallback to globals defaults."""
    from django.conf import settings

    return getattr(settings, "META_%s" % name, params["META_%s" % name])

@register.simple_tag
def meta(name, content):
    """
    Generates a meta tag according to the following markup:

    <meta name="{name}" content="{content}">

    :param name: meta name
    :param content: content value
    """
    return custom_meta("name", name, content)


@register.simple_tag
def custom_meta(attr, name, content):
    """
    Generates a custom meta tag:

    <meta {attr}="{name}" content="{content}">

    :param attr: meta attribute name
    :param name: meta name
    :param content: content value
    """
    return '<meta {attr}="{name}" content="{content}">'.format(
        attr=escape(attr), name=escape(name), content=escape(content)
    )


@register.simple_tag
def meta_list(name, lst):
    """
    Renders in a single meta a list of values (e.g.: keywords list)

    :param name: meta name
    :param lst: values
    """
    try:
        return custom_meta("name", name, ", ".join(lst))
    except Exception:
        return ""


@register.simple_tag
def meta_extras(extra_props):
    """
    Generates the markup for a list of meta tags

    Each key,value paur is passed to :py:func:meta to generate the markup

    :param extra_props: dictionary of additional meta tags
    """
    if not extra_props:
        return ""
    return " ".join(
        [
            meta(name, extra_props[name]) if extra_props[name] else ""
            for name in extra_props
        ]
    )


@register.simple_tag
def custom_meta_extras(extra_custom_props):
    """
    Generates the markup for a list of custom meta tags

    Each tuple is passed to :py:func:custom_meta to generate the markup

    :param extra_custom_props: list of tuple of additional meta tags
    """
    if not extra_custom_props:
        return ""
    return " ".join(
        [
            custom_meta(name_key, name_value, content) if content else ""
            for name_key, name_value, content in extra_custom_props
        ]
    )


@register.simple_tag
def title_prop(value):
    """
    Title tag

    :param value: title value
    """
    return "<title>%s</title>" % escape(value)


@register.simple_tag
def generic_prop(namespace, name, value):
    """
    Generic property setter that allows to create custom namespaced meta
    e.g.: fb:profile_id.
    """
    return custom_meta("property", "{}:{}".format(namespace, name), value)


@register.simple_tag
def og_prop(name, value):
    """
    Generic OpenGraph property

    :param name: property name (without 'og:' namespace)
    :param value: property value
    """
    if (
        not isinstance(value, dict)
        and name in get_setting("OG_SECURE_URL_ITEMS")
        and value.startswith("https")
    ):
        data = {name: value, "%s:secure_url" % name: value}
    elif not isinstance(value, dict):
        data = {
            name: value,
        }
    else:
        data = {"{}:{}".format(name, key): val for key, val in value.items()}
    data = OrderedDict(sorted(data.items()))
    content = [custom_meta("property", "og:%s" % key, val) for key, val in data.items()]
    return "\n".join(content)


@register.simple_tag
def facebook_prop(name, value):
    """
    Generic Facebook property

    :param name: property name (without 'fb:' namespace)
    :param value: property value
    """
    return custom_meta("property", "fb:%s" % name, value)


@register.simple_tag
def twitter_prop(name, value):
    """
    Generic Twitter property

    :param name: property name (without 'twitter:' namespace)
    :param value: property value
    """
    return custom_meta("name", "twitter:%s" % name, value)


@register.simple_tag
def schemaorg_prop(name, value):
    """
    Generic Schema.org property

    :param name: property name
    :param value: property value
    """
    return custom_meta("itemprop", name, value)


@register.simple_tag
def schemaorg_html_scope(value):
    """
    This is meant to be used as attribute to html / body or other tags to
    define schema.org type

    :param value: declared scope
    """
    return ' itemscope itemtype="https://schema.org/%s" ' % escape(value)


@register.simple_tag
def schemaorg_scope(value):
    """
    Alias for googleplus_html_scope

    :param value: declared scope
    """
    return schemaorg_html_scope(value)


@register.simple_tag
def googleplus_prop(name, value):
    """
    Legacy Google+ property
    """
    warnings.warn(
        "googleplus_prop will be removed in version 3.0",
        PendingDeprecationWarning,
        stacklevel=2,
    )
    return schemaorg_prop(name, value)


@register.simple_tag
def googleplus_html_scope(value):
    """
    Legacy Google+ scope
    """
    warnings.warn(
        "googleplus_html_scope will be removed in version 3.0",
        PendingDeprecationWarning,
        stacklevel=2,
    )
    return schemaorg_html_scope(value)


@register.simple_tag
def googleplus_scope(value):
    """
    Legacy Google+ scope
    """
    warnings.warn(
        "googleplus_scope will be removed in version 3.0",
        PendingDeprecationWarning,
        stacklevel=2,
    )
    return schemaorg_html_scope(value)


@register.simple_tag(takes_context=True)
def meta_namespaces(context):
    """
    Include OG namespaces. To be used in the <head> tag.
    """
    # do nothing if meta is not in context
    if not context.get("meta"):
        return ""

    meta = context["meta"]
    namespaces = ["og: http://ogp.me/ns#"]

    # add Facebook namespace
    if meta.use_facebook:
        namespaces.append("fb: http://ogp.me/ns/fb#")

    # add custom namespaces
    # needs to be after Facebook
    if meta.custom_namespace:
        custom_namespaces = meta.custom_namespace
        if isinstance(meta.custom_namespace, str):
            custom_namespaces = [meta.custom_namespace]
        for ns in custom_namespaces:
            custom_namespace = "{0}: http://ogp.me/ns/{0}#".format(ns)
            namespaces.append(custom_namespace)

    return mark_safe(' prefix="{}"'.format(" ".join(namespaces)))


@register.simple_tag(takes_context=True)
def meta_namespaces_schemaorg(context):
    """
    Include Schema.org attributes. To be used in the <html> or <body> tag.
    """
    # do nothing if meta is not in context or if G+ is not enabled
    if not context.get("meta") or not context["meta"].use_schemaorg:
        return ""
    return mark_safe(
        ' itemscope itemtype="https://schema.org/{}" '.format(
            context["meta"].schemaorg_type
        )
    )


@register.simple_tag(takes_context=True)
def meta_namespaces_gplus(context):
    """
    Legacy Google+ attributes.
    """
    warnings.warn(
        "meta_namespaces_gplus will be removed in version 3.0",
        PendingDeprecationWarning,
        stacklevel=2,
    )
    return meta_namespaces_schemaorg(context)
