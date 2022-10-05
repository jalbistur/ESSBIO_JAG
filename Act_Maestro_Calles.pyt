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
        self.label = "Crea Nombre Calles"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param1 = arcpy.Parameter(displayName="Nombre Calle", name="nom_callle", datatype="GPString", parameterType="Required", direction="Input")
        param2 = arcpy.Parameter(displayName="Nombre SIG", name="master_name", datatype="GPString", parameterType="Optional", direction="Output")
        param3 = arcpy.Parameter(displayName="Nombre SAP", name="varian_name", datatype="GPString", parameterType="Optional", direction="Output")
        param4 = arcpy.Parameter(displayName="Calle-Ciudad SAP", name="calle_ciudad", datatype="GPString", parameterType="Required", direction="Input")

        param4.filter.type = "ValueList"
        param4.filter.list = []

        params = [param1, param2, param3,param4]
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
           qry1 = "SAP_VAN_NOMBRECALLE = '" + parameters[0].value + "'" 
           fc = 'SAP_VariantName'
           fields = ["STR_MAN_ID", "SAP_VAN_NOMBRECALLE", "SAP_VAN_ID", "SAP_CIUDAD_ID", "SAP_NOMBRECIUDAD"]

# Create update cursor for feature class 
           master_name = "No Existe"
           sap_name = "No Existe"
           lista_calle = []
           with arcpy.da.SearchCursor(fc, fields, where_clause = qry1) as cursor:
                for row in cursor:
                    regl = str(row[3]) + "-" + row[4]
                    lista_calle.append(regl)
                    sap_name = row[1]
                    if row[0] > 0:
                       master_name = row[1]
           parameters[1].value = master_name
           parameters[2].value = sap_name
           parameters[3].filter.list = lista_calle
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        parameters[1] = "Hola Que Tal"
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        nom_calle = parameters[0].valueAsText
        existe_master = parameters[1].valueAsText
        existe_sap = parameters[2].valueAsText
        fc = 'STR_MasterName'
        
        for row  in arcpy.da.SearchCursor(fc, ['str_man_id'], sql_clause= (None,'ORDER BY str_man_id ')):
            str_man_id = row[0]
        str_man_id = str_man_id + 1

        fields = ["str_man_id","str_man_nombrecalle"]
        curinsert = arcpy.da.InsertCursor('STR_MasterName', fields)
        if existe_master != "No_Existe" :
           curinsert.insertRow((str_man_id, nom_calle))
        #"""The source code of the tool."""
        del curinsert

        return
