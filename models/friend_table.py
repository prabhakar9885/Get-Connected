# -*- coding: utf-8 -*-

db.define_table('friends_table',Field('usr_id','text',),
               Field('friend_id','text'),
               Field('status','text'),
               auth.signature
               )
