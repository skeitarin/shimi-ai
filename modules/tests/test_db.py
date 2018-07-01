import os, sys
path = os.path.join(os.path.dirname(__file__), '../')
sys.path.append(path)
import models.db as db

def disp_data(list):
    print(">>>>>>>>>>>")
    for x in list:
        print(x)
    print("<<<<<<<<<<<")

def disp_user_data(session):
    users = session.query(db.User).all()
    disp_data(users)


session_factory = db.SessionContextFactory()
with session_factory.create() as session:
    # --INSERT--
    ed_user = db.User(name='ed', fullname='Ed Jones', password='edspassword')
    session.add(ed_user)
    
    # select all columns
    users = session.query(db.User).all()
    disp_data(users)
    
    # select part of columns
    users = session.query(db.User.fullname, db.User.password).all()
    disp_data(users)

with session_factory.create() as session:  
    # --UPDATE--
    update_target = session.query(db.User).filter_by(name = 'ed').one()
    update_target.password = 'edit pass!!'
    
    disp_user_data(session)

with session_factory.create() as session:
    # --DELETE--
    delete_target = session.query(db.User).all()
    for del_user in delete_target:
        session.delete(del_user)
    session.commit()
    
    disp_user_data(session)