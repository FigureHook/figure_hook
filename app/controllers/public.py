from flask import Blueprint, render_template

from app.forms import SubscriptionForm

blueprint = Blueprint("public", __name__)


@blueprint.route("/", methods=["GET"])
def home():
    """Home page"""
    form = SubscriptionForm(
        redirect_uri="http://127.0.0.1:5000/webhook"
    )
    return render_template("index.html", form=form)