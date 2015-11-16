# -*- coding: utf-8 -*-
# 	Contains the code for displaying the user-wall


@auth.requires_login()
def home():
	loggedin_User_id = auth.user.id;
	new_status_from_server = request.vars.new_status

	db.tbl_posts.data_content.readable = False
	db.tbl_posts.data_content.writable = False
	form = SQLFORM(db.tbl_posts);
	posts = db(db.tbl_posts.created_by==loggedin_User_id or 
						db.tbl_posts.shared_with==loggedin_User_id).select();
	i=0;
	post_cleaned=[]
	for post in posts:
		post_cleaned.append(post);
		creater = db(post_cleaned[i].created_by ==db.auth_user.id).select()[0];
		post_cleaned[i].created_by = "%s %s" %(creater.first_name, creater.last_name);
		shared_with = db(post_cleaned[i].shared_with ==db.auth_user.id).select()[0];
		post_cleaned[i].shared_with = "%s %s" %(shared_with.first_name, shared_with.last_name);
		i = i+1;
	# options = form.elements('option');
	# for i in options:
	# 	if i.attributes["_value"]==str(loggedin_User_id):
	# 		options.remove( i );
	# form.element('option',replace=options);
	return locals();

def post_status():
	loggedin_User_id = auth.user.id;
	new_status_from_server = request.vars.new_status
	db.tbl_posts.insert(shared_with=request.vars.shared_with, data_content=request.vars.new_status)
	db.commit();
	session.flash = "Posted Successfully."
	redirect("home")
	# return response.render('user/home.html', locals() );