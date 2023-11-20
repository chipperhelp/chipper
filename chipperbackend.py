from flask import Flask,render_template,redirect,url_for,make_response,request,flash,session
import pyrebase
from datetime import datetime
from datetime import datetime,timedelta
firebaseConfig = {
  "apiKey": "AIzaSyDQkowU9ElUDooKZKb-b-g6beWBF30glv0",
  "authDomain": "chipper1-2980f.firebaseapp.com",
  "databaseURL": "https://chipper1-2980f-default-rtdb.firebaseio.com",
  "projectId": "chipper1-2980f",
  "storageBucket": "chipper1-2980f.appspot.com",
  "messagingSenderId": "276274547796",
  "appId": "1:276274547796:web:9593e0f6fdd3afba8471c1",
  "measurementId": "G-2NPS52N6ZX"
}
firebase= pyrebase.initialize_app(firebaseConfig)

auth=firebase.auth()

data=firebase.database()
storage=firebase.storage()

app=Flask(__name__)


app.secret_key = "123abc"

@app.route('/')
def landing():
    user_token = request.cookies.get("user_id")
    if user_token:
        return redirect(url_for("index"))
    else:
        return redirect(url_for("login"))
   
    

@app.route("/Login",methods=["POST","GET"])
def login():
    error=None
    if request.method=="POST":
        email=request.form["email"]
        passw=request.form["password"]

        if not email or not passw:
            return "Please enter your email and password"
        else:
            try:
                user=auth.sign_in_with_email_and_password(email,passw)
                user_id=user["localId"]
                session["userid"] = user_id
                max_age_in_years = 500
                max_age_in_seconds = max_age_in_years * 365.25 * 24 * 60 * 60 

               
                response = make_response(redirect(url_for('index')))
                
                response.set_cookie('user_id', value=user_id, max_age=int(max_age_in_seconds))
                return response
               
                #return redirect(url_for("index"))
                

            except:
                error="Invalid email or password"
                

                
                
     
            
    
    return render_template("login.html",error=error)
@app.route("/Home-thought's")
def index():
   
    
    
    user_id=session.get("userid", None)
   
    
   
    all_user_posts_response = data.get("Posts")
    all_user_posts = all_user_posts_response.val()

    posts = []

    if all_user_posts is not None:
        for post_id, post_content in all_user_posts.items():
            if isinstance(post_content, dict):
                posts_data = post_content.get("Posts")
                if posts_data is not None:
                    for post_info in reversed(list (posts_data.values())):
                        posts.append(post_info)


    

    paired_data =posts
                        
                        
    #nimg=data.child(user_id).child("Images").get().val()
    #if nimg is not None:
        #v=data.child(user_id).child("Images").get()
        #for img in v.each():
         #   imgc=img.val()
         #   ok=None
          #  imgc=imgc
                                
                          
    #else:
     #   imgc=None
        
      #  ok='https://img.icons8.com/fluency/500/user-male-circle.png'
                              

    return render_template("index.html",paired_data=paired_data)#imgc=imgc,ok=ok
    
@app.route("/Home-pic's")
def pics():
    all_user_posts_response = data.get("posts")
    all_user_posts = all_user_posts_response.val()

    images = []

    if all_user_posts is not None:
        for post_id, post_content in all_user_posts.items():
            if isinstance(post_content, dict):
                posts_data = post_content.get("posts")
                if posts_data is not None:
                    for post_info  in reversed(list (posts_data.values())):
                         images.append({"caption": post_info["caption"], "image_url": post_info["image_url"]})



    return  render_template("indexpics.html",images=images)
@app.route("/Home-videos's")
def video():
    all_user_posts_response = data.get("videosdata")
    all_user_posts = all_user_posts_response.val()

    images = []

    if all_user_posts is not None:
        for post_id, post_content in all_user_posts.items():
            if isinstance(post_content, dict):
                posts_data = post_content.get("videosdata")
                if posts_data is not None:
                    for post_info  in reversed(list (posts_data.values())):
                         images.append({"caption": post_info["caption"], "image_url": post_info["image_url"]})



    return  render_template("indexvideos.html",images=images)

@app.route("/Forgot",methods=["POST","GET"])
def forgot():
    error=None
    success=None
    if request.method=="POST":
        email=request.form["email"]

        try:
             auth.send_password_reset_email(email)
             success=f"Password reset link has been successfully sent to  {email}!"
        except:
            error="Invalid email address"
    return render_template("forgot.html",error=error,success=success)
@app.route("/Register",methods=["POST","GET"])
def register():
    error=None
    if request.method=="POST":
        email=request.form["email"]
        passw=request.form["password"]
        handle=request.form["name"]

        if not email or not passw:
            return "Please enter your email and password"
        else:
            try:
               
                user=auth.create_user_with_email_and_password(email,passw)
                data.child(user["localId"]).child("Handle").set(handle)
                data.child(user["localId"]).child("ID").set(user["localId"])
                dateofjoin = datetime.now().strftime("%d-%m-%y")
                dateofjoinadd="Joined on :"+dateofjoin
                data.child(user["localId"]).child("date").push(dateofjoinadd)

                return redirect(url_for("login"))
                

            except:
                error="Invalid email or user already exists"
    return render_template("register.html",error=error)
@app.route("/Share-a-thought",methods=["POST","GET"])
def sharethoughts():
    user_id=request.cookies.get("user_id")
    success=None
    error=None
    if request.method=="POST":
        
        post=request.form["thought"]
        try:
            now=datetime.now()
            dt=now.strftime("%d / %m / %y")
            dtt=now.strftime("%I:%M %p")
            userdata=data.child(user_id).child("Handle").get().val()
            post=f'''{userdata} \n\n\n {post} \n\n\n  shared on : {dt}  at  {dtt}'''
            results=data.child(user_id).child("Posts").push(post)
            success="Thought shared successfully!"
        except Exception as e :
            error=e
            
                       
    return render_template("sharethought.html",success=success,error=error)
@app.route("/Share-a-pic",methods=["POST","GET"])
def sharepics():
    user_id=request.cookies.get("user_id")
    error=None
    success=None
    if request.method=="POST":
        caption=request.form["caption"]
        image=request.files["filename"]
        try:
             
             image_path = f"images/{image.filename}"
             storage.child(image_path).put(image)

            
             userdata = data.child(user_id).child('Handle').get().val()

            
             now = datetime.now()
             dt = now.strftime("%d / %m / %y")
             dtt = now.strftime("%I:%M %p")
             captiondata = f"{userdata}\n\n{caption}\n\nShared on: {dt} at {dtt}"

            
             post_data = {"caption": captiondata, "image_url": storage.child(image_path).get_url(None)}
             data.child(user_id).child("posts").push(post_data)


             success="Pic shared successfully!"
        except Exception as e :
            error=e
                                                                                                   
    return render_template("sharepic.html",success=success,error=error)
@app.route("/Share-a-video",methods=["POST","GET"])
def sharevideo():
    user_id=request.cookies.get("user_id")
    error=None
    success=None

    if request.method=="POST":
        caption=request.form["caption"]
        image=request.files["filename"]

        
        try:

             image_path = f"videos/{image.filename}"
             storage.child(image_path).put(image)

            
             userdata = data.child(user_id).child('Handle').get().val()

            
             now = datetime.now()
             dt = now.strftime("%d / %m / %y")
             dtt = now.strftime("%I:%M %p")
             captiondata = f"{userdata}\n\n{caption}\n\nShared on: {dt} at {dtt}"

            
             post_data = {"caption": captiondata, "image_url": storage.child(image_path).get_url(None)}
             data.child(user_id).child("videosdata").push(post_data)

        
             success="Video shared successfully!"
        except Exception as e :
            error=e

            

        

    return render_template("sharevideo.html",error=error,success=success)

    
if __name__=="__main__":
    app.run( port=5000, debug=True)
    
