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
from zope import interface, component
from zope.security import checkPermission
from zope.traversing.browser import absoluteURL
from zojax.blogger.interfaces import IBlogPost
from zojax.personal.content.interfaces import IContentWorkspace
from zojax.personal.blogger.interfaces import IPersonalBlogWorkspace
from zojax.blogger.interfaces import _

from interfaces import IWritePostAction


class WritePostAction(object):
    interface.implements(IWritePostAction)
    component.adapts(IPersonalBlogWorkspace, interface.Interface)

    weight = 100
    title = _(u'Write a blog post')

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def url(self):
        ws = IContentWorkspace(self.request.principal, None)
        return '%s/content.blogpost/create.html'%(absoluteURL(ws, self.request))

    def isAvailable(self):
        if not checkPermission('zojax.AddBlogPost', self.context.space):
            return False

        ws = IContentWorkspace(self.request.principal, None)
        if ws is not None:
            return True

        return False


class WritePostActionPost(WritePostAction):
    interface.implements(IWritePostAction)
    component.adapts(IBlogPost, interface.Interface)

    def isAvailable(self):
        workspace = self.context.__parent__

        if not IPersonalBlogWorkspace.providedBy(workspace):
            return False

        if not checkPermission('zojax.AddBlogPost', workspace.space):
            return False

        ws = IContentWorkspace(self.request.principal, None)
        if ws is not None:
            return True

        return False
