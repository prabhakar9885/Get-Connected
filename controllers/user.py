# -*- coding: utf-8 -*-
# 	Contains the code for displaying the user-wall


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
	id_of_posts_liked_by_me = []

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

		comments_data = db( db.tbl_comments.post_id==post.id ).select(orderby=db.tbl_comments.created_on);
		comments_for_post_dict[ post.id ] = comments_data;

		for comment in comments_data:
			if comment.created_by not in commenter_profile_pic:
				commenter_profile_pic[ comment.created_by ] \
				   = db( db.auth_user.id == comment.created_by ).select()[0].profile_picture

		i = i+1;

	return locals();

def post_status():
	loggedin_User_id = auth.user.id;
	new_status_from_server = request.vars.new_status
	db.tbl_posts.insert(shared_with=request.vars.shared_with, data_content=request.vars.new_status)
	db.commit();
	session.flash = "Posted Successfully."
	redirect("home")
	# return response.render('user/home.html', locals() );


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
    return response.download(request, db);