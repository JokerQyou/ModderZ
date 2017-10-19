# coding: utf-8
import os
import sys
pkg_dir = os.path.join(os.path.dirname(__file__), 'pkgs')
sys.path.append(os.path.join(pkg_dir, 'win32'))
sys.path.append(os.path.join(pkg_dir, 'win32', 'lib'))
sys.path.append(os.path.join(pkg_dir, 'pythonwin'))

# Required by pywintypes import
os.environ['PATH'] = ';'.join([
    os.environ['PATH'], os.path.join(pkg_dir, 'pypiwin32_system32')
])
