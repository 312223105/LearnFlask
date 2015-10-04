# encoding=utf-8
from datetime import datetime

from app import db


class VIP(db.Model):
    __tablename__ = 'VIPs'
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.String(10), unique=True)  # 会员卡ID
    sex = db.Column(db.Integer, nullable=False)  # 1男 0女
    name = db.Column(db.String)  # 姓名
    phone = db.Column(db.String(20))  # 电话
    create_time = db.Column(db.DateTime, default=datetime.utcnow())
    money = db.Column(db.Float, nullable=True)  # 储蓄金额
    money_actully = db.Column(db.Float, nullable=True)  # 实收金额
    proposer_id = db.Column(db.Integer, db.ForeignKey('employees.id'))  # 办卡人
    plans = db.relationship('PlanCounting', backref='VIP')  # 计次项目
    records = db.relationship('Record', backref='VIP')  # 消费记录

    def __repr__(self):
        return '<VIP card_id=%r, name=%r>' % (self.card_id, self.name)


class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True, index=True)
    phone = db.Column(db.String(20), nullable=True)
    join_time = db.Column(db.Date, default=datetime.utcnow().date())  # 加入日期
    status = db.Column(db.Integer, nullable=False)  # 1 正常 0禁用
    code = db.Column(db.String(20), nullable=True, unique=True, index=True)  # 员工编号
    others = db.Column(db.String, nullable=True)  # 备注
    VIPs = db.relationship('VIP', backref='proposer')
    records = db.relationship('Record', backref='salesman')

    def __repr__(self):
        return '<Employee id=%r, name=%r>' % (self.id, self.name)


class Program(db.Model):
    __tablename__ = 'Programs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)  # 消费项目名称
    price = db.Column(db.Float, nullable=False)  # 单价
    create_time = db.Column(db.DateTime, default=datetime.utcnow())
    sort_num = db.Column(db.Integer, default=0)  # 排序值越大显示越靠前
    status = db.Column(db.Integer, default=1)  # 1可见 2隐藏
    records = db.relationship('Record', backref='program')
    plan = db.relationship('PlanCounting', backref='program')

    def __repr__(self):
        return '<Program id=%r, name=%r>' % (self.id, self.name)


class PlanCounting(db.Model):  # 计次项目
    __tablename__ = 'plancounting'
    id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.Integer, db.ForeignKey('Programs.id'))
    create_time = db.Column(db.DateTime, default=datetime.utcnow())
    card_id = db.Column(db.Integer, db.ForeignKey('VIPs.id'))  # 属性名VIP
    count = db.Column(db.Integer, nullable=False)  # 次数
    # money = db.Column(db.Float, nullable=False)  # 实收金额
    others = db.Column(db.String, nullable=True)  # 备注

    def __repr__(self):
        return '<PlanCounting id=%r, count=%r>' % (self.id, self.count)


class Record(db.Model):
    __tablename__ = 'Records'
    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DateTime, default=datetime.utcnow())
    card_id = db.Column(db.Integer, db.ForeignKey('VIPs.id'))
    program_id = db.Column(db.Integer, db.ForeignKey('Programs.id'), nullable=False)
    consume_type = db.Column(db.Integer, nullable=False)  # 消费类型 0普通消费 1计次消费
    count = db.Column(db.Float, default=0.0)  # 消费金额
    balance_pay = db.Column(db.Float, default=0.0)  # 余额支付
    cash_pay = db.Column(db.Float, default=0.0)  # 现金支付
    salesman_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    other = db.Column(db.String, nullable=True)

    def __repr__(self):
        return '<Record id=%r, VIP_name=%r, Program_name=%r, count=%r>' % \
               (self.id, self.VIP.name, self.Program.name, self.count)
