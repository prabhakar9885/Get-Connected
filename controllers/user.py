# -*- coding: utf-8 -*-
# 	Contains the code for displaying the user-wall

@auth.requires_login()
def get_gallary_rows():
	loggedin_User_id = auth.user.id;
	rows = db( db.tbl_gallery.created_by==loggedin_User_id ).select( orderby=db.tbl_gallery.gallery_name )
	gallery_size={};
	for row in rows:
		gallery_size[row.id] = len(db(db.tbl_pictures.gallery_name==row.id).select())
	return (rows, gallery_size);

@auth.requires_login()
def list_galleries():
	print "list_galleries"
	gallery_rows, gallery_size = get_gallary_rows();

	return locals();


@auth.requires_login()
def home():
	loggedin_User_id = auth.user.id;
	new_status_from_server = request.vars.new_status

	db.tbl_posts.data_content.readable = False
	db.tbl_posts.data_content.writable = False
	form = SQLFORM(db.tbl_posts);
	posts = db( (db.tbl_posts.created_by==loggedin_User_id) | 
						(db.tbl_posts.shared_with==loggedin_User_id) ).select( orderby=~db.tbl_posts.created_on );
	
	i=0;
	post_cleaned=[]
	commenter_profile_pic = {}
	comments_for_post_dict = {}
	count_of_likes_for_post = {}
	id_of_posts_liked_by_me = []
	profile_picture_of_post_owner = {}
	first_two_likes_by = {}

	query_the_liked_posts = (db.tbl_likes.post_id != None) & \
								 (db.tbl_likes.created_by == auth.user.id);

	_id_of_posts_liked_by_me = db( query_the_liked_posts ).select( db.tbl_likes.post_id );
	for liked_post in _id_of_posts_liked_by_me:
		id_of_posts_liked_by_me.append( liked_post.post_id )

	for post in posts:
		post_cleaned.append(post);
		creater = db(post_cleaned[i].created_by ==db.auth_user.id).select()[0];
		post_cleaned[i].created_by = "%s %s" %(creater.first_name, creater.last_name);
		try:
			shared_with = db(post_cleaned[i].shared_with ==db.auth_user.id).select()[0];
			post_cleaned[i].shared_with = "%s %s" %(shared_with.first_name, shared_with.last_name);
		except IndexError: # The post is shared with none.
			post_cleaned[i].shared_with = "";

		# Get all the comments for the "post"
		comments_data = db( db.tbl_comments.post_id==post.id ).select(orderby=db.tbl_comments.created_on);
		comments_for_post_dict[ post.id ] = comments_data;

		# Get the profile pic of all the commenters for the "post"
		for comment in comments_data:
			if comment.created_by not in commenter_profile_pic:
				commenter_profile_pic[ comment.created_by ] \
				   = db( db.auth_user.id == comment.created_by ).select()[0].profile_picture

		# Get count of the likes for "post"
		count_of_likes_for_post[post.id] = db( db.tbl_likes.post_id == post.id ).count()

		print count_of_likes_for_post
		if count_of_likes_for_post[post.id] > 0:
			first_two_likes_by[post.id] = [];
			temp = db( db.tbl_likes.post_id == post.id ).select(orderby=db.tbl_likes.created_on)
			if len(temp)>0 :
				x = db( db.auth_user.id == temp[0].created_by ).select()[0]
				x = x.first_name +" " + x.last_name;
				print x
				first_two_likes_by[post.id].append( x );
			if len(temp)>1 :
				x = db( db.auth_user.id == temp[1].created_by ).select()[0]
				x = x.first_name +" " + x.last_name;
				print x
				first_two_likes_by[post.id].append( x );

		# Get profile pic of the "post" creater.
		if post.modified_by not in profile_picture_of_post_owner:
			profile_picture_of_post_owner[ post.modified_by ] = \
						db(db.auth_user.id==post.modified_by).\
							select( db.auth_user.profile_picture )[0].profile_picture ;

		i = i+1;

	gallary_rows, gallery_size  = get_gallary_rows();
	return locals();


@auth.requires_login()
def new_gallery():
	return locals();


@auth.requires_login()
def view_gallery( gallery_id ):
	gallery_name = db.tbl_gallery[gallery_id].gallery_name;
	loggedin_user = db( db.auth_user.id== auth.user.id ).select() [0];

	pics = db(db.tbl_pictures.created_by==loggedin_user and 
				db.tbl_pictures.gallery_name==gallery_id ).select();
	return pics;


@auth.requires_login()
def new_gallery_creater():
	session.flash = request.vars;
	gallery_id = db.tbl_gallery.insert( gallery_name=request.vars.gallery_name,
										description=request.vars.description );
	session.flash="done "+str(id);

	pics = view_gallery( gallery_id )
	script_js  = "jQuery('#%s').get(0).reload();" % ("list-galleris")
	script_js += "jQuery('#%s').get(0).reload();" % ("list-galleris")
	response.js =  script_js
	return locals();


@auth.requires_login()
def edit_gallery():
	loggedin_user = db( db.auth_user.id== auth.user.id ).select() [0];
	gallery_id = request.args(0);
	gallery_name = db.tbl_gallery[gallery_id].gallery_name;

	db.tbl_pictures.gallery_name.default = gallery_id;
	db.tbl_pictures.gallery_name.writable = False;

	img_form = SQLFORM(db.tbl_pictures).process();

	if img_form.accepts(request.vars, formname="img_form"):
		session.flash = "Added to "+gallery_name+" successfully."
		
	return locals();




@auth.requires_login()
def list_gallery_contents():
	print "list_gallery_contents"
	gallery_id = request.args(0);
	print gallery_id
	gallery_name = db(db.tbl_gallery.id==gallery_id).select()[0].gallery_name;
	loggedin_user = db( db.auth_user.id== auth.user.id ).select() [0];
	
	print URL('views/user', 'list_gallery_contents.html')

	pics = db(db.tbl_pictures.created_by==loggedin_user and 
				db.tbl_pictures.gallery_name==gallery_id ).select();

	return locals();

@auth.requires_login()
def delete_pic():
	print "Delete Pic"
	gallery_id = int(request.args(0));
	print gallery_id
	pic_id = int(request.args(1));
	print pic_id
	db( (db.tbl_pictures.id==pic_id) & (db.tbl_pictures.gallery_name==gallery_id) ).delete();
	session.flash = "Pic Deleted" 
	response.js = "jQuery('#%s').get(0).reload();" % ("list-galleris")


@auth.requires_login()
def post_status():
	loggedin_User_id = auth.user.id;
	new_status_from_server = request.vars.new_status
	db.tbl_posts.insert(shared_with=request.vars.shared_with, data_content=request.vars.new_status)
	db.commit();
	session.flash = "Posted Successfully."
	redirect("home")
	# return response.render('user/home.html', locals() );


@auth.requires_login()
def post_comment_like():
	session.flash = "as "+str(request.vars);

	if request.vars.like_btn:
		# The user has submitted a like/unlike
		
		query = (db.tbl_likes.post_id == request.vars.post_id) & (db.tbl_likes.created_by == auth.user.id);
		user_has_already_liked_the_post = True if len( db( query ).select() ) > 0 else False;

		if user_has_already_liked_the_post:
			db( query ).delete();
			db.commit();
			session.flash = "Removed like."
		else:
			db.tbl_likes.insert( post_id = request.vars.post_id )
			db.commit();
			session.flash = "Liked: " # + str(request.vars);
	else:
		# The user has submitted a comment
		new_comment = request.vars.new_comment
		db.tbl_comments.insert(post_id=request.vars.post_id, data_content=request.vars.new_comment)
		db.commit();
		session.flash = "Commented Successfully."

	redirect("home")


@auth.requires_login()
def download():
    return response.download(request, db, attachment=False);