from flask import Flask, render_template, request, session, url_for
from werkzeug.utils import redirect
from forms import SignUpForm, EnvironmentForm, RightScriptForm
from controller import wfm
from beans.User import User1
import json
import sys
import logging

logging.basicConfig(filename='app.log', level=logging.DEBUG)

sys.path.append(".")

app = Flask(__name__)
app.secret_key = 'My Keys'


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = SignUpForm()
    return render_template('login.html', form=form)


@app.route('/deployment_info', methods=['GET', 'POST'])
def deployment_info():
    form = SignUpForm()
    form1 = EnvironmentForm()
    if form.is_submitted() and form.submit.data:
        rs_token = request.form['password']
        obj = User1(rs_token)
        logging.info("Authenticating User RS token")
        response = obj.authenticate_user(rs_token)
        if response.status_code == 200:
            session['bearer_token'] = obj.bearer_token
            return render_template('second.html', form=form1)
        else:
            logging.error("Invalid RS Token")
            message = "Invalid RS Token, Please Re-try."
            return redirect(url_for('error', message=message))


@app.route('/apply_patch', methods=['GET', 'POST'])
def apply_patch():
    form1 = EnvironmentForm()
    form2 = RightScriptForm()
    if form1.is_submitted() and form1.proceed.data:
        print("inside form1 submitted")
        result = request.form
        stack = result['stack']
        environment = result['environment']
        rel_v = result['release_version']
        service = result['service']
        bearer_token = session['bearer_token']
        dep_list = wfm.get_deployment_details(environment, rel_v, service, stack, bearer_token)
        session['dep_list'] = dep_list
        dep_list1 = []
        for i in dep_list:
            a = json.loads(i)
            dep_list1.append(a)

        session['dep_list1'] = dep_list1

        #        for i in dep_list:
        #            print(i.self_service_url)

        if len(dep_list1) == 0:
            logging.error("Deployment received is empty")
            message = "No Deployments found for selected parameters."
            return redirect(url_for('error', message=message, dep_list1=dep_list1))
        return render_template('fourth.html', form=form2, dep_list=dep_list1)
    return render_template('second.html', form=form1)


@app.route('/execute_right_script', methods=['GET', 'POST'])
def execute_right_script():
    form2 = RightScriptForm()

    if form2.is_submitted() and form2.confirm.data:
        print("inside form2 submitted")
        User1.bearer_token = session['bearer_token']
        print(request.form.getlist('selected'))
        print(request.form['rs_name'])
        my_list = wfm.execute_right_script(request.form.getlist('selected'), request.form['rs_name'],
                                           session['bearer_token'])
        if len(my_list) == 0:
            logging.error("Entered Rightscript doesn't exist")
            message = "Entered Rightscript doesn't exist"
            return redirect(url_for('error', message=message, dep_list1=session['dep_list1']))

        #        for response in my_list:
        #            print(response.content)
        return render_template('fourth.html', form=form2, dep_list=session['dep_list1'])


@app.route('/error', methods=['GET', 'POST'])
def error():
    message = request.args['message']
    form = SignUpForm()
    form2 = RightScriptForm()

    if message == "No Deployments found for selected parameters.":
        dep_list1 = session['dep_list1']
        return render_template('fourth.html', form=form2, dep_list=dep_list1, message=message)
    elif message == "Invalid RS Token, Please Re-try.":
        return render_template('login.html', form=form, message=message)
    elif message == "Entered Rightscript doesn't exist":
        dep_list1 = session['dep_list1']
        return render_template('fourth.html', form=form2, dep_list=dep_list1, message=message)


if __name__ == '__main__':
    app.run(debug=True)
