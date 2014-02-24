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
import os, unittest, doctest
from zojax.layoutform.interfaces import ILayoutFormLayer
from zojax.personal.space.tests.tests import checkPermissionForPrincipal
from zope.app.rotterdam import Rotterdam
from zope.app.security.interfaces import IAuthentication
from zope.app.testing import functional
from zope.app.component.hooks import setSite
from zope.security.management import newInteraction, endInteraction
from zojax.security import utils


zojaxPersonalPhotoalbumLayer = functional.ZCMLLayer(
    os.path.join(os.path.split(__file__)[0], 'ftesting.zcml'),
    __name__, 'zojaxPersonalPhotoalbumLayer', allow_teardown=True)


class IDefaultSkin(ILayoutFormLayer, Rotterdam):
    """ skin """

oldMethod = None


def checkPermissionForPrincipal(principal, permission, object):
    return True


def FunctionalDocFileSuite(*paths, **kw):
    layer = zojaxPersonalPhotoalbumLayer

    globs = kw.setdefault('globs', {})
    globs['http'] = functional.HTTPCaller()
    globs['getRootFolder'] = functional.getRootFolder
    globs['sync'] = functional.sync

    kw['package'] = doctest._normalize_module(kw.get('package'))
    global oldMethod
    oldMethod = utils.checkPermissionForPrincipal.func_code
    utils.checkPermissionForPrincipal.func_code = checkPermissionForPrincipal.func_code

    kwsetUp = kw.get('setUp')

    def setUp(test):
        functional.FunctionalTestSetup().setUp()
        newInteraction()
        root = functional.getRootFolder()
        setSite(root)
        sm = root.getSiteManager()
        auth = sm.getUtility(IAuthentication)
        p = auth.getPrincipal('zope.mgr')
        setattr(root, 'principal', p)
        setattr(root, 'owner', p)
        endInteraction()

    kw['setUp'] = setUp

    kwtearDown = kw.get('tearDown')

    def tearDown(test):
        setSite(None)
        functional.FunctionalTestSetup().tearDown()

    kw['tearDown'] = tearDown

    if 'optionflags' not in kw:
        old = doctest.set_unittest_reportflags(0)
        doctest.set_unittest_reportflags(old)
        kw['optionflags'] = (old | doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)

    suite = doctest.DocFileSuite(*paths, **kw)
    suite.layer = layer
    return suite


def test_suite():
    return unittest.TestSuite((
        FunctionalDocFileSuite("testbrowser.txt"),
    ))
