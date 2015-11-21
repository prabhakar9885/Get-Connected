# -*- coding: utf-8 -*-
# * View Gallaries
# * Create Gallery
# * View contents of a gallary
# * Like Gallery
# * Like Photo(s)

@auth.requires_login()
def index():
	"""	Returns the list of all the Galleries for the logged-in user.
	"""
	loggedin_user = db( db.auth_user.id== auth.user.id ).select() [0];
	rows = db( db.tbl_gallery.created_by==loggedin_user ).select( orderby=db.tbl_gallery.gallery_name )
	gallery_size={};
	for row in rows:
		gallery_size[row.id] = len(db(db.tbl_pictures.gallery_name==row.id).select())

	return locals();


@auth.requires_login()
def new_gallery():
	gallery_form = FORM(
		INPUT(_name='gallery_name',_type='string', _placeholder="Gallery Name"),
		INPUT(_name='description',_type='text', _placeholder="Gallery is about..."),
		# INPUT(_name='image_title',_type='text', _placeholder="Image Title"),
		# INPUT(_name='image_file',_type='file', _placeholder="Image File"),
		INPUT(_type="submit", _value="Done")
	)
	
	if gallery_form.accepts(request.vars):
		
		id = db.tbl_gallery.insert( gallery_name=gallery_form.vars.gallery_name,
									description=gallery_form.vars.description );
		session.flash="done "+str(id);
		# redirect( URL("gallery", "index") );

	return locals();


@auth.requires_login()
def edit_gallery():

	loggedin_user = db( db.auth_user.id== auth.user.id ).select() [0];
	gallery_id = request.args(0);
	gallery_name = db.tbl_gallery[gallery_id].gallery_name;

	db.tbl_pictures.gallery_name.default = gallery_id;
	db.tbl_pictures.gallery_name.writable = False;

	img_form = SQLFORM(db.tbl_pictures);

	if img_form.process(message_onsuccess="Added to "+gallery_name+" successfully.").accepted:
		session.flash = "Added to "+gallery_name+" successfully."
		
	return locals();


@auth.requires_login()
def view_gallery():
	gallery_id = request.args(0);
	gallery_name = db.tbl_gallery[gallery_id].gallery_name;
	loggedin_user = db( db.auth_user.id== auth.user.id ).select() [0];

	pics = db(db.tbl_pictures.created_by==loggedin_user and 
				db.tbl_pictures.gallery_name==gallery_id ).select();
	return locals();


@auth.requires_login()
def download():
    return response.download(request, db);