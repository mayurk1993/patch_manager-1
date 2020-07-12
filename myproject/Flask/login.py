from flask import Flask, render_template, request, session
from forms import SignUpForm, EnvironmentForm, RightScriptForm
from controller import wfm
from beans.User import User1
import json
import sys
import logging

logging.basicConfig(filename='app.log',level=logging.DEBUG)

sys.path.append(".")

app = Flask(__name__)
app.secret_key = 'My Keys'

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = SignUpForm()
    form1 = EnvironmentForm()
    form2 = RightScriptForm()

    if form.is_submitted() and form.submit.data:
        rs_token = request.form['password']
        obj = User1(rs_token)
        logging.info("Authenticating User RS token")
        response = obj.authenticate_user(rs_token)
        if response.status_code == 200:
            session['bearer_token'] = obj.bearer_token
            return render_template('second.html', form=form1)
        else:
            return render_template('invalid.html')

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
        return render_template('fourth.html', form=form2, dep_list=dep_list1)

    if form2.is_submitted() and form2.confirm.data:
        print("inside form2 submitted")
        User1.bearer_token = session['bearer_token']
        print(request.form.getlist('selected'))
        my_list = wfm.execute_right_script(request.form.getlist('selected'), request.form['rs_name'],
                                           session['bearer_token'])
        for response in my_list:
            print(response.content)
        return render_template('fourth.html', form=form2, dep_list=session['dep_list1'])

    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
