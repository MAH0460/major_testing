#Backend is responsible for routing to the correct destination, computational tasks, security & data access
#We cannot directly use raw links name in practical cases as it has to represent an actual endpoint destination
#url_for(route_function) is widely use to represent links dynamically & make the management much more easier
#Redirect means hop from one route to another
#messages to be flashed are stored in a queue known as flashstore/message store.

#Developed by : Animesh  Mishra
from flask import Flask,request,session,render_template,url_for,flash,redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = "super_secret"

@app.route("/")
def services():
    return render_template('services.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/signup")
def register():
    #print(session['register'])
    return render_template('signup.html')

@app.route("/authenticate",methods=["POST"])
def authenticate():
    if request.method == "POST":
        session['register'] = request.form['fname']
        return render_template('services.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/feedback")
def feedback():
    return render_template('feedback.html')

@app.route("/toolbox/<string:toolName>",methods=['GET'])
def toolbox(toolName):
    return render_template('toolInterface.html',toolname=toolName)

@app.route("/forgot_pswd")
def forgot_pswd():
    return render_template('forgotPassword.html')

@app.route("/otp")
def otp_auth():
    get_otp = gen_otp()
    flash(f"OTP generated : {get_otp}","information")
    return render_template('otp.html')

def gen_otp():
    from string import digits
    from random import choice
    random_otp = "".join(choice(digits) for _ in range(4))
    session['otp'] = random_otp
    return random_otp

@app.route("/otp_check",methods=['GET','POST'])
def otp_check():
    if request.method == "POST":
        if session['otp'] == request.form.get("input_otp"):
            flash("OTP VALIDATED SUCCESSFULLY!", "information")
            return redirect(url_for('login'))
        else:
            flash("OTP INVALID!","error")
            return redirect(url_for('otp_auth'))

#@nimesh : Generalised endpoint to connect frontend with core modules respectively
@app.route("/toolkit/<string:toolName>",methods=['GET','POST'])
def toolkit(toolName):
    inputData = request.form.get('inputData')
    if toolName == "TagExtraction":
        from textInsightToolkit.keyword_extract_tfidf import tagIntegrator
        return "\t#".join(tagIntegrator(inputData))
    elif toolName == "TextSummarization":
        from textInsightToolkit.textSummarization import summaryIntegrator
        requiredSize = request.form.get('rangeValue')
        return "\n\n".join(summaryIntegrator(inputData,requiredSize))
    elif toolName == "QuestionGeneration":
        from textInsightToolkit.SubjectiveQGen import subQGenIntegrator
        from textInsightToolkit.textSummarization import summaryIntegrator
        requiredSize = request.form.get('rangeValue')
        extractedData = "\n\n".join(summaryIntegrator(inputData, requiredSize))
        return "\n\n".join(subQGenIntegrator(extractedData))
    else:
        return "Invalid Tool Selected"



#@app.route("/upload_pdf", methods=['GET', 'POST'])
#def upload_pdf():
#    if request.method == 'POST':
#        if 'file' not in request.files:
#           flash("No file chosen", 'danger')
#            return redirect(request.url)
#        file = request.files['file']
#        if file.filename == '':
#            return redirect(request.url)
#        elif not allowed_file(file.filename):
#            flash('Incorrect file extenstion. Must be .TXT!', 'danger')
#            return redirect(request.url)
#        elif file:
#            filename = secure_filename(file.filename)
#            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #
            # Process the file (omitted here)
            #
#
#            proc = subprocess.Popen('python author_script.py {} -p {} -s {} -m {}'.format(file.filename, period, space, affiliation), shell=True, stdout=subprocess.PIPE)
#            time.sleep(0.5)
#           return redirect(url_for('results'))
#        else:
            # THIS PART IS NOT WORKING!
#           return redirect(request.path)
#          flash('There is an affiliation missing from your Place list.', 'danger')
#    return render_template('index.html', template_file=app.config['TEMPLATE_FILE'])

if __name__ == '__main__':
    app.run(debug=True)
