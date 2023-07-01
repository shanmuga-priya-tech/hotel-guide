import secrets
import os
from flask import Flask,render_template,request,redirect,flash,url_for
from pymongo import MongoClient,DESCENDING
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()
secret_key = secrets.token_hex(32)


def create_app():
    app=Flask(__name__)
    app.secret_key = secret_key
    client=MongoClient(os.getenv("MONGODB_URI"))
    app.db=client.hotel

    @app.route("/",methods=["GET","POST"])
    def home():
        return render_template("home.html")

    @app.route("/add" ,methods =["GET","POST"] )
    def add_new():
        if request.method == "POST":
            hotel=request.form.get("hotel")
            address=request.form.get("address")
            price=request.form.get("cost")
            time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            app.db.hotel_details.insert_one ({
                                            "hotel":hotel,
                                            "address":address,
                                            "cost":price,
                                            "time":time}) 
            flash("Added successfully!") 
            return redirect(url_for("view"))

                                        
        return render_template("add_new.html")

    @app.route("/view",methods=["GET","POST"])
    def view():
        hotelinfo=[
                        (entry["hotel"], 
                        entry["address"],
                        entry ["cost"],
                        entry["time"]
                        )   
                    for entry in app.db.hotel_details.find({}).sort("time",DESCENDING)
                    ]       
        return render_template("display.html",entries=hotelinfo)

    @app.route("/update",methods=["GET","POST"])
    def update():
        if request.method == "POST":
            hotel=request.form.get("hotel")
            Address=request.form.get("address")
            price=request.form.get("cost")
            user=app.db.hotel_details.find_one({"hotel":hotel})
            
            if user:
                updated_value= {
                        "$set": {
                            "hotel": hotel,
                            "address": Address,
                            "cost": price
                        }}

                updated = app.db.hotel_details.update_one({"hotel":hotel}, updated_value)
                flash("Updated successfully!") 
                return redirect(url_for("view"))
                
            else:
                return render_template("home.html")
        return render_template("update.html")
            
        
    @app.route("/delete",methods=["GET","POST"])
    def delete():
        
        if request.method == "POST":
            hotel=request.form.get("hotel")
            Address=request.form.get("address")
            price=request.form.get("cost")
            user=app.db.hotel_details.find_one({"hotel":hotel})
            
            if user:
                app.db.hotel_details.delete_one({"hotel":hotel})

                flash("Deleted successfully!") 
                return redirect(url_for("view"))
                
            else:
                return render_template("home.html")
            
        return render_template("delete.html")
    return app
