from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from datetime import datetime

import sqlite3
import os
import pytz

# Folder path
UPLOAD_FOLDER = 'static'
# Allowed files
ALLOWED_EXTENSIONS = {'png', 'PNG', 'jpg', 'JPG', 'jpeg', 'JPEG'}

app = Flask( 
	__name__,
	template_folder='templates',
	static_folder='static'
)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    split = filename.split('.')
    if split[-1] in ALLOWED_EXTENSIONS:
        return True
    return False

@app.route('/', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		# If a file was picked and was one of the allowed extensions
		file = request.files['file']
		userName = request.form.get('uname')
		userCaption = request.form.get('ucap')
		
		if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		
		# Writing to the database
		with sqlite3.connect('socialMedia.db') as conn:
			c = conn.cursor()
				
			time_date = datetime.now(pytz.timezone('US/Pacific')).strftime('%m-%d-%Y %H:%M:%S')
			time_date = str(time_date)

			date_time = datetime.strptime(time_date,'%m-%d-%Y %H:%M:%S')

			thehour = date_time.strftime("%H")
			am_pm = date_time 
			am_pm = int(thehour)
			if am_pm > 11:
					am_pm = 'PM'
			else:
					am_pm = 'AM'

			date_time = str(date_time.strftime("%m-%d-%Y %I:%M ")) + am_pm
			
			c.execute("INSERT INTO socialposts VALUES (?,?,?,?)",(userName,filename,userCaption, date_time))
			conn.commit()

		return 'Donezo!!'
																	
	return render_template("main.html")

@app.route("/posts")
def social_posts():
  # Grabbing all entries from posts table
	with sqlite3.connect('socialMedia.db') as conn:
		c = conn.cursor()
		c.execute("SELECT * FROM socialposts")
		social_entries = c.fetchall()
	conn.close() 
		
	my_index = len(social_entries)

	# Putting data in a corresponding list
	usernames = []
	images = []
	captions = []
	dateAndTime = []
	for i in range(len(social_entries)):
			usernames.append(social_entries[i][0])
			images.append('static/'+social_entries[i][1])
			captions.append(social_entries[i][2])
			dateAndTime.append(social_entries[i][3])

	return render_template("posts.html",usernames=usernames,images=images,captions=captions,my_index=my_index, date_times = dateAndTime)

if __name__ == "__main__":
  app.run(host='0.0.0.0')