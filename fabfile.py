#
import fnmatch
import glob
import os
import urllib
import xml.etree.ElementTree as etree

from fabric import api as fab

PROJECT_DIR = os.path.dirname(__file__)
DB_NAME = 'osopen_data'
DB_USER = 'osopen'


def get_data():
    url = 'http://data.inspire.landregistry.gov.uk/'
    xml_string = urllib.urlopen(url).read()
    element = etree.XML(xml_string)
    f = os.path.join(PROJECT_DIR, 'data', 'Land_Registry_Cadastral_Parcels.gml')
    for content in element.findall('{http://s3.amazonaws.com/doc/2006-03-01/}Contents'):
        k = content.find('{http://s3.amazonaws.com/doc/2006-03-01/}Key').text
        if not k.endswith('.zip'):
            continue
        with fab.lcd(os.path.join(PROJECT_DIR, 'data')):
            fab.local('wget http://data.inspire.landregistry.gov.uk/' + k)
            fab.local('unzip -o {0}'.format(k))
            fab.local('ogr2ogr -f "ESRI Shapefile" {0} {1}'.format(k[:-3] + 'shp', f))
            fab.local('rm -f Land_Registry_Cadastral_Parcels.gml')
            fab.local('rm -f ' + k)

def import_shp():
    template = 'shp2pgsql -d -s 27700:4326 -I {0} cadastral_parcel | psql -d {1} -U {2} -h localhost'
    inpath = os.path.join(PROJECT_DIR, 'data')
    for root, dirnames, filenames in os.walk(inpath):
        for filename in fnmatch.filter(filenames, '*.shp'):
            with fab.lcd(root):
                fab.local(template.format(filename, DB_NAME, DB_USER))
                template = 'shp2pgsql -a -s 27700:4326 {0} cadastral_parcel | psql -d {1} -U {2} -h localhost'
