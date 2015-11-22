# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """

    if auth.user:
        redirect(URL("user","home"));

    response.flash = T("Time to get connected")
    message=T('Get connected with your friends')
    dev_mode = False;
    return locals();

def message():
    name_list=[]
    email_list=[]
    recent_message=[]
    time=[]
    user_id=[]
    profile_pic = []
    current_user=db.auth_user(auth.user.id).email
    user=db(db.auth_user).select()
    for each_user in user:
        if each_user.id!=auth.user.id:
            
            entry=db(((db.tbl_message.from_email==current_user)&(db.tbl_message.to_email==each_user.email))|((db.tbl_message.to_email==current_user)&(db.tbl_message.from_email==each_user.email))).select(orderby=~db.tbl_message.created_on)
            if entry:
                profile_pic.append( each_user.profile_picture );
                user_id.append(each_user.id)
                name_list.append(each_user.first_name+" "+each_user.last_name)
                email_list.append(each_user.email)
                recent_message.append(entry[0].msg_content)
                time.append(entry[0].created_on)
    return locals()

def connection():
    friends_rows=[]
    login_friends_ids= db((db.friends_table.usr_id==auth.user.id)&(db.friends_table.status=="a")).select(distinct=True)
    for id in login_friends_ids:
        temp=db(db.auth_user.id==id.friend_id).select()
        for temp2 in temp:
            friends_rows.append(temp2)
    pending_friends_rows=[]
    pending_friends_ids= db((db.friends_table.friend_id==auth.user.id)&(db.friends_table.status=="p")|(db.friends_table.status=="v")).select(distinct=True)
    for each_id in pending_friends_ids:
        temp=db(db.auth_user.id==each_id.usr_id).select()
        for temp2 in temp:
            pending_friends_rows.append(temp2)
    
    
    return locals()

def chat_window():
#     str=''.join(request.args)
    str = request.args(0)

    print "chat_window"
    print str;

    to_email = str;

    q=db.auth_user(auth.user.id)
    from_name= q.first_name +" "+ q.last_name

    print str;

    prevchat=db(((db.tbl_message.to_email==str)&(db.tbl_message.from_email==q.email))|
                (((db.tbl_message.to_email==q.email))&((db.tbl_message.from_email==str)))).select(orderby=db.tbl_message.created_on)
    print "----"
    print prevchat
    return locals()

def add_message():

    print "---------------"
    print "add_message"
    print request.vars.to_email
    print request.vars.user_message
    db.tbl_message.insert(\
        to_email=request.vars.to_email,\
        from_email=db.auth_user(auth.user.id).email,\
        msg_content=request.vars.user_message\
        )




def search():
    search_entry_form=FORM(
    INPUT(_name="first_name",_type="text",_placeholder="first name"),
    INPUT(_name="last_name",_type="text",_placeholder="last name"),
    INPUT(_type="submit",_value="Search"))
    if search_entry_form.accepts(request.vars,formname='search_entry_form'):
        session.flash="Search result"
        redirect(URL('search_friends',vars={'a':request.vars.first_name,'b':request.vars.last_name}))
    return locals()

def search_friends():
    friend_list=[]
    logged_usr_id=auth.user.id
    x=request.vars
    a=x.a
    b=x.b
    if b and a:
        rows=db((db.auth_user.first_name.contains(a))&(db.auth_user.last_name.contains(b))&(db.auth_user.id!=auth.user.id)).select(orderby=db.auth_user.first_name)
    elif a:
        rows=db((db.auth_user.first_name.contains(a))&(db.auth_user.id!=auth.user.id)).select()
    elif b:
        rows=db((db.auth_user.last_name.contains(b))&(db.auth_user.id!=auth.user.id)).select()
    else:
        pass
    friend_id_all=db(db.friends_table).select(db.friends_table.friend_id,distinct=True)
    for row in rows:
            val=db((db.friends_table.friend_id==row.id)&(db.friends_table.usr_id==auth.user.id) ).select()
            if val:
                for c in val:
                    friend_list.append(c.status)
            else:
                friend_list.append('n')
    return locals()

#def search_friends():
    
#    x=request.vars
#    a=x.a
#    b=x.b
#    if b and a:
#        rows=db((db.auth_user.first_name.contains(a))&(db.auth_user.last_name.contains(b))&#(db.auth_user.id!=auth.user.id)).select(orderby=db.auth_user.first_name)
#    elif a:
#        rows=db((db.auth_user.first_name.contains(a))&(db.auth_user.id!=auth.user.id)).select()
#    elif b:
#        rows=db((db.auth_user.last_name.contains(b))&(db.auth_user.id!=auth.user.id)).select()
#    else:
#        pass    
#    return locals()
def show_profile():
    profile_info = db(db.auth_user.id==request.vars.id).select()
    return locals()

def friend_request():
    db.friends_table.insert(usr_id=request.vars.login_usr_id,friend_id=request.vars.frnd_id,status=request.vars.stats)
    
    redirect(URL('search_friends',vars={'a':request.vars.first,'b':request.vars.last}))
    #redirect(URL('search_friends',vars={'a':request.vars.first_name,'b':request.vars.last_name}))
    return locals()

def pending_friend_request():
    
    row_update=db((db.friends_table.usr_id==request.vars.usr_id)&(db.friends_table.friend_id==request.vars.frnd_id)).select()
    if row_update:
        for row_first in row_update:
            row_first.update_record(status=request.vars.stats)
            
    if request.vars.stats=='a':
        revers_row_update=db((db.friends_table.usr_id==request.vars.frnd_id)&(db.friends_table.friend_id==request.vars.usr_id)).select()
        if revers_row_update:
            for rev_row_first in revers_row_update:
                rev_row_first.update_record(status=request.vars.stats)
               
        else:
            db.friends_table.insert(usr_id=request.vars.frnd_id,friend_id=request.vars.usr_id,status=request.vars.stats)
            
    redirect(URL('connection'))
    return locals()

def unfriend():
    db((db.friends_table.usr_id==request.vars.usr_id)&(db.friends_table.friend_id==request.vars.frnd_id)).delete()
    db((db.friends_table.usr_id==request.vars.frnd_id)&(db.friends_table.friend_id==request.vars.usr_id)).delete()
    redirect(URL('connection'))
    return locals



def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
