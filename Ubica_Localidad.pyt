# -*- coding: utf-8 -*-

import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Localidad"
        self.alias = "Localidad"

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Selec_Localidad"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param1 = arcpy.Parameter(displayName="Localidad", name="localidad", datatype="GPString", parameterType="Required", direction="Input")
        aprx = arcpy.mp.ArcGISProject('current')
        m = aprx.listMaps("Calles")[0]
        l_localidades = []
        for lyr in m.listLayers():
            if lyr.name == 'Concesion Metro':
                for row in  arcpy.da.SearchCursor(lyr, ['nombre_localidad'], sql_clause= (None,'ORDER BY nombre_localidad')):
                    l_localidades.append(row[0])
        param1.filter.type = "ValueList"
        param1.filter.list = l_localidades
        params = [param1]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        if parameters[0].altered:
           #parameters[1].value = "Hola Que Tal"
           qry1 = "nombre_localidad = '" + parameters[0].value + "'" 
           fc = 'SAP_VariantName'
           fields = ["str_desc", "SAP_VAN_NOMBRECALLE", "SAP_VAN_ID", "SAP_CIUDAD_ID", "SAP_NOMBRECIUDAD"]

        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        import arcpy
        arcpy.env.overwriteOutput = True

        localidad = parameters[0].valueAsText

        # FIltros Querys
        qry1 = "nombre_localidad = " + "'" + str(localidad) + "'" 
        theSql = "GROUP BY SRT_RDESC"
        file_calles = open('calles_aux.csv', 'w')
        file_localidad = open('localidad_aux.csv', 'w')

        aprx = arcpy.mp.ArcGISProject('current')
        m = aprx.listMaps("Calles")[0]
        for lyr in m.listLayers():
            if lyr.name == 'Concesion Metro':
                arcpy.SelectLayerByAttribute_management(lyr,"NEW_SELECTION", qry1)
                extents = []
                with arcpy.da.SearchCursor(lyr, ["Shape@", 'codigo_localidad','nombre_localidad'], qry1) as cur:
                     for row in cur:
                         extents.append(row[0].extent)
                         ext = row[0].extent
                         registro = str(row[1]) + "," + row[2]
                m.extent = extents
                #ext = arcpy.Describe(lyr).extent
                cam = aprx.activeView.camera
                cam.setExtent(ext)
                arcpy.SelectLayerByAttribute_management(lyr.name, "CLEAR_SELECTION")
                file_localidad.write(registro + '\n')
                file_localidad.close
            if lyr.name == 'STR_Street':
                arcpy.AddMessage("ExisteLayer Calle..."+qry1)
                for row in  arcpy.da.SearchCursor(lyr, ['STR_RDESC'], where_clause= qry1, sql_clause= ('DISTINCT', None)):
                    arcpy.AddMessage("Registros Calle...")
                    registro = row[0]
                    file_calles.write(registro + '\n')
        file_calles.close

        return
