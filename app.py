import os
from flask import Flask,render_template,request
from pymongo import MongoClient
from dotenv import load_dotenv


load_dotenv()

def create_app():
    app=Flask(__name__)
    client=MongoClient(os.getenv("MONGODB_URI"))
    app.db=client.hotel

    @app.route("/",methods=["GET","POST"])
    def home():
        return render_template("home.html")

    @app.route("/add" ,methods =["GET","POST"] )
    def add_new():
        if request.method == "POST":
            username=request.form.get("username")
            hotel=request.form.get("hotel")
            Address=request.form.get("address")
            price=request.form.get("cost")
            app.db.hotel_details.insert_one({"username":username,
                                            "hotel":hotel,
                                            "address":Address,
                                            "cost":price})
        return render_template("add_new.html",title="AddNew")

    @app.route("/view")
    def view():
        hotelinfo=[
                        (entry["hotel"], 
                        entry["address"],
                        entry["cost"]  
                        )
                    for entry in app.db.hotel_details.find({})
                    ]
            
        return render_template("display.html",entries=hotelinfo)

    @app.route("/update",methods=["GET","POST"])
    def update():
        if request.method == "POST":
            username=request.form.get("username")
            hotel=request.form.get("hotel")
            Address=request.form.get("address")
            price=request.form.get("cost")
            user=app.db.hotel_details.find_one({"username":username})
            
            if user:
                updated_value= {
                        "$set": {
                            "hotel": hotel,
                            "address": Address,
                            "cost": price
                        }}

                updated = app.db.hotel_details.update_one({"username": username}, updated_value)
                
                return render_template("update.html", user=user)
            else:
                return render_template("home.html")
            

        return render_template("update.html")
            
        
    @app.route("/delete",methods=["GET","POST"])
    def delete():
        
        if request.method == "POST":
            username=request.form.get("username")
            hotel=request.form.get("hotel")
            Address=request.form.get("address")
            price=request.form.get("cost")
            user=app.db.hotel_details.find_one({"username":username})
            
            if user:
                deleted = app.db.hotel_details.delete_one({"username": username})
                
                return render_template("delete.html")
            else:
                return render_template("home.html")
            
        return render_template("delete.html")
    return app