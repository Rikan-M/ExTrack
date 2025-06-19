from app import create_app,db
import os
#from app.models.models import Users,Budget,Expanse,Category
app=create_app()

with app.app_context():
    db.create_all()

if __name__=="__main__":
    port=int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port)