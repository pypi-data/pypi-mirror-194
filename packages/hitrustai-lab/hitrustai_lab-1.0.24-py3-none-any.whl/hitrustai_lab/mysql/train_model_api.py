
from hitrustai_lab.matrix.model_performance import ModelPerfornance
from hitrustai_lab.orm.Tables.ModelPerformance import Model_Performance
import pandas as pd
import json
from hitrustai_lab.mysql.connenction_db import open_connection
from sqlalchemy.orm import sessionmaker

dict_init_arg = {
    "list_y_test": list,
    "list_y_score": list,
    "customer_id_lst": str,
    "training_id_lst": str,
    "model_id_lst": str,
    "profile_id_lst": str,
    "tag_lst": str,
    "connector_id_lst": str,
    "institute_id_lst": str,
    "model_name_lst": str,
    "training_start_time_lst": str,
    "total_training_time_lst": str,
    "training_start_time_lst": str,
    "training_end_time_lst": str,
    "number_of_training_data_lst": str,
    "number_of_positive_samples_in_training_data": str,
    "number_of_negative_samples_in_training_data": str,
    "number_of_validation_data": str,
    "true_label_column_lst": str,
    "number_of_positive_samples_in_validation_data": str,
    "number_of_negative_samples_in_validation_data": str,
}


class TrainModelToSQl:
    def __init__(self, dict_init_arg, host="192.168.10.102", port="3305", user="root", passwd="root16313302", db="diia_test", table_name="") -> None:
        self.engine = open_connection(host=host, port=port, user=user, passwd=passwd, db=db)
        self.dict_init_arg = dict_init_arg
        self.table_name = table_name

    def performance(self):
        threshold_lst = []
        tp_lst = []
        fp_lst = []
        tn_lst = []
        fn_lst = []
        accuracy_lst = []
        precision_lst = []
        recall_lst = []
        f1_score_lst = []
        fnr_lst = []
        fpr_lst = []
        npv_lst = []
        fdr_lst = []
        for_lst = []
        tnr_lst = []
        auc_lst = []

        mp = ModelPerfornance(score_type='policy_score')
        result = mp.performance_output(
            self.dict_init_arg["list_y_test"], self.dict_init_arg["list_y_score"])
        threshold_lst.append(result['threshold_lst'])
        tp_lst.append(result['tp_lst'])
        fp_lst.append(result['fp_lst'])
        tn_lst.append(result['tn_lst'])
        fn_lst.append(result['fn_lst'])
        accuracy_lst.append(result['accuracy_lst'])
        precision_lst.append(result['precision_lst'])
        recall_lst.append(result['recall_lst'])
        f1_score_lst.append(result['f1_score_lst'])
        fnr_lst.append(result['fnr_lst'])
        fpr_lst.append(result['fpr_lst'])
        npv_lst.append(result['npv_lst'])
        fdr_lst.append(result['fdr_lst'])
        for_lst.append(result['for_lst'])
        tnr_lst.append(result['tnr_lst'])
        auc_lst.append(result['auc_lst'])
        result = {
            'customer_id': self.dict_init_arg["customer_id_lst"],
            'training_id': self.dict_init_arg["training_id_lst"],
            'model_id': self.dict_init_arg["model_id_lst"],
            'profile_id': self.dict_init_arg["profile_id_lst"],
            'tag': self.dict_init_arg["tag_lst"],
            'connector_id': self.dict_init_arg["connector_id_lst"],
            'institute_id': self.dict_init_arg["institute_id_lst"],
            'operator_id': self.dict_init_arg["operator_id_lst"],
            'model_name': self.dict_init_arg["model_name_lst"],
            'training_start_time': self.dict_init_arg["training_start_time_lst"],
            'training_end_time': self.dict_init_arg["training_end_time_lst"],
            'total_training_time': self.dict_init_arg["total_training_time_lst"],
            'training_data_start_date': self.dict_init_arg["training_start_time_lst"],
            'training_data_end_date': self.dict_init_arg["training_end_time_lst"],
            'number_of_training_data': self.dict_init_arg["number_of_training_data_lst"],
            'number_of_positive_samples_in_training_data': self.dict_init_arg["number_of_positive_samples_in_training_data"],
            'number_of_negative_samples_in_training_data': self.dict_init_arg["number_of_negative_samples_in_training_data"],
            'number_of_validation_data': self.dict_init_arg["number_of_validation_data"],
            'true_label_column': self.dict_init_arg["true_label_column_lst"],
            'number_of_positive_samples_in_validation_data': self.dict_init_arg["number_of_positive_samples_in_validation_data"],
            'number_of_negative_samples_in_validation_data': self.dict_init_arg["number_of_negative_samples_in_validation_data"],
            'threshold': threshold_lst,
            'tp': tp_lst,
            'fp': fp_lst,
            'tn': tn_lst,
            'fn': fn_lst,
            'accuracy': accuracy_lst,
            'ppv': precision_lst,
            'recall': recall_lst,
            'f1_score': f1_score_lst,
            'fnr': fnr_lst,
            'fpr': fpr_lst,
            'npv': npv_lst,
            'fdr': fdr_lst,
            'for_': for_lst,
            'tnr': tnr_lst,
            'auc': auc_lst,
            # 'create_time':datetime.datetime.now()
        }
        return result

    def dict_to_dataframe(self):
        reslt = self.performance()
        df = pd.DataFrame(data=reslt)
        df['total_training_time'] = df.total_training_time.dt.seconds
        df['training_data_start_date'] = df.training_data_start_date.dt.date
        df['training_data_end_date'] = df.training_data_end_date.dt.date
        df['threshold'] = df['threshold'].apply(lambda x: json.dumps(x))
        df['tp'] = df['tp'].apply(lambda x: json.dumps(x))
        df['fp'] = df['fp'].apply(lambda x: json.dumps(x))
        df['tn'] = df['tn'].apply(lambda x: json.dumps(x))
        df['fn'] = df['fn'].apply(lambda x: json.dumps(x))
        df['accuracy'] = df['accuracy'].apply(lambda x: json.dumps(x))
        df['ppv'] = df['ppv'].apply(lambda x: json.dumps(x))
        df['recall'] = df['recall'].apply(lambda x: json.dumps(x))
        df['f1_score'] = df['f1_score'].apply(lambda x: json.dumps(x))
        df['fnr'] = df['fnr'].apply(lambda x: json.dumps(x))
        df['fpr'] = df['fpr'].apply(lambda x: json.dumps(x))
        df['npv'] = df['npv'].apply(lambda x: json.dumps(x))
        df['fdr'] = df['fdr'].apply(lambda x: json.dumps(x))
        df['for_'] = df['for_'].apply(lambda x: json.dumps(x))
        df['tnr'] = df['tnr'].apply(lambda x: json.dumps(x))
        return df

    def insert_db(self):
        df = self.dict_to_dataframe()

        Session = sessionmaker(bind=self.engine)
        try:
            session = Session()
            Model_Performance.__tablename__ = self.table_name
            session.bulk_insert_mappings(Model_Performance, df.to_dict(orient='records'))
            session.commit()
        except Exception as e:
            session.rollback()
            print(e)
        finally:
            session.close()


if __name__ == '__main__':
    tmts = TrainModelToSQl(dict_init_arg, host="192.168.10.102", port="3305", user="root", passwd="root16313302", db="diia_test", table_name="model_performance")
    tmts.insert_db()
