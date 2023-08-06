import os
from os.path import isfile, join
import multiprocessing as mp
from decouple import AutoConfig
from hitrustai_lab.model_train.core.message import MessageQueue
from hitrustai_lab.model_train.core.utils import return_code, decrypt_passwd, open_connection, close_connection
from hitrustai_lab.apollo.apollo_client import ApolloClient
from hitrustai_lab.apollo.util import check_apollo_change, get_apollo_value


class HitrustaiTrainTemple:
    def __init__(self, dict_model, init_logger, so_name="./data/passwd.so"):
        self.kg_list = None
        self.accuracy = None
        self.precision = None
        self.recall = None
        self.f1_score = None
        self.finish_reason = None
        self.SQLALCHEMY_DATABASE_URI = None
        self.mq_info = None
        self.so_name = so_name
        self.dict_model = dict_model
        self.train_info = None
        self.init_logger = init_logger

    def read_train_conf_env(self):
        config = AutoConfig(search_path=os.getcwd() + "/env")
        # check docker environment exist
        CUSTOMER_ID = os.environ.get('CUSTOMER_ID')
        MODEL_ID = os.environ.get('MODEL_ID')
        TRAINING_ID = os.environ.get('TRAINING_ID')
        KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC')

        # check service .env file exist
        kafka_node = config('KAFKA_N', default='0')
        bootstrap_servers = []
        for i in range(int(kafka_node)):
            host = config('KAFKA_HOST_' + str(i + 1), default='')
            port = config('KAFKA_PORT_' + str(i + 1), default='')
            if host == "" or port == "":
                self.init_logger.error('Error: Invalid variable in env. Expected keys [KAFKA_HOST, KAFKA_PORT]')
                os.kill(0, 4)
            bootstrap_servers.append(host + ":" + port)

        self.mq_info = {
            "servers": bootstrap_servers,
            "customer_id": CUSTOMER_ID,
            "model_id": MODEL_ID,
            "training_id": TRAINING_ID,
            "topic": KAFKA_TOPIC,
            "BATCH_SIZE": int(config('Chunksize', default='100000')),
            "dataset_path": config('SOURCE_PATH_DATASET', default=''),
            "kg_path": config('SOURCE_PATH_KNOWLEDGE', default=''),
            "lib_path": config('SOURCE_PATH_LIB', default=''),
            "KAFKA_USE": config('KAFKA_USE', default=''),
            
        }
        
        mq = MessageQueue(self.mq_info["servers"], self.mq_info["customer_id"], self.mq_info["model_id"], self.mq_info["training_id"], self.mq_info["topic"], self.mq_info["KAFKA_USE"],self.init_logger)

        if self.mq_info['dataset_path'] == "" or self.mq_info['lib_path'] == "":
            self.init_logger.error("No dataset/kg/lib path")
            mq.startup(return_code["container_start_fail"], "No dataset/kg/lib path")
            return

        db_pass = config('DB_PASS', default='')
        password = decrypt_passwd(self.so_name, db_pass)
        SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
            config('DB_ENGINE', default='mysql+pymysql'),
            config('DB_USERNAME', default='test'),
            password,
            config('DB_HOST', default='127.0.0.1'),
            config('DB_PORT', default=3306),
            config('DB_NAME', default='testdb')
        )
        return SQLALCHEMY_DATABASE_URI, mq

    def read_train_conf_apollo(self):
        config = AutoConfig(search_path=os.getcwd() + "/env")
        try:
            APOLLO_URL = config('APOLLO_URL')
            APOLLO_APPID = config('APOLLO_APPID')
            APOLLO_CLUSTER = config('APOLLO_CLUSTER')
            APOLLO_SECRET = config('APOLLO_SECRET')
            APOLLO_NAMESPACE_INF = config('APOLLO_NAMESPACE_INF')
            APOLLO_NAMESPACE_MODAL = config('APOLLO_NAMESPACE_MODAL')
        except Exception:
            os.kill(0, 4)
        apollo_client = ApolloClient(
            app_id=APOLLO_APPID,
            cluster=APOLLO_CLUSTER,
            config_url=APOLLO_URL,
            secret=APOLLO_SECRET,
            change_listener=check_apollo_change)

        # check service .env file exist
        KAFKA_N = get_apollo_value(apollo_client, "KAFKA_NODE", APOLLO_NAMESPACE_INF)
        KAFKA_N = KAFKA_N.split(",")
        # kafka_node = len(KAFKA_N)
        bootstrap_servers = []
        for ip in KAFKA_N:
            host, port = ip.split(":")
            if host == "" or port == "":
                self.init_logger.error('Error: Invalid variable in env. Expected keys [KAFKA_HOST, KAFKA_PORT]')
                os.kill(0, 4)
            bootstrap_servers.append(host + ":" + port)
        self.mq_info = {
            "servers": bootstrap_servers,
            "customer_id": get_apollo_value(apollo_client, "CUSTOMER_ID", APOLLO_NAMESPACE_MODAL),
            "model_id": get_apollo_value(apollo_client, "MODEL_ID", APOLLO_NAMESPACE_MODAL),
            "training_id": get_apollo_value(apollo_client, "TRAINING_ID", APOLLO_NAMESPACE_MODAL),
            "topic": get_apollo_value(apollo_client, "TRAINING_ID", APOLLO_NAMESPACE_MODAL),
            "BATCH_SIZE": int(get_apollo_value(apollo_client, "BATCH_SIZE", APOLLO_NAMESPACE_MODAL)),

            "dataset_path": get_apollo_value(apollo_client, "SOURCE_PATH_DATASET", APOLLO_NAMESPACE_MODAL),
            "kg_path": get_apollo_value(apollo_client, "SOURCE_PATH_KNOWLEDGE", APOLLO_NAMESPACE_MODAL),
            "lib_path": get_apollo_value(apollo_client, "SOURCE_PATH_LIB", APOLLO_NAMESPACE_MODAL),
            "KAFKA_USE": get_apollo_value(apollo_client, "KAFKA_USE", APOLLO_NAMESPACE_MODAL)

        }
        mq = MessageQueue(self.mq_info["servers"], self.mq_info["customer_id"], self.mq_info["model_id"], self.mq_info["training_id"], self.mq_info["topic"], self.mq_info["KAFKA_USE"], self.init_logger)

        if self.mq_info['dataset_path'] == "" or self.mq_info['lib_path'] == "":
            self.init_logger.error("No dataset/kg/lib path")
            mq.startup(return_code["container_start_fail"], "No dataset/kg/lib path")
            return

        db_pass = get_apollo_value(apollo_client, "DB_PASS", APOLLO_NAMESPACE_INF)

        password = decrypt_passwd(self.so_name, db_pass)
        SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
            get_apollo_value(apollo_client, "DB_ENGINE", APOLLO_NAMESPACE_INF),
            get_apollo_value(apollo_client, "DB_USERNAME", APOLLO_NAMESPACE_INF),
            password,
            get_apollo_value(apollo_client, "DB_HOST", APOLLO_NAMESPACE_INF),
            get_apollo_value(apollo_client, "DB_PORT", APOLLO_NAMESPACE_INF),
            get_apollo_value(apollo_client, "DB_NAME", APOLLO_NAMESPACE_INF)
        )

        return SQLALCHEMY_DATABASE_URI, mq

    def process(self, manager_dict, lock, model, dict_model, chunksize):
        self.init_logger.info("[{}] Start to train model".format(model))
        try:
            train_model = dict_model[model]
            result = train_model.train(chunksize)
        except Exception:
            manager_dict["mq"].send(return_code["train_fail"], "0")
            self.init_logger.error('Error: [{}] training fail'.format(model))
            os.kill(0, 4)
        
        lock.acquire()
        manager_dict["progress"] += 1
        manager_dict[model] = result
        manager_dict[model + "_train_info"] = {
            "DATA_START_DATE": train_model.DATA_START_DATE,
            "DATA_TOTAL_ROW": train_model.DATA_TOTAL_ROW,
            "DATA_END_DARE": train_model.DATA_END_DARE
        }
        lock.release()

        if manager_dict["progress"] < len(dict_model.keys()):
            self.init_logger.info("[{}] Send progress: {}".format(model, manager_dict["progress"]))
            manager_dict["mq"].send(result["return_code"], str(manager_dict["progress"]*16), result["reason"])
        self.init_logger.info("[{}] {}".format(model, result))

        if result["return_code"] != return_code["train_success"]:
            self.init_logger.error('Error: [{}] training fail'.format(model))
            os.kill(0, 4)
        self.init_logger.info("[{}] Process finish".format(model))

    def train(self, module_quantity=1):
        config = AutoConfig(search_path=os.getcwd() + "/env")
        if config('ENV_METHOD') == "env":
            SQLALCHEMY_DATABASE_URI, mq = self.read_train_conf_env()
        else:
            SQLALCHEMY_DATABASE_URI, mq = self.read_train_conf_apollo()
        self.SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI

        # Generate Train and Val csv file
        # val_quantity = 450

        # Manager to create shared object.
        manager = mp.Manager()
        # Create a lock.
        lock = manager.Lock()
        # Create and Init global variables.
        manager_dict = manager.dict()
        manager_dict["mq"] = mq
        manager_dict["progress"] = 0

        models_list = list(self.dict_model.keys())

        # Multiprocess pool.
        pools = []
        for model in models_list:
            p = mp.Process(
                target=self.process,
                args=(manager_dict, lock, model, self.dict_model, self.mq_info["BATCH_SIZE"])
            )
            pools.append(p)

        for p in pools:
            p.start()
        for p in pools:
            p.join()

        # Waiting for backing to main process
        if manager_dict["progress"] < len(models_list):
            manager_dict["mq"].send(return_code["train_fail"], str(manager_dict["progress"] * 16, "Train Fail"))
            os.kill(0, 4)

        progress = "100"
        kg_list = [f for f in os.listdir(self.mq_info['lib_path']) if isfile(join(self.mq_info['lib_path'], f)) and (".pkl" in f or ".joblib" in f)]

        init_score = 0
        accuracy, precision, recall, f1_score = init_score, init_score, init_score, init_score
        if module_quantity == 1:
            finish_reason = []
            for model in models_list:
                if model not in manager_dict:
                    manager_dict["mq"].send(return_code["train_fail"], progress, manager_dict[model]["reason"])
                    os.kill(0, 4)

                if manager_dict[model]["return_code"] != return_code["train_success"]:
                    finish_reason.append(manager_dict[model]["reason"])
                accuracy += manager_dict[model]["report"]["accuracy"]
                precision += manager_dict[model]["report"]["precision"]
                recall += manager_dict[model]["report"]["recall"]
                f1_score += manager_dict[model]["report"]["f1_score"]
            accuracy = 1.0 if accuracy > 1 else round(accuracy, 2)
            precision = 1.0 if precision > 1 else round(precision, 2)
            recall = 1.0 if recall > 1 else round(recall, 2)
            f1_score = 1.0 if f1_score > 1 else round(f1_score, 2)
            
            self.kg_list = kg_list
            self.accuracy = accuracy
            self.precision = precision
            self.recall = recall
            self.f1_score = f1_score
            self.finish_reason = finish_reason
        else:
            init = 0
            accuracy_8 = precision_8 = recall_8 = f1_score_8 = init
            accuracy_7 = precision_7 = recall_7 = f1_score_7 = init
            finish_reason = []
            for model in models_list:
                if model not in manager_dict:
                    manager_dict["mq"].send(return_code["train_fail"], progress, manager_dict[model]["reason"])
                    os.kill(0, 4)

                if manager_dict[model]["f8"]["return_code"] != return_code["train_success"]:
                    finish_reason.append(manager_dict[model]["reason"])
                accuracy_8 += manager_dict[model]["f8"]["report"]["accuracy"]
                precision_8 += manager_dict[model]["f8"]["report"]["precision"]
                recall_8 += manager_dict[model]["f8"]["report"]["recall"]
                f1_score_8 += manager_dict[model]["f8"]["report"]["f1_score"]
                if manager_dict[model]["f7"]["return_code"] != return_code["train_success"]:
                    finish_reason.append(manager_dict[model]["reason"])
                accuracy_7 += manager_dict[model]["f7"]["report"]["accuracy"]
                precision_7 += manager_dict[model]["f7"]["report"]["precision"]
                recall_7 += manager_dict[model]["f7"]["report"]["recall"]
                f1_score_7 += manager_dict[model]["f7"]["report"]["f1_score"]
                
            self.accuracy_8 = 1.0 if accuracy_8 > 1 else round(accuracy_8, 2)
            self.precision_8 = 1.0 if precision_8 > 1 else round(precision_8, 2)
            self.recall_8 = 1.0 if recall_8 > 1 else round(recall_8, 2)
            self.f1_score_8 = 1.0 if f1_score_8 > 1 else round(f1_score_8, 2)

            self.accuracy_7 = 1.0 if accuracy_7 > 1 else round(accuracy_7, 2)
            self.precision_7 = 1.0 if precision_7 > 1 else round(precision_7, 2)
            self.recall_7 = 1.0 if recall_7 > 1 else round(recall_7, 2)
            self.f1_score_7 = 1.0 if f1_score_7 > 1 else round(f1_score_7, 2)

            self.kg_list = kg_list
            self.finish_reason = finish_reason
        return manager_dict

    def orm_to_table(self, tb, manager_dict, module_quantity=1):
        val_quantity = 450
        progress = 100
        try:
            session = open_connection(db_uri=self.SQLALCHEMY_DATABASE_URI)
            val_quantity = 450
            session.addprogress = 100

            session.add(tb)
            session.commit()  
            close_connection(session)
            self.init_logger.info("Save Fraud Detect Validation Report successfully insert into db")
        except Exception as e:
            session.rollback()
            self.init_logger.error("Save validation report fail: " + str(e))
        if module_quantity == 1:
            val_report = {
                "model_name": "fraud_detect",
                "validation_sample_count": str(val_quantity),
                "accuracy": str(self.accuracy),
                "precision": str(self.precision),
                "recall": str(self.recall),
                "f1_score": str(self.f1_score)
            }
        else:
            val_report = {
                "model_name": "fraud_detect",
                "validation_sample_count": str(val_quantity),
                "accuracy_8": str(self.accuracy_8),
                "precision_8": str(self.precision_8),
                "recall_8": str(self.recall_8),
                "f1_score_8": str(self.f1_score_8),

                "accuracy_7": str(self.accuracy_7),
                "precision_7": str(self.precision_7),
                "recall_7": str(self.recall_7),
                "f1_score_7": str(self.f1_score_7)
            }
        manager_dict["mq"].finish(return_code["train_all_success"], progress, self.kg_list, val_report, ", ".join(self.finish_reason))            


if __name__ == '__main__':
    pass
