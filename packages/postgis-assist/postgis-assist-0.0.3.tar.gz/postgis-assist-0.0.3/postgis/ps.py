from postgis.pg import pg 

class ps(pg):
    def raster_makeempty(self, schema_name="public", table_name="raster"):
        self.execute(f"SELECT ST_AsBinary(ST_MakeEmptyRaster(100, 100, 100, 100, 100, 100, '8BUI')) FROM {schema_name}.{table_name} ")
        return self.return_json(self.fetchall())

    def raster_addband(self, schema_name="public", table_name="raster"):
        self.execute(f"SELECT ST_AddBand(geom, '8BUI') FROM {schema_name}.{table_name}")
        return self.return_json(self.fetchall())

    def raster_binary(self, schema_name="public", table_name="raster"):
        self.execute(f"SELECT ST_AsBinary(geom) FROM {schema_name}.{table_name}")
        return self.return_json(self.fetchall())

    def vector_isValid(self, schema_name="public", table_name="vector"):
        self.execute(f"SELECT ST_IsValid(geom) FROM {schema_name}.{table_name}")
        return self.return_json(self.fetchall())
    
    def vector_from_binary(self, binary, schema_name="public", table_name="vector"):
        self.execute(f"CREATE TABLE IF NOT EXISTS {schema_name}.{table_name}( name varchar, geom geometry)")
        self.execute(f"INSERT INTO {schema_name}.{table_name} (name, geom) VALUES ('{table_name}', ST_GeometryFromBinary('{binary}', " +"4326))")
    
    def vector_from_text(self, text, schema_name="public", table_name="vector"):
        self.execute(f"CREATE TABLE IF NOT EXISTS {schema_name}.{table_name}( name varchar, geom geometry)")
        self.execute(f"INSERT INTO {schema_name}.{table_name} (name, geom) VALUES ('{table_name}', ST_GeometryFromText('{text}', " +"4326))")

    def vector_geojson(self, schema_name="public", table_name="vector"):
        self.execute(f"SELECT ST_AsGeoJSON(geom) FROM {schema_name}.{table_name}")
        return self.return_json(self.fetchall())
    
    def vector_binary(self, schema_name="public", table_name="vector"):
        self.execute(f"SELECT ST_AsBinary(geom) FROM {schema_name}.{table_name}")
        return self.return_json(self.fetchall())
    
    def vector_text(self, schema_name="public", table_name="vector"):
        self.execute(f"SELECT ST_AsText(geom) FROM {schema_name}.{table_name}")
        return self.return_json(self.fetchall())

    def vector_geometrytype(self, schema_name="public", table_name="vector"):
        self.execute(f"SELECT ST_GeometryType(geom) FROM {schema_name}.{table_name}")
        return self.return_json(self.fetchall())

    def vector_buffer(self, distance, schema_name="public", table_name="vector"):
        self.execute(f"SELECT ST_AsGeoJSON(ST_Buffer(geom, {distance})) FROM {schema_name}.{table_name}")
        return self.return_json(self.fetchall())

    def vector_simplify(self, tolerance, schema_name="public", table_name="vector"):
        self.execute(f"SELECT ST_AsGeoJSON(ST_Simplify(geom, {tolerance})) FROM {schema_name}.{table_name}")
        return self.return_json(self.fetchall())

    def vector_centroid(self, schema_name="public", table_name="vector"):
        self.execute(f"SELECT ST_AsGeoJSON(ST_Centroid(geom)) FROM {schema_name}.{table_name}")
        return self.return_json(self.fetchall())
    
    def vector_convexhull(self, schema_name="public", table_name="vector"):
        self.execute(f"SELECT ST_AsGeoJSON(ST_ConvexHull(geom)) FROM {schema_name}.{table_name}")
        return self.return_json(self.fetchall())

    def vector_envelope(self, schema_name="public", table_name="vector"):
        self.execute(f"SELECT ST_AsGeoJSON(ST_Envelope(geom)) FROM {schema_name}.{table_name}")
        return self.return_json(self.fetchall())