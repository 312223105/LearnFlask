# encoding=utf-8

from . import main
from flask import render_template, session, redirect, url_for, flash, request, jsonify
from .forms import *
from .. import db, app_log
from ..models import *
from sqlalchemy.exc import IntegrityError, InvalidRequestError


@main.route('/employee_manage', methods=['GET', 'POST'])
def employee_manage():
    form = EmployeeForm()
    if form.validate_on_submit():
        name = form.name.data
        phone = form.phone.data
        status = form.status.data
        others = form.others.data
        code = form.code.data
        obj = Employee(name=name, phone=phone, status=status, others=others, code=code)
        db.session.add(obj)
        try:
            db.session.commit()
            flash("<p>添加新员工成功：</p><p> 姓名： %r </p><p> 编号：%r </p><p> 电话：%r </p><p> 状态： %r </p><p>  "
                  "其他：%r</p>" % (name, code, phone, status, others))
        except IntegrityError or InvalidRequestError as e:
            flash("<h4>添加数据失败:</h4><p>%r</p>" % str(e))
            db.session.rollback()
        return redirect(url_for("main.employee_manage"))

    employees = Employee.query.all()
    if len(employees) == 0:
        employees = None
    return render_template('employee_manage.html', form=form, employees=employees)


@main.route('/employee_manage/edit/<e_id>', methods=['GET', 'POST'])
def employee_edit(e_id):
    employee = Employee.query.filter_by(id=e_id).first()
    if request.method == "POST":
        new_code = request.form.get("code")
        result = Employee.query.filter_by(code=new_code).first()
        if new_code != employee.code and result is not None:
            flash("员工编码（%s）已存在，请重新输入。" % request.form.get("code"))
            return redirect(url_for("main.employee_edit", e_id=e_id))
        employee.phone = request.form.get("phone")
        employee.code = new_code
        employee.status = request.form.get("status")
        employee.others = request.form.get("others")
        db.session.add(employee)
        db.session.commit()
        flash("员工信息已修改成功！")
        return redirect(url_for("main.employee_edit", e_id=e_id))

    return render_template('employee_edit.html', employee=employee)


@main.route("/program_manage", methods=["GET", "POST"])
def program_manage():
    form = ProgramForm()
    if form.validate_on_submit():
        p = Program()
        p.name = form.name.data
        p.price = form.price.data
        p.sort_num = form.sort_num.data
        p.status = form.status.data
        db.session.add(p)
        try:
            db.session.commit()
            flash("<p>添加新消费项目成功：</p><p>项目名称：%r</p><p>项目单价：%r</p><p>排序：%r</p><p>状态：%r</p>" %
                  (p.name, p.price, p.sort_num, p.status))
        except IntegrityError or InvalidRequestError as e:
            flash("<h4>添加数据失败:</h4><p>%r</p>" % e)
            db.session.rollback()
        return redirect(url_for("main.program_manage"))

    programs = Program.query.order_by(Program.sort_num.desc()).all()
    return render_template("program_manage.html", form=form, programs=programs)


@main.route('/program_manage/edit/<p_id>', methods=['GET', 'POST'])
def program_edit(p_id):
    program = Program.query.filter_by(id=p_id).first()
    if request.method == "POST":
        program.price = request.form.get("price")
        program.sort_num = request.form.get("sort_num")
        program.status = request.form.get("status")
        db.session.add(program)
        db.session.commit()
        flash("项目信息已修改成功！")
        return redirect(url_for("main.program_edit", p_id=p_id))

    return render_template('program_edit.html', program=program)


@main.route("/add_vip", methods=["GET", "POST"])
def add_vip():
    add_vip_form = NewVIPForm()
    add_vip_form.proposer.choices = [(int(a.id), a.name + " | " + str(a.code)) for a in Employee.query.filter_by(status=1).all()]
    if add_vip_form.validate_on_submit():
        if VIP.query.filter_by(card_id=add_vip_form.card_id.data).first() is not None:
            flash("卡号已存在，请重新输入！")
            return redirect(url_for("main.add_vip"))
        obj = VIP()
        obj.card_id = add_vip_form.card_id.data
        obj.name = add_vip_form.name.data
        obj.sex = add_vip_form.sex.data
        obj.phone = add_vip_form.phone.data
        if add_vip_form.money.data >= 0:
            obj.money = add_vip_form.money.data
        else:
            obj.money = 0.0
        # obj.money_actully = add_vip_form.money_actully.data
        obj.proposer_id = add_vip_form.proposer.data
        db.session.add(obj)

        try:
            db.session.commit()
        except IntegrityError or InvalidRequestError as e:
            flash("添加会员卡失败：%r" % str(e))
            db.session.rollback()
        # else:
        #     obj_plan = PlanCounting(program_id=add_vip_form.program.data, card_id=obj.id, count=add_vip_form.count.data)
        #     db.session.add(obj_plan)

        else:
            record_add = Record()
            record_add.card_id = obj.id
            record_add.other = "新建会员"
            flash("<p>添加会员成功：</p><p>id=%r</p><p>card_id=%r</p>" % (obj.id, add_vip_form.card_id.data))
            if len(request.form) > 9:
                length = (len(request.form) - 9)
                if length % 3 == 0:
                    p_count = int(length/3)
                    for i in range(1, p_count+1):
                        _name = request.form.get("program"+str(i))
                        _count = request.form.get("count"+str(i))
                        if _count < 0:
                            _count = 0
                        _amount = request.form.get("amount"+str(i))
                        p_c = PlanCounting()
                        p_c.program_id = Program.query.filter_by(name=_name, status=1).first().id
                        p_c.card_id = obj.card_id
                        p_c.count = _count
                        db.session.add(p_c)
                    try:
                        db.session.commit()
                    except IntegrityError or InvalidRequestError as e:
                        flash("<p>添加会员时，设置计次项目失败，请通过<b>充值</b>重新设置：</p><p>%r</p>" % str(e))
                        db.session.rollback()
                else:
                    flash("信息填写错误，请检查后重新输入！！！")
        return redirect(url_for("main.add_vip"))
    programs = Program.query.filter_by(status=1).order_by(Program.sort_num.desc()).all()
    return render_template("add_vip.html", add_vip_form=add_vip_form, programs=programs)


@main.route("/vip_list")
def vip_list():
    vips = VIP.query.all()
    return render_template("vip_list.html", vips=vips)


@main.route("/recharge", methods=["GET", "POST"])
def recharge():
    if request.method == "POST":
        card_id = request.form.get("card_id_input", None)
        if not card_id:
            flash("错误，请先输入卡号，点击查询！")
        else:
            vip = VIP.query.filter_by(card_id=card_id).first()
            if vip is not None:
                money = float("0"+request.form.get("money", 0))
                if money < 0:
                    money = 0.0
                amount = float("0"+request.form.get("amount", 0))
                if amount < 0:
                    amount = 0.0
                proposer_name = request.form.get("proposer")
                proposer_name = proposer_name.split("|")[0].rstrip()
                proposer = Employee.query.filter_by(name=proposer_name).first()
                p_count = (len(request.form)-4) // 3
                print(money, amount, p_count)
                for i in range(1, p_count+1):
                    program = request.form.get("program"+str(i), None)
                    program = program.split("|")[0].rstrip()
                    prog_instance = Program.query.filter_by(name=program).first()
                    if prog_instance is None:
                        continue
                    program_id = prog_instance.id
                    count = int("0"+request.form.get("recharge_count"+str(i), None))
                    m = float("0"+request.form.get("recharge_money"+str(i), None))
                    plan = PlanCounting.query.filter_by(program_id=program_id, card_id=vip.id).first()
                    if plan is None:
                        continue
                    if count < 0:
                        count = 0
                    plan.count += count
                    if m < 0:
                        m = 0.0
                    db.session.add(plan)
                    print(program, count, m)
                vip.money += money
                db.session.add(vip)
                try:
                    db.session.commit()
                except IntegrityError or InvalidRequestError as e:
                    flash(str(e))
                else:
                    flash("充值成功！")
            # print(request.form)
        return redirect(url_for("main.recharge"))

    employees = Employee.query.filter_by(status=1).all()
    return render_template("recharge.html", employees=employees)


# @main.route("/recharge/<card_id>", methods=["GET", "POST"])
# def recharge_id(card_id):
#     v = VIP.query.filter_by(card_id=card_id).first_or_404()
#     form = RechargeForm()
#     form.program_recharge.program.choices = [(int(p.id), p.name) for p in Program.query.filter_by(status=1)]
#     form.proposer.choices = [(int(p.id), p.name) for p in Employee.query.filter_by(status=1)]
#     if form.validate_on_submit():
#         return redirect(url_for("main.recharge_id"))
#
#     return render_template("recharge_id.html", form=form, vip=v)


@main.route("/consume", methods=["GET", "POST"])
def consume():
    if request.method == "POST":
        # l = ""
        if request.form.get("vip_normal_consume", False):
            card_id = request.form.get("vip_cardid")
            vip = VIP.query.filter_by(card_id=card_id).first()
            if vip in None:
                flash("消费请求失败，会员卡号不存在，请重新输入！")
                return redirect(url_for("main.consume"))
            plans = vip.plans
            plan_count = len(plans)
            length = len(request.form) - 2 - plan_count
            if length < 4 or length % 4 != 0:
                flash("信息填写错误！！！")
                return redirect(url_for("main.consume"))
            for i in range(1, int(length/4)+1):
                program_name = request.form.get("vip_program"+str(i))
                program = Program.query.filter_by(name=program_name).first()
                if program is None:
                    flash("发生严重错误，请重试！")
                    app_log("fun[consume] 发生严重错误，表单中的Program_name[%s]在数据库中不存在!" % program_name)
                    return redirect(url_for("main.consume"))
                price = float("0"+request.form.get("vip_price"+str(i)))
                count = int("0"+request.form.get("vip_count"+str(i)))
                if count < 0:
                    count = 0
                if price < 0:
                    price = 0.0
                if count == 0 or price == 0.0:
                    flash("[%s]的单价或消费次数输入错误，请重新输入！  <code>该项未产生消费！</code>" % program_name)
                proposer_name = request.form.get("vip_employee"+str(i))
                proposer_name = proposer_name.split("|")[0].rstrip()
                vip.money -= (price * count)
                # todo : 添加消费记录
                db.session.add(program)
            for p in vip.plans:
                count = int("0"+request.form.get("consume_count"+str(p.id)))
                if count < 0:
                    count = 0
                    flash("[%s]的消费次数输入错误，请重新输入！  <code>该项未产生消费！</code>" % p.name)
                p.count -= count
                db.session.add(p)
            try:
                db.session.commit()
            except Exception as e:
                flash("发生严重错误，请重试！")
                app_log("fun[consume] 数据保存时发生错误!! %s " % str(e))
            else:
                flash("消费成功！")
            return redirect(url_for("main.consume"))
        elif request.form.get("once_consume", False):
            length = len(request.form)
            if length < 4 or length % 4 != 0:
                flash("信息填写错误！！！")
                return redirect(url_for("main.consume"))
            for i in range(1, int(length/4)+1):
                program_name = request.form.get("program"+str(i))
                price = float("0"+request.form.get("price"+str(i)))
                if price < 0:
                    price = 0
                count = int("0"+request.form.get("count"+str(i)))
                if count < 0:
                    count = 0
                if price == 0 or count == 0:
                    flash("[%s]的单价或消费次数输入错误，请重新输入！  <code>该项未产生消费！</code>" % program_name)
                proposer_name = request.form.get("employee"+str(i))
                proposer_name = proposer_name.split("|")[0].rstrip()
            flash("消费成功！")
            return redirect(url_for("main.consume"))
        elif request.form.get("vip_count_consume", False):
            pass
        else:
            flash("无信息，请重试！")
            return redirect(url_for("main.consume"))
    employees = Employee.query.filter_by(status=1).all()
    programs = Program.query.filter_by(status=1).order_by(Program.sort_num.desc()).all()
    return render_template("consume.html", employees=employees, programs=programs)


@main.route('/q/')
def q():
    return str([m.name for m in Employee.query.all()])


@main.route('/example')
def example():
    return render_template("example.html")


@main.route('/record')
def record():
    return "<h1>还未完成</h1>"


@main.route('/log')
def log():
    return "<h1>还未完成</h1>"