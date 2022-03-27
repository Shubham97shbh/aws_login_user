from models import *
from data_class import *
import os



def is_url_image(image_url):
   image_formats = [".png", ".jpeg",".JPG",".jpg"]
   for i in image_formats:
       if i in image_url:
          return True
   return False
# login when the user is verified

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        ip_addr = request.remote_addr
        geo_data = geo.record_by_addr(ip_addr)
        # saving location of the client
        if geo_data:
            new_location = Location(state=geo_data['city'],lat=geo_data['latitude'],long=geo_data['longitude'])
            db.session.add(new_location)
            db.session.commit()
        media_data = User.query.get(current_user.id)
        return render_template('index.html',current_user=current_user,value=media_data)
    return render_template('index.html', current_user=current_user)
@app.route('/register',methods=['GET','POST'])

def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Your account is present')
            return redirect(url_for('login'))
        new_user = User(email=form.email.data,name=form.name.data,password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('index'))
    return render_template('register.html',form=form,current_user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('That email does not exist, please try again')
            return redirect(url_for('login'))
        elif password != user.password:
            flash('Password incorrect,please try again')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html', form=form, current_user=current_user)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/upload',methods=['POST'])
def upload():
    upload_folder = 'uploads'
    if request.method =='POST':
      f = request.files['file']
      bucket_name = 'lambda-s3-dynamo-v1'
      ob_name = f'{f.filename}'
      file_path = os.path.join(upload_folder,secure_filename(f.filename))
      f.save(file_path)
      #saving in s3 bucket
      client.upload_file(f'uploads/{f.filename}',bucket_name,ob_name,)
      #Saving new data
      link = f'http://{bucket_name}.s3.amazonaws.com/{f.filename}'
      new_data = Data(user_id=current_user.id,data_link=link,image=is_url_image(link))
      db.session.add(new_data)
      db.session.commit()
      os.remove(f'uploads/{f.filename}')
      return redirect(url_for('index'))

if __name__ =='__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)