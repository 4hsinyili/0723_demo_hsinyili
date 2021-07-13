import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, DateTime, Float
from datetime import datetime

Base = declarative_base()


class Topic(Base):
    __tablename__ = 'topic'
    url = Column(String(255), primary_key=True)
    title = Column(String(255))
    topic_id = Column(Integer)
    post_time = Column(DateTime)
    stop_track_at = Column(DateTime)
    stop_track = Column(Boolean)
    post_by = Column(String(255))
    created_at = Column(DateTime)
    triggered_at = Column(DateTime)

    def __init__(self, url, title, topic_id, post_time, stop_track_at, stop_track, post_by, created_at, triggered_at):
        self.url = url
        self.title = title
        self.topic_id = topic_id
        self.post_time = post_time
        self.stop_track_at = stop_track_at
        self.stop_track = stop_track
        self.post_by = post_by
        self.created_at = created_at
        self.triggered_at = triggered_at


class Track(Base):
    __tablename__ = 'track'
    id = Column(Integer, primary_key=True)
    url = Column(ForeignKey('topic.url'))
    created_at = Column(DateTime)
    triggered_at = Column(DateTime)
    view_count = Column(Integer)

    def __init__(self, url, created_at, triggered_at, view_count):
        self.url = url
        self.created_at = created_at
        self.triggered_at = triggered_at
        self.view_count = view_count


class Monitor(Base):
    __tablename__ = 'monitor'
    id = Column(Integer, primary_key=True)
    triggered_at = Column(DateTime)
    new_topics_count = Column(Integer)
    target_topics_count = Column(Integer)
    execution_time = Column(Float)
    execution_count = Column(Float)

    def __init__(self, triggered_at, new_topics_count, target_topics_count=0, execution_time=0, execution_count=0):
        self.triggered_at = triggered_at
        self.new_topics_count = new_topics_count
        self.target_topics_count = target_topics_count
        self.execution_time = execution_time
        self.execution_count = execution_count


class Query():
    def __init__(self, host, user, pwd, port, db_name, *args, **kwargs):
        self.host = host
        self.user = user
        self.password = pwd
        self.port = port
        self.db_name = db_name
        self.session = self.db_connect()

    def db_connect(self):
        engine = sqlalchemy.create_engine(
            f"mysql+pymysql://{self.user}:{self.password}@{self.host}/{self.db_name}", connect_args={'connect_timeout': 60}
            )
        Session = sqlalchemy.orm.sessionmaker(bind=engine)
        return Session()

    def to_dict(self, result):
        result = result.__dict__
        del result['_sa_instance_state']
        return result

    def bulk_insert(self, table, values):
        new_records = [table(**value) for value in values]
        session = self.session
        session.add_all(new_records)
        session.commit()
        session.close()

    def get_latest_topic_id(self):
        session = self.session
        raw = session.query(Topic).order_by(Topic.topic_id.desc()).first()
        session.close()
        if raw:
            result = self.to_dict(raw)
            return result['topic_id']
        else:
            return None

    def insert_topic(self, topics):
        session = self.session
        session.bulk_insert_mappings(Topic, topics)
        session.commit()
        session.close()

    def get_urls(self, offset, limit):
        session = self.session
        raw = session.query(Topic).filter(Topic.stop_track == 0).order_by(Topic.topic_id).limit(limit).offset(offset).all()
        session.close()
        if raw:
            results = [self.to_dict(i)['url'] for i in raw]
            return results
        else:
            return None

    def get_view_counts(self, url):
        session = self.session
        query = session.query(Track).filter(Track.url == url).order_by(Track.id)
        raw = query.all()
        session.close()
        if raw:
            results = [self.to_dict(i)['view_count'] for i in self.to_dict(raw)]
            return results
        else:
            return None

    def insert_track(self, tracks):
        session = self.session
        session.bulk_insert_mappings(Track, tracks)
        session.commit()
        session.close()

    def insert_monitor(self, monitor):
        session = self.session
        record = Monitor(**monitor)
        session.add(record)
        session.commit()
        session.close()

    def update_stop_track(self):
        session = self.session
        now = datetime.utcnow()
        session.query(Topic).filter(Topic.stop_track == 0)\
            .filter(Topic.stop_track_at <= now).update({'stop_track': 1})
        session.commit()
        session.close()

    def update_monitor(self, triggered_at, target_topics_count, end_at, execution_count):
        execution_time = end_at.timestamp() - triggered_at.timestamp()
        session = self.session
        session.query(Monitor).filter(Monitor.triggered_at == triggered_at)\
            .update({
                'target_topics_count': target_topics_count,
                'execution_time': execution_time,
                'execution_count': execution_count,
                })
        session.commit()
        session.close()
