from app import create_app,db
#from app.models.models import Users,Budget,Expanse,Category
app=create_app()

with app.app_context():
    db.create_all()

if __name__=="__main__":
    app.run(debug=True)