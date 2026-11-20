import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "development-key-change-me")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///movie_streaming.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SubscriptionPlan(db.Model):
    __tablename__ = "subscription_plans"
    plan_id = db.Column(db.Integer, primary_key=True)
    plan_name = db.Column(db.String(50), unique=True, nullable=False)
    price = db.Column(db.Numeric(8,2), nullable=False)
    duration_days = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255))

class Payment(db.Model):
    __tablename__ = "payments"
    payment_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey("subscription_plans.plan_id"), nullable=False)
    amount = db.Column(db.Numeric(8,2), nullable=False)
    payment_status = db.Column(db.String(20), default="SIMULATED")
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)

class Genre(db.Model):
    __tablename__ = "genres"
    genre_id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(60), unique=True, nullable=False)

class Movie(db.Model):
    __tablename__ = "movies"
    movie_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180), nullable=False)
    description = db.Column(db.Text)
    release_year = db.Column(db.Integer)
    language = db.Column(db.String(60))
    rating = db.Column(db.Numeric(3,1), default=0)
    genre_id = db.Column(db.Integer, db.ForeignKey("genres.genre_id"))

class Series(db.Model):
    __tablename__ = "series"
    series_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180), nullable=False)
    description = db.Column(db.Text)
    release_year = db.Column(db.Integer)
    language = db.Column(db.String(60))
    rating = db.Column(db.Numeric(3,1), default=0)
    genre_id = db.Column(db.Integer, db.ForeignKey("genres.genre_id"))

class Season(db.Model):
    __tablename__ = "seasons"
    season_id = db.Column(db.Integer, primary_key=True)
    series_id = db.Column(db.Integer, db.ForeignKey("series.series_id"), nullable=False)
    season_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(120))
    __table_args__ = (db.UniqueConstraint("series_id", "season_number"),)

class Episode(db.Model):
    __tablename__ = "episodes"
    episode_id = db.Column(db.Integer, primary_key=True)
    season_id = db.Column(db.Integer, db.ForeignKey("seasons.season_id"), nullable=False)
    episode_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(180), nullable=False)
    duration_minutes = db.Column(db.Integer)
    description = db.Column(db.Text)
    __table_args__ = (db.UniqueConstraint("season_id", "episode_number"),)

class Actor(db.Model):
    __tablename__ = "actors"
    actor_id = db.Column(db.Integer, primary_key=True)
    actor_name = db.Column(db.String(120), nullable=False)

class Casting(db.Model):
    __tablename__ = "casting"
    casting_id = db.Column(db.Integer, primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey("actors.actor_id"), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.movie_id"))
    episode_id = db.Column(db.Integer, db.ForeignKey("episodes.episode_id"))
    role_name = db.Column(db.String(100))
    __table_args__ = (db.CheckConstraint(
        "(movie_id IS NOT NULL AND episode_id IS NULL) OR (movie_id IS NULL AND episode_id IS NOT NULL)",
        name="ck_casting_one_target"),)

class Review(db.Model):
    __tablename__ = "reviews"
    review_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.movie_id"))
    series_id = db.Column(db.Integer, db.ForeignKey("series.series_id"))
    episode_id = db.Column(db.Integer, db.ForeignKey("episodes.episode_id"))
    review_text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    __table_args__ = (db.CheckConstraint(
        "((movie_id IS NOT NULL) + (series_id IS NOT NULL) + (episode_id IS NOT NULL)) = 1",
        name="ck_review_one_target"), db.CheckConstraint("rating BETWEEN 1 AND 5", name="ck_review_rating"))

class Watchlist(db.Model):
    __tablename__ = "watchlists"
    watchlist_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.movie_id"))
    series_id = db.Column(db.Integer, db.ForeignKey("series.series_id"))
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    __table_args__ = (db.CheckConstraint(
        "(movie_id IS NOT NULL AND series_id IS NULL) OR (movie_id IS NULL AND series_id IS NOT NULL)",
        name="ck_watchlist_one_target"),)

def logged_in():
    return "user_id" in session

@app.route("/")
def home():
    return render_template("index.html", movies=Movie.query.all(), series=Series.query.all())

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        name=request.form.get("full_name","").strip()
        email=request.form.get("email","").strip().lower()
        password=request.form.get("password","")
        if not name or not email or len(password)<8:
            flash("Fill all fields. Password must contain at least 8 characters.")
        elif User.query.filter_by(email=email).first():
            flash("This email is already registered.")
        else:
            db.session.add(User(full_name=name,email=email,password_hash=generate_password_hash(password)))
            db.session.commit()
            flash("Account created. Please log in.")
            return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        user=User.query.filter_by(email=request.form.get("email","").strip().lower()).first()
        if user and check_password_hash(user.password_hash,request.form.get("password","")):
            session["user_id"]=user.user_id
            session["user_name"]=user.full_name
            return redirect(url_for("home"))
        flash("Incorrect email or password.")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/plans")
def plans():
    return render_template("plans.html",plans=SubscriptionPlan.query.order_by(SubscriptionPlan.price).all())

@app.route("/subscribe/<int:plan_id>",methods=["POST"])
def subscribe(plan_id):
    if not logged_in():
        return redirect(url_for("login"))
    plan=db.session.get(SubscriptionPlan,plan_id)
    if not plan:
        flash("Plan not found.")
    else:
        db.session.add(Payment(user_id=session["user_id"],plan_id=plan.plan_id,amount=plan.price))
        db.session.commit()
        flash("Demo subscription saved. No real payment was taken.")
    return redirect(url_for("plans"))

@app.route("/search")
def search():
    q=request.args.get("q","").strip()
    movies=Movie.query.filter(Movie.title.ilike(f"%{q}%")).all() if q else []
    series=Series.query.filter(Series.title.ilike(f"%{q}%")).all() if q else []
    return render_template("search.html",q=q,movies=movies,series=series)

@app.route("/watchlist")
def watchlist():
    if not logged_in(): return redirect(url_for("login"))
    rows=Watchlist.query.filter_by(user_id=session["user_id"]).all()
    movies=[db.session.get(Movie,r.movie_id) for r in rows if r.movie_id]
    series=[db.session.get(Series,r.series_id) for r in rows if r.series_id]
    return render_template("watchlist.html",movies=movies,series=series)

@app.route("/watchlist/add/<kind>/<int:item_id>",methods=["POST"])
def add_watchlist(kind,item_id):
    if not logged_in(): return redirect(url_for("login"))
    uid=session["user_id"]
    if kind=="movie" and db.session.get(Movie,item_id):
        exists=Watchlist.query.filter_by(user_id=uid,movie_id=item_id).first()
        if not exists: db.session.add(Watchlist(user_id=uid,movie_id=item_id))
    elif kind=="series" and db.session.get(Series,item_id):
        exists=Watchlist.query.filter_by(user_id=uid,series_id=item_id).first()
        if not exists: db.session.add(Watchlist(user_id=uid,series_id=item_id))
    else:
        flash("Content not found."); return redirect(url_for("home"))
    db.session.commit()
    flash("Added to watchlist.")
    return redirect(request.referrer or url_for("home"))

@app.route("/health")
def health():
    return {"status":"ok"}

@app.cli.command("init-db")
def init_db():
    db.create_all()
    print("Database tables created.")

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
