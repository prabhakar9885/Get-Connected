# -*- coding: utf-8 -*-
db.define_table('tbl_message',
               Field('from_email','string',requires=IS_NOT_EMPTY()),
               Field('to_email','string',requires=IS_NOT_EMPTY()),
               Field('msg_content','string'),
               auth.signature
               )
