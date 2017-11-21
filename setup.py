#!/usr/bin/env python

#  Copyright (c) 2014 INFN - "Istituto Nazionale di Fisica Nucleare" - Italy
#  All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License. 

import sys, os, os.path, shlex, subprocess
from subprocess import Popen as execScript
from distutils.core import setup
from distutils.command.bdist_rpm import bdist_rpm as _bdist_rpm

pkg_name = 'openstack-auth-cedc'
pkg_version = '1.2.0'
pkg_release = '7'

source_items = "setup.py src config"

class bdist_rpm(_bdist_rpm):

    def run(self):

        topdir = os.path.join(os.getcwd(), self.bdist_base, 'rpmbuild')
        builddir = os.path.join(topdir, 'BUILD')
        srcdir = os.path.join(topdir, 'SOURCES')
        specdir = os.path.join(topdir, 'SPECS')
        rpmdir = os.path.join(topdir, 'RPMS')
        srpmdir = os.path.join(topdir, 'SRPMS')
        
        cmdline = "mkdir -p %s %s %s %s %s" % (builddir, srcdir, specdir, rpmdir, srpmdir)
        execScript(shlex.split(cmdline)).communicate()
        
        cmdline = "tar -zcf %s %s" % (os.path.join(srcdir, pkg_name + '.tar.gz'), source_items)
        execScript(shlex.split(cmdline)).communicate()
        
        specOut = open(os.path.join(specdir, pkg_name + '.spec'),'w')
        cmdline = "sed -e 's|@PKGVERSION@|%s|g' -e 's|@PKGRELEASE@|%s|g' project/%s.spec.in" % (pkg_version, pkg_release, pkg_name)
        execScript(shlex.split(cmdline), stdout=specOut, stderr=sys.stderr).communicate()
        specOut.close()
        
        cmdline = "rpmbuild -ba --define '_topdir %s' %s.spec" % (topdir, os.path.join(specdir, pkg_name))
        execScript(shlex.split(cmdline)).communicate()

os_main_dir = 'usr/share/openstack-dashboard/openstack_dashboard/'
templates_dir = os_main_dir + 'templates'
img_dir = os_main_dir + 'static/dashboard/img'
themes_dir = os_main_dir + 'themes'

logo_list = [
    'src/templates/logoCloudVeneto.ico',
    'src/templates/logoCloudVeneto.png',
    'src/templates/logoCloudVenetoStrip.png'
]

setup(
      name=pkg_name,
      version=pkg_version,
      description='Shibboleth-Openstack integrations',
      long_description='''Shibboleth-Openstack integrations''',
      license='Apache Software License',
      author_email='CREAM group <cream-support@lists.infn.it>',
      packages=[ 'dashboard_conf' ],
      package_dir = {'': 'src'},
      data_files=[
                  (templates_dir, ['src/templates/aup.html']),
                  (img_dir, logo_list),
                  ('etc/openstack-auth-shib', ['config/idem-template-metadata.xml']),
                  ('etc/openstack-auth-shib/notifications', ['config/notifications_en.txt']),
                  (themes_dir + '/cedc/static', 
                    [ 'src/themes/cedc/static/_styles.scss', 'src/themes/cedc/static/_variables.scss']),
                  (themes_dir + '/cedc/templates', 
                    ['src/themes/cedc/templates/_aai_status_style.html', 'src/themes/cedc/templates/_aai_registr_style.html']),
                  (themes_dir + '/cedc/templates/auth', ['src/themes/cedc/templates/auth/_splash.html']),
                  (themes_dir + '/cedc/templates/header', ['src/themes/cedc/templates/header/_brand.html']),
                 ],
      cmdclass={'bdist_rpm': bdist_rpm}
     )


