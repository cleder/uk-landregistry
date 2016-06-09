# UK Landregistry Data

Download UK Land Registry INSPIRE Index Polygons and import them into a spatial db.

# Usage

Install Fabric and execute

    fab get_data

to download the data and convert it into shapefiles.

Execute

    fab import_shp

to import the data into a postgis database.

More information about the data at https://www.gov.uk/guidance/inspire-index-polygons-spatial-data
