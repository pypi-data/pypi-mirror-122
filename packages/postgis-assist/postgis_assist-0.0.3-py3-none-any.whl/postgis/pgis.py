from postgis.ps import ps 
from osgeo import gdal, ogr
import os, zipfile, tempfile

class pgis(ps):
    def load_raster(self, raster_path, name, schema_name="public", table_name="raster"):
        with open(raster_path, 'rb') as f:
            raster_data = f.read()
            self.execute(f"CREATE TABLE IF NOT EXISTS {schema_name}.{table_name}( name varchar, geom raster)")
            self.cur.execute(f"INSERT INTO {schema_name}.{table_name} (name, geom) VALUES ('{name}'," + "ST_FromGDALRaster(%(byte)s))", {'byte': raster_data})
            self.conn.commit()
        
    def load_vector(self, vector_path, schema_name="public", table_name="vector"):
        ds = ogr.Open(vector_path, 0)
        layer = ds.GetLayer()
        for i in range(layer.GetFeatureCount()):  
            feature = layer.GetFeature(i)  
            wkt = feature.GetGeometryRef().ExportToWkt()  
            self.execute(f"CREATE TABLE IF NOT EXISTS {schema_name}.{table_name}( name varchar, geom geometry)")
            self.execute(f"INSERT INTO {schema_name}.{table_name} (name, geom) VALUES ('{table_name}', ST_GeometryFromText('{wkt}', " +"4326))")
    
    def load_shapefile_fromzip(self, zip_path, schema_name="public", table_name="vector"):
        zip = zipfile.ZipFile(zip_path)
        tempdir = tempfile.mkdtemp()
        for name in zip.namelist():
            data = zip.read(name)
            outfile = os.path.join(tempdir, name)
            f = open(outfile, 'wb')
            f.write(data)
            f.close()
        self.load_vector(outfile, table_name, schema_name)
    
    def vector_rasterize(self, schema_name="public", table_name="vector"):
        self.execute(f"DROP TABLE IF EXISTS mytable")
        self.execute(f"SELECT ST_AsRaster(geom,100,100,ARRAY['8BUI'],ARRAY[118]) AS rast INTO TEMP mytable FROM {schema_name}.{table_name}")
        self.execute(f"SELECT ST_AsGDALRaster(rast, 'GTiff') FROM mytable")
        vsipath = '/vsimem/from_postgis'
        gdal.FileFromMemBuffer(vsipath, bytes(self.cur.fetchone()[0]))
        ds = gdal.Open(vsipath)
        tif_file = f'/vsimem/{table_name}.tif'
        gdal.Translate(tif_file, ds, format='GTiff')
        return tif_file