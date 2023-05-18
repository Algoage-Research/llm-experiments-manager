import os
from sacred import Experiment

ex = Experiment()

source_filepaths = [
    'main.py'
]

for fpath in source_filepaths:
    if os.path.exists(fpath):
        ex.add_source_file(fpath)


@ex.config
def ex_config():
    user_configs = [
        {
            'instruction':
                'You are now assuming the role of a person who is considering job change.\n' +
                'generate simple comments one by one.\n' +
                'try behaving naturally as a real person, lazy for long text and visiting the places, might stop conversation if not satisfied.',
            'personas': persona,
            # 'openai_model': 'gpt-4'
            'openai_model': 'gpt-3.5-turbo',
            'definition_of_success': 'want to consider applying for a recommended company'
        } for persona in [
            # 下記のプロンプトをgpt-4に投げて作成しました
            # `11ペルソナあたり150文字程度で、転職先を探している（ただし、転職意欲が高いとは限らない）人のペルソナを5個作ってください`
            '高橋 悠介（32歳、男性）: ITエンジニア。専門的なスキルを持つが、現在の会社では技術の更新が遅く、満足していない。しかし、長い就業年数を考えると、転職には躊躇している。',
            '山口 由美子（29歳、女性）: マーケティング担当者。現在の職場の人間関係に不満があるものの、安定した生活を送りたいと考えているため、転職はリスクと感じている。',
            # '佐藤 明美（45歳、女性）: 事務職。長年働いてきたが、仕事のルーチンに飽きてきている。新しいことを学びたいが、年齢的な不安から転職には消極的。',
            # '吉田 雅彦（26歳、男性）: デザイナー。仕事は好きだが給料が低く、生活に困窮している。転職を考えているが、現在の職場の仲間との絆があり、躊躇している。',
            # '鈴木 一郎（39歳、男性）: 営業マン。職場でのパフォーマンスは良いが、家族と過ごす時間が欲しいと考えている。ワークライフバランスを重視した転職を検討中。'
        ]
    ]

    system_config = {
        'system_prompt': 'act like a great recruitment agent who is trying to introduce companies looking for members to a user.' +
        'try your best to make a user want to consider applying the company.' +
        'ask simple questions one by one first until you can confidently understand user\'s needs and recommend companies.' +
        '日本語で話をしてください。',
        'initial_prompt': None,
        'initial_message': 'こんにちは。転職先をお探しですか？ご要望をお聞かせください。',
        'openai_model': 'gpt-4'
        # 'openai_model': 'gpt-3.5-turbo'
    }

    evaluation_config = {
        'system_goal': 'making a user want to consider applying for a recommended company'
    }
