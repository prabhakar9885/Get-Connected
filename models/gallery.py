# -*- coding: utf-8 -*-

db.define_table( "tbl_gallery", Field("gallery_name", "string", requires=IS_NOT_EMPTY() ),
								Field("description", "text"),
								auth.signature,
								format = '%(gallery_name)s'
				)
db.tbl_gallery.gallery_name.requires = [ IS_NOT_EMPTY(), IS_NOT_IN_DB(db, db.tbl_gallery.gallery_name) ]



tbl_pic = db.define_table( "tbl_pictures",	Field("gallery_name", 'reference tbl_gallery' ),
    							#Field('pic_blob', 'blob'),
								Field('pic_upload', 'upload', requires=IS_NOT_EMPTY()),#, uploadfield='pic_blob'),
								Field("thumbnail", "upload"),
								Field('description', 'string'),
								auth.signature
				);


from smarthumb import SMARTHUMB 
box = (200, 200)
tbl_pic.thumbnail.compute = lambda row: SMARTHUMB(row.pic_upload, box)


db.define_table( "tbl_posts",	Field('shared_with', 'reference auth_user'),
								Field('data_content', 'text', requires=IS_NOT_EMPTY() ),
								auth.signature
				);

db.define_table( "tbl_comments",	Field('post_id', 'reference tbl_posts'),
									# Field('gallery_id', 'reference tbl_gallery'),
									Field("data_content", 'text' ),
									auth.signature
				);


db.define_table( "tbl_likes",	Field('post_id', 'reference tbl_posts'),
								Field('comment_id', 'reference tbl_comments'),
								Field('gallery_id', 'reference tbl_gallery'),
								auth.signature
				);
