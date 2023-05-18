import os
import re
import openai
from agents.user_agent import UserAgent
from logger import generate_logger
from utils.try_with_interval import safe_chat_complete

logger = generate_logger(__name__)


def evaluate_user_experience(evaluation_config: dict, user_agent: UserAgent):
    '''
    This function evaluates the user experience of the agent.
    :param agent: The agent to evaluate.
    :return: A score between 0 and 1 .
    '''

    openai.api_key = os.environ['OPENAI_API_KEY']

    conversation_log_text = ''
    for event_log in user_agent.conversation_log:
        if event_log['text'] is not None:
            conversation_log_text += f'{event_log["sender_type"]} : {event_log["text"]}\n'

    prompt = f'''
# Instructions
This is a test of the user experience of a chat service.

# System Goal
{evaluation_config['system_goal']}

# Conversation
{conversation_log_text}

# Output Format (explicitly follow the format below including '##')

## score of the service
number 0 ~ 1
- 0.00: not working correctly for the mission
- 0.20: very bad
- 0.40: bad
- 0.50: okay
- 0.70: good (as good as average human professionals)
- 0.80: great (as good as great human professionals)
- 0.90: excellent (much better than great human professionals)
- 1.00: beyond imagination

## Reason of the score
text

## Improvement suggestions
text
    '''

    logger.debug(prompt)

    result = safe_chat_complete(
        chatcompletion_kwargs=dict(
            model='gpt-3.5-turbo',
            messages=[
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
        )
    )
    reply = result.choices[-1].message
    logger.debug(reply)

    split_reply = reply.content.split('##')

    parsed_result = {
        'score': float(re.search(r'\d+(?:\.\d+)?', reply.content).group()),
        'success': user_agent.success,
        'reason': split_reply[2].split('Reason of the score')[-1] if len(split_reply) >= 3 else None,
        'improvement_suggestions': split_reply[3].split('Improvement suggestions')[-1] if len(split_reply) >= 4 else None,
    }
    logger.info(parsed_result)

    return parsed_result
