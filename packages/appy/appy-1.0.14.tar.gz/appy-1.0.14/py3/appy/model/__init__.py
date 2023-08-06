'''Management of the model behind a Appy application'''

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Copyright (C) 2007-2023 Gaetan Delannay

# This file is part of Appy.

# Appy is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.

# Appy is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with
# Appy. If not, see <http://www.gnu.org/licenses/>.

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import pathlib

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Config:
    '''Model configuration'''

    def __init__(self):
        # The "root" classes are those that will get their menu in the user
        # interface. Put their names in the list below. If you leave the list
        # empty, all classes will be considered root classes (the default). If
        # rootClasses is None, no class will be considered as root.
        self.rootClasses = []
        # People having one of these roles will be able to create instances
        # of classes defined in your application.
        self.defaultCreators = ['Manager']
        # Roles in use in a Appy application are identified at make time from
        # workflows or class attributes like "creators": it is not needed to
        # declare them somewhere. If you want roles that Appy will be unable to
        # detect, add them in the following list. Every role can be a Role
        # instance or a string.
        self.additionalRoles = []
        # When marshalling File fields via the XML layout, binary content is, by
        # default, included as a series of fixed size Base64-encoded chunks
        # wrapped in "part" tags. If the target site has access to this site's
        # filesystem, an alternative is to marshall the disk location of the
        # binary file instead of its content. If you want to enable this latter
        # behaviour, set the following attribute to False.
        self.marshallBinaries = True

    def set(self, appFolder):
        '''Sets site-specific configuration elements'''
        # The absolute path to the app as a pathlib.Path instance
        self.appPath = pathlib.Path(appFolder)
        # The application name
        self.appName = self.appPath.name

    def get(self, config, logger=None, appOnly=False):
        '''Creates and returns a Model instance (see below)'''
        from appy.model.loader import Loader
        return Loader(self, config, logger, appOnly).run()
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
