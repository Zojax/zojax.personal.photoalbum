##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from zope import interface, component, event
from zope.security import checkPermission
from zope.lifecycleevent import ObjectCreatedEvent
from zope.lifecycleevent import ObjectModifiedEvent
from zope.security.proxy import removeSecurityProxy

from zojax.blogger.blog import BaseBlog
from zojax.blogger.tags import BlogTags
from zojax.blogger.category import CategoryContainer

from zojax.personal.space.interfaces import IPersonalSpace
from zojax.personal.space.interfaces import IPersonalWorkspaceDescription
from zojax.security.utils import checkPermissionForPrincipal

from interfaces import _, IPersonalBlogWorkspace, IPersonalBlogWorkspaceFactory


class PersonalBlogWorkspace(BaseBlog):
    interface.implements(IPersonalBlogWorkspace)

    __name__ = u'blog'

    @property
    def space(self):
        return self.__parent__


class PersonalBlogWorkspaceFactory(object):
    component.adapts(IPersonalSpace)
    interface.implements(IPersonalBlogWorkspaceFactory)

    title = _(u'Blog')
    description = _(u'Personal blog')
    weight = 10
    name = 'blog'

    def __init__(self, space):
        self.space = space

    def get(self):
        return self.space.get('blog')

    def install(self):
        ws = self.space.get('blog')

        if not IPersonalBlogWorkspace.providedBy(ws):
            ws = PersonalBlogWorkspace(
                title="%s's Blog"%self.space.principal.title)
            event.notify(ObjectCreatedEvent(ws))
            removeSecurityProxy(self.space)['blog'] = ws

        return self.space['blog']

    def uninstall(self):
        del self.space['blog']

    def isInstalled(self):
        return 'blog' in self.space

    def isAvailable(self):
        return checkPermissionForPrincipal(
            self.space.principal, 'zojax.PersonalBlog', self.space)


class PersonalBlogWorkspaceDescription(object):
    interface.implements(IPersonalWorkspaceDescription)

    name = 'blog'
    title = _(u'Blog')
    description = _(u'Personal blog')

    def createTemp(self, context):
        ws = PersonalBlogWorkspace()
        ws.__parent__ = context

        try:
            ws[u'tags'] = BlogTags()
        except:
            pass

        try:
            ws[u'category'] = CategoryContainer()
        except:
            pass

        return ws
