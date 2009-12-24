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
from zope import interface, schema
from zope.i18nmessageid import MessageFactory
from zojax.content.space.interfaces import IWorkspace
from zojax.blogger.interfaces import IBlog, IBlogPost, IBloggerWorkspaceFactory

_ = MessageFactory('zojax.content.space')


class IPersonalBlogWorkspace(IBlog, IWorkspace):
    """ blog workspace """


class IPersonalBlogWorkspaceFactory(IBloggerWorkspaceFactory):
    """Personal blogger workspace factory."""
