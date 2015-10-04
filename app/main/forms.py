# encoding=utf-8
from wtforms import StringField, SubmitField, SelectField, TextAreaField, FloatField, IntegerField, FormField
from flask.ext.wtf import Form
from wtforms.validators import DataRequired
from app.models import Employee

class EmployeeForm(Form):
    name = StringField("员工姓名", validators=[DataRequired()])
    code = StringField("员工编码")
    phone = StringField("员工电话")
    status = SelectField("员工状态", choices=[(1, "正常"), (2, "禁用")], validators=[DataRequired()], coerce=int)
    others = TextAreaField("备注")
    submit = SubmitField("提交")


class ProgramForm(Form):
    name = StringField("项目名称", validators=[DataRequired()])
    price = FloatField("项目单价", validators=[DataRequired()])
    status = SelectField("显示状态", choices=[(1, "可见"), (2, "隐藏")], validators=[DataRequired()], coerce=int)
    sort_num = IntegerField("排序（排序值越大显示越靠前）", validators=[DataRequired()], default=1)
    submit = SubmitField("提交")


class NewVIPForm(Form):
    card_id = StringField("会员卡ID", validators=[DataRequired()])
    name = StringField("姓名", validators=[DataRequired()])
    sex = SelectField("性别",choices=[(1, '男'), (0, '女')], coerce=int, default=1)
    phone = StringField("电话")
    money = FloatField("储值金额", default=0.0)
    money_actully = FloatField("实收金额", default=0.0)
    proposer = SelectField("办卡人", coerce=int)
    submit = SubmitField("提交")


class BalanceRechargeForm(Form):
    money = FloatField("充值金额", default=0.0)
    money_actully = FloatField("实收金额", default=0.0)
    other = StringField("备注")


class ProgramRechargeForm(Form):
    program = SelectField("项目", coerce=int)
    count = IntegerField("充值次数", default=0)
    money = FloatField("收费金额", default=0.0)
    other = StringField("备注信息")


class RechargeForm(Form):
    balance_recharge = FormField(BalanceRechargeForm, label="余额充值")
    program_recharge = FormField(ProgramRechargeForm , label="项目充次")
    proposer = SelectField("销售人员", coerce=int, validators=[DataRequired()])
    submit = SubmitField("提交")


class NormalConsumeForm(Form):
    program = SelectField("项目", coerce=int)
    price = StringField("单价")
    count = FloatField("数量")
    sum = FloatField("合计")


class PlanConsumeForm(Form):
    pass


class ConsumeForm(Form):
    normal = FormField(NormalConsumeForm, label="普通消费")
    plan = FormField(PlanConsumeForm, label="计次消费")
    proposer = SelectField("销售人员", coerce=int, validators=[DataRequired()])
    submit = SubmitField("提交")