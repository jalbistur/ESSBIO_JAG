# -*- coding: utf-8 -*-

import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Tool"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = None
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
 
        qry1 = "str_id > 0"
        fields = ["str_rdesc", "str_ldesc", "str_lff", "str_ltt", "str_rff", "str_rtt"]
        fc = 'STR_Street'
        lyr_ptos = 'STR_Node'
# Create update cursor for feature class 
        aprx = arcpy.mp.ArcGISProject('current')
        m = aprx.listMaps("Calles")[0]
        arcpy.env.overwriteOutput = True

        for lyr in m.listLayers():
            if lyr.name == 'STR_Street': # and arcpy.GetCount_management(lyr) == 1:
                numsel = arcpy.GetCount_management(lyr)
                regsel = "R" + str(numsel)
                if regsel == "R1":
                   pointList = []
                   with  arcpy.da.UpdateCursor(lyr, ["OID@", "SHAPE@"]) as cursor:
                       for row in cursor:
                           arcpy.AddMessage("Registros seleccionados ... " + str(numsel))
                           print("Feature {0}:".format(row[0]))

                           #Set start point
                           startpt = row[1].firstPoint

                           #Set Start coordinates
                           startx = startpt.X
                           starty = startpt.Y
                           point = arcpy.Point(startx, starty)
                           point_geom = arcpy.PointGeometry(point)
                           arcpy.CopyFeatures_management([point_geom], "Nodos_Calle")

                           STR_Node_2_ = "Calle\\STR_Node"
                           STR_Node_3_ = point_geom
                           # Process: Select Layer By Location (Select Layer By Location) (management)
                           STR_Node, Output_Layer_Names, Count = arcpy.management.SelectLayerByLocation(in_layer=[STR_Node_2_], overlap_type="WITHIN_A_DISTANCE", select_features=STR_Node_3_, search_distance="1 Meters", selection_type="NEW_SELECTION", invert_spatial_relationship="NOT_INVERT")

                           regsel1 = "S" + str(arcpy.GetCount_management(lyr_ptos))
                           arcpy.AddMessage("Nodos Seleccionados..."+str(regsel1))

                           #Set end point
                           endpt = row[1].lastPoint
                           #Set End coordinates
                           endx = endpt.X
                           endy = endpt.Y
                           point = arcpy.Point(endx, endy)
                           point_geom = arcpy.PointGeometry(point)
                           arcpy.CopyFeatures_management([point_geom], "Nodos_Calle")

                           STR_Node_3_ = point_geom
                           # Process: Select Layer By Location (Select Layer By Location) (management)
                           STR_Node, Output_Layer_Names, Count = arcpy.management.SelectLayerByLocation(in_layer=[STR_Node_2_], overlap_type="WITHIN_A_DISTANCE", select_features=STR_Node_3_, search_distance="1 Meters", selection_type="NEW_SELECTION", invert_spatial_relationship="NOT_INVERT")

                           regsel2 = "S" + str(arcpy.GetCount_management(lyr_ptos))
                           arcpy.AddMessage("Nodos Seleccionados..."+str(regsel2))

                           #arcpy.SelectLayerByLocation_management(lyr_ptos, 'WITHIN_A_DISTANCE', 'Nodos_Calle', '2')

                           arcpy.AddMessage("Nodos Inicio Termino x:" + str(startx) + ",y:"+ str(starty))
                           arcpy.AddMessage("Regsel 1 :" + str(regsel1))
                           arcpy.AddMessage("Regsel 2 :" + str(regsel2))
                       
                       pointList = [[startx, starty],[endx, endy]]
                       # Create an empty Point object
                       point = arcpy.Point()
                       # A list to hold the PointGeometry objects
                       pointGeometryList = []

                       fc = "STR_Node"

                       # A list of values that will be used to construct new rows
                       row_values = []
                       if regsel1 == "S0":
                          arcpy.AddMessage("Agrega Nodo x:" + str(startx) + ",y:"+ str(starty))
                          row_values.append((startx, starty))

                       if regsel2 == "S0":
                          arcpy.AddMessage("Agrega Nodo x:" + str(endx) + ",y:"+ str(endy))
                          row_values.append((endx, endy))

                       # Open an InsertCursor
                       cursor = arcpy.da.InsertCursor(fc,['SHAPE@X', 'SHAPE@Y'])

                       # Insert new rows that include the county name and a x,y coordinate
                       #  pair that represents the county center
                       for row in row_values:
                           cursor.insertRow(row)
                       # Delete cursor object
                       del cursor
                else:
                   arcpy.AddMessage("Mas de 1 Registros seleccionados ... " + str(numsel))
        return
