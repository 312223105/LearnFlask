# encoding=utf-8

from . import main
from flask import render_template, session, redirect, url_for, flash, request, jsonify
from .forms import *
from .. import db
from ..models import *

@main.route("/api/employees")
def get_employees():
    result = Employee.query.filter_by(status=1).all()
    data = [{"id":i.id, "name":i.name, "code":i.code} for i in result]
    # data = [{"id":1,"name":"小王","code":"101"}, {"id":2,"name":"小李","code":"102"},{"id":3,"name":"徐哲","code":"103"}]
    return jsonify({"data":data})


@main.route("/api/programs")
def get_programs():
    result = Program.query.filter_by(status=1).order_by(Program.sort_num.desc()).all()
    data = [{"id":i.id, "name":i.name, "price":str(i.price)} for i in result]
    # data = [{"id":1,"name":"剪发"}, {"id":2,"name":"洗头"},{"id":3,"name":"染发"}]
    return jsonify({"data": data})


@main.route("/api/vip/<card_id>")
def get_vip(card_id):
    result = VIP.query.filter_by(card_id=card_id).first()
    if result:
        data = {"id":result.id,
                "card_id": result.card_id,
                "name": result.name,
                "phone": result.phone,
                "money": result.money,
                "create_time": result.create_time.strftime("%Y-%m-%d %H:%M:%S"),
                "plans":[]
                }
        for p in result.plans:
            data["plans"].append({"program_name": p.program.name, "rest_count": p.count, "id": p.id,
                                 "create_time": p.create_time.strftime("%Y-%m-%d %H:%M:%S"),
                                  "program_price": p.program.price
                                 })
        return jsonify({"data":data})
    else:
        return jsonify({"data":None})