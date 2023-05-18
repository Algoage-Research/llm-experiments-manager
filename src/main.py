import datetime
from typing import Dict, List
from sacred.observers import MongoObserver
from agents.system_agent import SystemAgent
from agents.user_agent import UserAgent
from config import ex
from evaluator import evaluate_user_experience
from logger import generate_logger

logger = generate_logger(__name__)

mongo_observer = MongoObserver.create(
    url='mongo:27017', db_name='train_log'
)
ex.observers.append(
    mongo_observer
)


@ex.automain
def main(user_configs: dict, system_config: dict, evaluation_config: dict, _run=None, *args, **kwargs):
    # create experiment id from sacred
    if _run is not None:
        run_id = _run._id
    else:
        run_id = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    scores = []
    success_count = 0
    iteration_mongo_collection = mongo_observer._client['train_log']['iterations']
    conversation_mongo_collection = mongo_observer._client['train_log']['conversations']
    for i, user_config in enumerate(user_configs):
        system_agent = SystemAgent(system_config=system_config)
        mocked_user_agent = UserAgent(
            user_config
        )

        while not (system_agent.is_finished() or mocked_user_agent.is_finished()):
            mocked_user_agent.input_text(
                system_agent.output_text(), system_agent)
            user_out = mocked_user_agent.output_text()
            if user_out is not None:
                system_agent.input_text(user_out)
        experiment_result = evaluate_user_experience(
            evaluation_config, mocked_user_agent)
        scores.append(experiment_result['score'])
        if mocked_user_agent.success:
            success_count += 1

        iteration_mongo_collection.insert_one({
            'run_id': run_id,
            'iteration': i,
            'result': experiment_result,
            'info': {
                'user_config': user_config,
            }
        })
        conversation_mongo_collection.insert_one(
            {
                'run_id': run_id,
                'iteration': i,
                'conversation_log': mocked_user_agent.conversation_log,
            }
        )

    ex.log_scalar(f'average_score', sum(scores)/len(scores))
    ex.log_scalar(f'success_rate', success_count/len(scores))
    for key in experiment_result:
        _run.info[f'result_{key}'] = experiment_result[key]
