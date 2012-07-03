# -*- encoding: utf-8 -*-
from distutils.core import setup
import os, glob

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name="lightdm_pywebkit_greeter",
      version='0.1.0',
      maintainer="lamikae",
      maintainer_email="",
      license="GPL-2",
      description="LightDM Webkit Greeter written in Python",
      long_description=read('README'),
      packages=["lightdm_pywebkit_greeter"],
      package_dir={'':"src"},
      data_files=[('share/xgreeters',['data/lightdm-pywebkit-greeter.desktop']),
                  ('share/lightdm_pywebkit_greeter', glob.glob('assets/*.*')),
                  ],
                  )
