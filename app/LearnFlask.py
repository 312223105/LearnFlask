# encoding=utf-8

import os
from flask import Flask, render_template, redirect, url_for, flash

from app.models import *
from Form import *

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SECRET_KEY'] = 'YingZi'
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)





@app.route('/', methods=['GET', 'POST'])
def employee_manage():
    name = None
    phone = None
    status = 1
    others = None
    form = EmployeeForm()
    if form.validate_on_submit():
        name = form.name.data
        phone = form.phone.data
        status = form.status.data
        others = form.others.data
        code = form.code.data
        data = Employee.query.filter_by(name=name).all()
        if len(data) == 0:
            obj = Employee(name=name, phone=phone, status=status, others=others, code=code)
            db.session.add(obj)
            db.session.commit()
            flash("<p>添加新员工成功：</p><p> 姓名： %r </p><p> 编号：%r </p><p> 电话：%r </p><p> 状态： %r </p><p> 其他：%r</p>" % (name, code, phone, status, others))
        else:
            obj = data[0]
            name = obj.name
            phone = obj.phone
            status = obj.status
            others = obj.others
            code = obj.code
            flash("<p>已存在与“%r”姓名相同的员工：</p><p> 姓名： %r </p><p> 编号：%r </p><p> 电话：%r </p><p> 状态： %r </p><p> 其他：%r</p>"\
                  % (name, name, code, phone, status, others))
        return redirect(url_for("employee_manage"))

    return render_template('employee_manage.html', form=form)


if __name__ == '__main__':
    app.run()
