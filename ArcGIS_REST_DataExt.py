#Import Libraries
import urllib
import os
import arcpy
import time
from datetime import datetime
import os
import shutil

#Creating Folder structure
ISO="AUS"
Year="Y-"+str(datetime.now().year)
Month="M-"+str(datetime.now().month)
Source="ACT"
Format="JSON-Shapefiles"
Cur_dir = os.path.dirname(os.path.realpath(__file__))
prj_dir=Cur_dir+"\\"+ISO+"\\"+Year+"\\"+Month+"\\"+Source+"\\"+Format
if os.path.exists(prj_dir):
    shutil.rmtree(prj_dir)
os.makedirs(prj_dir)
print ("Folder Structure Created")

#From API->JSON->Shapefile
print "Extracting JSON and coverting to shape"

for a,b in zip(range(0,2000,1000), range(1001,3001,1000)):
    URL="http://data.actmapi.act.gov.au/arcgis/rest/services/basemaps/basic/MapServer/49/query?where=OBJECTID%3E"+str(a)+"+AND+OBJECTID%3C"+str(b)+"&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=*&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&resultOffset=&resultRecordCount=&f=pjson"
    URL_open = urllib.urlopen(URL)
    #Reading the JSON response
    JSON_Response = URL_open.read()
    #Storing the JSON file with time information attached
    timestr = time.strftime("%Y%m%d-%H%M%S")
    JSONfile = open(prj_dir+"\\"+timestr+"_Json.json", "wb")
    JSONfile.write(JSON_Response)
    JSONfile.close()
    #Converting JSON to shapefile
    arcpy.JSONToFeatures_conversion(prj_dir+"\\"+timestr+"_Json.json",prj_dir+"\\"+timestr+"_ShapeFile.shp")
print ("."*80)

#Find all the files with extension *.shp
shpfilelist = []
for files in os.listdir(prj_dir):
    if files.endswith(".shp"):
        shpfilelist.append(files)

#Merge all the shapefiles
arcpy.env.workspace = prj_dir
print "Merging Shapefiles"
arcpy.Merge_management(shpfilelist, prj_dir+"\\"+"Merged.shp")

print ("."*80)
print "Extraction Completed Successfully"
