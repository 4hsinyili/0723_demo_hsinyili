import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, DateTime, Float
from datetime import datetime
import time

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
    topic_id = Column(Integer)
    created_at = Column(DateTime)
    triggered_at = Column(DateTime)
    view_count = Column(Integer)

    def __init__(self, url, topic_id, created_at, triggered_at, view_count):
        self.url = url
        self.topic_id = topic_id
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


class TrackError(Base):
    __tablename__ = 'track_error'
    id = Column(Integer, primary_key=True)
    triggered_at = Column(DateTime)
    topic_id = Column(Integer)
    url = Column(String(255))
    loop_count = Column(Integer)
    offset = Column(Integer)
    message = Column(String(10000))

    def __init__(self, triggered_at, topic_id, url, loop_count, offset, message):
        self.triggered_at = triggered_at
        self.topic_id = topic_id
        self.url = url
        self.loop_count = loop_count
        self.offset = offset
        self.message = message


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

    def check_session(self):
        try:
            session = self.session
            session.query(TrackError).first()
        except Exception:
            time.sleep(5)
            self.session = self.db_connect()
            session = self.session
        return session

    def to_dict(self, result):
        result = result.__dict__
        del result['_sa_instance_state']
        return result

    def bulk_insert(self, table, values):
        new_records = [table(**value) for value in values]
        session = self.check_session()
        session.add_all(new_records)
        session.commit()
        session.close()

    def get_latest_topic_id(self):
        session = self.check_session()
        raw = session.query(Topic).order_by(Topic.topic_id.desc()).first()
        session.close()
        if raw:
            result = self.to_dict(raw)
            return result['topic_id']
        else:
            return 0

    def insert_topic(self, topics):
        session = self.check_session()
        session.bulk_insert_mappings(Topic, topics)
        session.commit()
        session.close()

    def get_urls(self, offset, limit):
        session = self.check_session()
        raw = session.query(Topic).filter(Topic.stop_track == 0).order_by(Topic.topic_id).limit(limit).offset(offset).all()
        session.close()
        if raw:
            results = [self.to_dict(i)['url'] for i in raw]
            return results
        else:
            return None

    def get_urls_count(self):
        session = self.check_session()
        raw = session.query(Topic).filter(Topic.stop_track == 0).count()
        session.close()
        if raw:
            result = raw
            return result
        else:
            return None

    def get_view_counts(self, url):
        session = self.check_session()
        query = session.query(Track).filter(Track.url == url).order_by(Track.id)
        raw = query.all()
        session.close()
        if raw:
            results = [self.to_dict(i)['view_count'] for i in self.to_dict(raw)]
            return results
        else:
            return None

    def insert_track(self, tracks):
        session = self.check_session()
        session.bulk_insert_mappings(Track, tracks)
        session.commit()
        session.close()

    def insert_monitor(self, monitor):
        session = self.check_session()
        record = Monitor(**monitor)
        session.add(record)
        session.commit()
        session.close()

    def update_stop_track(self):
        session = self.check_session()
        now = datetime.utcnow()
        session.query(Topic).filter(Topic.stop_track == 0)\
            .filter(Topic.stop_track_at <= now).update({'stop_track': 1})
        session.commit()
        session.close()

    def update_monitor(self, triggered_at, target_topics_count, end_at, execution_count):
        execution_time = end_at.timestamp() - triggered_at.timestamp()
        session = self.check_session()
        session.query(Monitor).filter(Monitor.triggered_at == triggered_at)\
            .update({
                'target_topics_count': target_topics_count,
                'execution_time': execution_time,
                'execution_count': execution_count,
                })
        session.commit()
        session.close()

    def insert_track_error(self, error):
        session = self.check_session()
        record = TrackError(**error)
        session.add(record)
        session.commit()
        session.close()
