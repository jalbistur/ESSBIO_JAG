# -*- coding: utf-8 -*-

import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "DatosCalle"
        self.alias = "DatosCalle"

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Datos_Calles"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param1 = arcpy.Parameter(displayName="Calle", name="Calle", datatype="GPString", parameterType="Required", direction="Input")
        param2 = arcpy.Parameter(displayName="Inicio_Izquierda", name="Inicio_Izquierda", datatype="GPlong", parameterType="Required", direction="Input")
        param3 = arcpy.Parameter(displayName="Fin_Izquierda", name="Fin_Izquierda", datatype="GPlong", parameterType="Required", direction="Input")
        param4 = arcpy.Parameter(displayName="Inicio_Derecha", name="Inicio_Derecha", datatype="GPlong", parameterType="Required", direction="Input")
        param5 = arcpy.Parameter(displayName="Fin_Derecha", name="Fin_Derecha", datatype="GPlong", parameterType="Required", direction="Input")
        #param6 = arcpy.Parameter(displayName="Msg Ejecución", name="msg_ejec", datatype="GPtext", parameterType="Required", direction="Input")

        fcalles = open('calles_aux.csv', 'r')
        i = 0
        listacalles = []
        for line in fcalles:
            listacalles.append(line.strip())
        fcalles.close()
        param1.filter.type = "ValueList"
        param1.filter.list = listacalles

        params = [param1,param2, param3, param4, param5]
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
        nom_calle = parameters[0].valueAsText
        izq_ini = parameters[1].value
        izq_fin = parameters[2].value
        der_ini = parameters[3].value
        der_fin = parameters[4].value

        qry1 = "str_id > 0"
        fields = ["OID@", "SHAPE@","str_rdesc", "str_ldesc", "str_lff", "str_ltt", "str_rff", "str_rtt","pais", "str_nodeinit", "str_nodeend"]
        fc = 'STR_Street'
# Create update cursor for feature class 
        aprx = arcpy.mp.ArcGISProject('current')
        m = aprx.listMaps("Calles")[0]

        nodo_inicio = 0
        nodo_fin = 0
        for lyr in m.listLayers():
            if lyr.name == 'STR_Street': # and arcpy.GetCount_management(lyr) == 1:
                numsel = arcpy.GetCount_management(lyr)
                regsel = "R" + str(numsel)
                with  arcpy.da.UpdateCursor(lyr, fields) as cursor:
                    for row in cursor:
                        startpt = row[1].firstPoint
                        endpt = row[1].lastPoint
                        startx = startpt.X
                        starty = startpt.Y
                        endx = endpt.X
                        endy = endpt.Y
                        arcpy.AddMessage("Nodo ... " + str(startx) + " " + str(starty))

                        point = arcpy.Point(startx, starty)
                        point_geom = arcpy.PointGeometry(point)

                        lyr_in = "Calle\\STR_Node"
                        lyr_sel = point_geom
                        STR_Node, Output_Layer_Names, Count = arcpy.management.SelectLayerByLocation(in_layer=[lyr_in], overlap_type="WITHIN_A_DISTANCE", select_features=lyr_sel, search_distance="1 Meters", selection_type="NEW_SELECTION", invert_spatial_relationship="NOT_INVERT")

                        for row1 in  arcpy.da.SearchCursor(lyr_in, ['objectid']):
                            arcpy.AddMessage("Registros Calle...")
                            nodo_inicio = row1[0]

                        point = arcpy.Point(endx, endy)
                        point_geom = arcpy.PointGeometry(point)
                        lyr_sel = point_geom
                        STR_Node, Output_Layer_Names, Count = arcpy.management.SelectLayerByLocation(in_layer=[lyr_in], overlap_type="WITHIN_A_DISTANCE", select_features=lyr_sel, search_distance="1 Meters", selection_type="NEW_SELECTION", invert_spatial_relationship="NOT_INVERT")

                        for row1 in  arcpy.da.SearchCursor(lyr_in, ['objectid']):
                            arcpy.AddMessage("Registros Calle...")
                            nodo_fin = row1[0]

                        row[2] = nom_calle
                        row[3] = nom_calle
                        row[4] = izq_ini
                        row[5] = izq_fin
                        row[6] = der_ini
                        row[7] = der_fin
                        row[8] = "CHL"
                        row[9] = nodo_inicio
                        row[10] = nodo_fin
                        cursor.updateRow(row)
        return
