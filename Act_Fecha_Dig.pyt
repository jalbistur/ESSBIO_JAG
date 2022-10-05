# -*- coding: utf-8 -*-

import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Fechadig"
        self.alias = "Fechadig"

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Fecha Digitalizacion"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = None
        """Define parameter definitions"""
        param0 = arcpy.Parameter(displayName="TipoEdicion", name="Tipo_ed", datatype="GPString", parameterType="Required", direction="Input")
        param1 = arcpy.Parameter(displayName="Localidad", name="Localidad", datatype="GPString", parameterType="Required", direction="Input")
        param2 = arcpy.Parameter(displayName="Cod_Inv - Cod_Proyecto", name="Cod_Proyecto", datatype="GPString", parameterType="Required", direction="Input")
     
        fcalles = open('Localidad_aux.csv', 'r')
        ftablas = open('tablas_aux.csv', 'w')

        l_tipoed = ["Cartografia", "Calles"]     
        param0.filter.type = "ValueList"
        param0.filter.list = l_tipoed

        i = 0
        listaloc = []
        for line in fcalles:
            reg  = line.split(",")
            cod_localidad = reg[0]
            nom_localidad = reg[1]
            reglinea = str(cod_localidad) + " - " + nom_localidad
            #listaloc.append(line.strip())
            listaloc.append(reglinea.strip())
        fcalles.close()
        #param1.filter.type = "ValueList"
        #param1.filter.list = listaloc
        param1.value = listaloc[0]
        aprx = arcpy.mp.ArcGISProject('current')
        m = aprx.listMaps("Calles")[0]
        l_proyecto = []
        qry1 = "codigo_localidad = " + str(cod_localidad)
        print ("Rev Tabla BDT")
        for lyr in m.listTables():
            registro = lyr.name
            ftablas.write(registro + '\n')
            if lyr.name == 'BTD_PROYECTO_LOCALIDAD':
                for row in  arcpy.da.SearchCursor(lyr, ['id_inventario','codigo_proyecto'],where_clause = qry1):
                    reg = str(row[0]) + "-" + str(row[1])
                    l_proyecto.append(reg)
        for lyr in m.listTables():
            if lyr.name == 'BTD_INVENTARIO':
                l_proynom = []
                for l in l_proyecto:
                    idproy = l.split("-")[0]
                    codproy = l.split("-")[1]
                    qry2 = "codigo_proyecto = '" + str(codproy) + "'" # + " and id_proyecto = " + str(idproy)
                    for row in  arcpy.da.SearchCursor(lyr, ['id_inventario','codigo_proyecto','nombre_proyecto'],where_clause = qry2):
                        reg = str(row[0]) + "-" + str(row[1] + "-" + row[2])
                        l_proynom.append(reg)
        param2.filter.type = "ValueList"
        param2.filter.list = l_proynom
        params = [param0, param1,param2]

        ftablas.close
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
        from datetime import date
        from datetime import datetime
        
        """The source code of the tool."""
        tipo_edicion = parameters[0].valueAsText
        text_param1 = parameters[2].valueAsText.split("-")
        id_inventario = text_param1[0]
        cod_proyecto = text_param1[1]
        nom_proyecto = text_param1[2]

        qry1 = "id_inventario = " + id_inventario
        fields = ["digitalizado_cb", "digitalizado_ejes_de_calle"]
        fc = "BTD_INVENTARIO"
# Create update cursor for feature class 
        with arcpy.da.UpdateCursor(fc, fields, where_clause = qry1) as cursor:
             for row in cursor:
                if tipo_edicion == 'Cartografia':
                    row[0] = datetime.today()
                if tipo_edicion == 'Calles':
                    row[1] = datetime.today()
                cursor.updateRow(row)
        return
