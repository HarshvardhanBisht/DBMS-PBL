from app import app, db, Genre, SubscriptionPlan, Movie, Series, Season, Episode, Actor, Casting
with app.app_context():
    db.create_all()
    if not Genre.query.first():
        g1=Genre(genre_name="Drama"); g2=Genre(genre_name="Action")
        db.session.add_all([g1,g2]); db.session.flush()
        db.session.add_all([
          SubscriptionPlan(plan_name="Basic",price=149,duration_days=30,description="Sample plan"),
          SubscriptionPlan(plan_name="Standard",price=299,duration_days=30,description="Sample plan"),
          SubscriptionPlan(plan_name="Premium",price=499,duration_days=30,description="Sample plan"),
          Movie(title="The Last Signal",description="A fictional mystery film.",release_year=2025,language="Hindi",genre_id=g1.genre_id),
          Movie(title="Chasing Tomorrow",description="A fictional adventure film.",release_year=2024,language="English",genre_id=g2.genre_id)])
        show=Series(title="City of Stories",description="A fictional drama series.",release_year=2025,language="Hindi",genre_id=g1.genre_id)
        db.session.add(show); db.session.flush()
        season=Season(series_id=show.series_id,season_number=1,title="Season One")
        actor=Actor(actor_name="Demo Actor"); db.session.add_all([season,actor]); db.session.flush()
        ep=Episode(season_id=season.season_id,episode_number=1,title="The Beginning",duration_minutes=42)
        db.session.add(ep); db.session.flush()
        db.session.add(Casting(actor_id=actor.actor_id,episode_id=ep.episode_id,role_name="Lead"))
        db.session.commit()
    print("Sample data added.")
