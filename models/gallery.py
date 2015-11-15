# -*- coding: utf-8 -*-

db.define_table( "tbl_gallery", Field("gallery_name", "string" ),
								Field("description", "text"),
								auth.signature,
								format = '%(gallery_name)s'
				)
db.tbl_gallery.gallery_name.requires = [ IS_NOT_EMPTY(), IS_NOT_IN_DB(db, db.tbl_gallery.gallery_name) ]

db.define_table( "tbl_pictures",	Field("galleryId", 'reference tbl_gallery' ),
    							Field('pic_blob', 'blob'),
								Field('pic_upload', 'upload', uploadfield='pic_blob'),
								Field('description', 'text'),
								auth.signature
				);
