# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SaveAttributes
                                 A QGIS plugin
 This plugin saves the attribute of the selected....
                             -------------------
        begin                : 2018-11-25
        copyright            : (C) 2018 by FernandoB
        email                : mail@mail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load SaveAttributes class from file SaveAttributes.

    :param iface: A QGIS interface instance.
    :type iface: QgisInterface
    """
    #
    from .save_attributes import SaveAttributes
    return SaveAttributes(iface)
