from sqlalchemy import Column, Integer, Numeric
from sqlalchemy.dialects.mysql import TIMESTAMP, VARCHAR, LONGTEXT
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Model_Performance(Base):
    __tablename__ = 'model_performance'

    pk_id = Column(Integer, primary_key=True,
                   autoincrement=True, nullable=False)
    customer_id = Column(VARCHAR(20))
    training_id = Column(VARCHAR(45))
    model_id = Column(VARCHAR(20))
    profile_id = Column(VARCHAR(20))
    tag = Column(VARCHAR(20))
    connector_id = Column(VARCHAR(255))
    institute_id = Column(VARCHAR(255))
    operator_id = Column(VARCHAR(255))
    model_name = Column(VARCHAR(100))
    training_start_time = Column(TIMESTAMP())
    training_end_time = Column(TIMESTAMP())
    total_training_time = Column(Integer)
    training_data_start_date = Column(TIMESTAMP())
    training_data_end_date = Column(TIMESTAMP())
    number_of_training_data = Column(Integer)
    number_of_positive_samples_in_training_data = Column(Integer)
    number_of_negative_samples_in_training_data = Column(Integer)
    number_of_validation_data = Column(Integer)
    true_label_column = Column(VARCHAR(45))
    number_of_positive_samples_in_validation_data = Column(Integer)
    number_of_negative_samples_in_validation_data = Column(Integer)
    threshold = Column(LONGTEXT)
    tp = Column(LONGTEXT)
    fp = Column(LONGTEXT)
    tn = Column(LONGTEXT)
    fn = Column(LONGTEXT)
    accuracy = Column(LONGTEXT)
    ppv = Column(LONGTEXT)
    recall = Column(LONGTEXT)
    f1_score = Column(LONGTEXT)
    fnr = Column(LONGTEXT)
    fpr = Column(LONGTEXT)
    npv = Column(LONGTEXT)
    fdr = Column(LONGTEXT)
    for_ = Column(LONGTEXT)
    tnr = Column(LONGTEXT)
    auc = Column(Numeric)
    create_time = Column(TIMESTAMP())
    
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            setattr(self, property, value)

    def get_attr_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}