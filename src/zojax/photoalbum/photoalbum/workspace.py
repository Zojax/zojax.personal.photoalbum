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

from zojax.photoalbum.album import BasePhotos

from zojax.personal.space.interfaces import IPersonalSpace
from zojax.personal.space.interfaces import IPersonalWorkspaceDescription
from zojax.security.utils import checkPermissionForPrincipal

from interfaces import _, IPersonalPhotosWorkspace, IPersonalPhotosWorkspaceFactory


class PersonalPhotosWorkspace(BasePhotos):
    interface.implements(IPersonalPhotosWorkspace)

    __name__ = u'photos'

    @property
    def space(self):
        return self.__parent__


class PersonalPhotosWorkspaceFactory(object):
    component.adapts(IPersonalSpace)
    interface.implements(IPersonalPhotosWorkspaceFactory)

    title = _(u'Photos')
    description = _(u'Personal photos')
    weight = 10
    name = 'photos'

    def __init__(self, space):
        self.space = space

    def get(self):
        return self.space.get('photos')

    def install(self):
        ws = self.space.get('photos')

        if not IPersonalPhotosWorkspace.providedBy(ws):
            ws = PersonalPhotosWorkspace(
                title="%s's Photos"%self.space.principal.title)
            event.notify(ObjectCreatedEvent(ws))
            removeSecurityProxy(self.space)['photos'] = ws

        return self.space['photos']

    def uninstall(self):
        del self.space['photos']

    def isInstalled(self):
        return 'photos' in self.space

    def isAvailable(self):
        return checkPermissionForPrincipal(
            self.space.principal, 'zojax.PersonalPhotos', self.space)


class PersonalPhotosWorkspaceDescription(object):
    interface.implements(IPersonalWorkspaceDescription)

    name = 'photos'
    title = _(u'Photos')
    description = _(u'Personal photos')

    def createTemp(self, context):
        ws = PersonalPhotosWorkspace()
        ws.__parent__ = context
        return ws
