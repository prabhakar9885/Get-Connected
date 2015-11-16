# -*- coding: utf-8 -*-

db.define_table( "tbl_gallery", Field("gallery_name", "string" ),
								Field("description", "text"),
								auth.signature,
								format = '%(gallery_name)s'
				)
db.tbl_gallery.gallery_name.requires = [ IS_NOT_EMPTY(), IS_NOT_IN_DB(db, db.tbl_gallery.gallery_name) ]



tbl_pic = db.define_table( "tbl_pictures",	Field("gallery_name", 'reference tbl_gallery' ),
    							#Field('pic_blob', 'blob'),
								Field('pic_upload', 'upload'),#, uploadfield='pic_blob'),
								Field("thumbnail", "upload"),
								Field('description', 'text'),
								auth.signature
				);


from smarthumb import SMARTHUMB 
box = (200, 200)
tbl_pic.thumbnail.compute = lambda row: SMARTHUMB(row.pic_upload, box)
