import json

def parser(input_str):
    '''
        input_str: "[[label, confident_score, xmin, ymin, xmax, ymax],...]"
    '''
    input_str = json.loads(input_str)
    for gt in input_str:
        label = gt[0]
        confident_score = gt[1]
        xmin = gt[2]
        ymin = gt[3]
        xmax = gt[4]
        ymax = gt[5]
        yield label, confident_score, xmin, ymin, xmax, ymax


def get_groundtruth_stats_by_model_id(model_id):
    from dm_modules.analytics_dao.groundtruth_dao import get_groundtruth_by_model_id
    gen = get_groundtruth_by_model_id(model_id)
    print(f'Model: {model_id}')
    print(f'gen: {len(list(gen))}')
    stats = {}
    for item in get_groundtruth_by_model_id(model_id):
        data = item.to_dict()
        gt = data['gt']
        for label, _, _, _, _, _ in parser(gt):
            if label not in stats:
                stats[label] = 0
            stats[label] += 1

    return stats

# print(get_groundtruth_stats_by_model_id('moap-crossarmfunc-cls'))


def get_groundtruth_stats_by_dataset_id(dataset_id):
    from dm_modules.analytics_dao.groundtruth_dao import get_groundtruth_by_dataset_id
    gen = get_groundtruth_by_dataset_id(dataset_id)
    print(f'Dataset: {dataset_id}')
    print(f'gen: {len(list(gen))}')
    stats = {}
    for item in get_groundtruth_by_dataset_id(dataset_id):
        data = item.to_dict()
        gt = data['gt']
        for label, _, _, _, _, _ in parser(gt):
            if label not in stats:
                stats[label] = 0
            stats[label] += 1

    return stats

# print(get_groundtruth_stats_by_dataset_id('moap_crossarmfunc_cls_infer'))


# def aggrate(list_of_):


def scan_all():
    from dm_modules.analytics_dao.groundtruth_dao import get_groundtruth
    gen = get_groundtruth()
    model_level = {}
    dataset_level = {}
    object_level = {}

    for item in gen:
        data = item.to_dict()
        gt = data['gt']
        for label, _, _, _, _, _ in parser(gt):
            #
            model_level.setdefault(data['model_id'], {}).setdefault(label, 0)
            model_level[data['model_id']][label] += 1

            #
            dataset_level.setdefault(data['dataset_id'], {}).setdefault(label, 0)
            dataset_level[data['dataset_id']][label] += 1

            #
            object_level.setdefault(label, 0)
            object_level[label] += 1

    # model level to to database
    from dm_modules.analytics_dao.dbms import execute_query
    query = "INSERT INTO annotation_stats_model_level (model_id, annotation_object, count) VALUES (%s, %s, %s)"
    data = []
    for model_id, stats in model_level.items():
        data.extend([(model_id, label, count) for label, count in stats.items()])
    print(f'Inserting {len(data)} rows into annotation_stats_model_level')
    print(f'query: {query}')
    print(f'data: {data}')
    # execute_query(query, data)

    # dataset level to to database
    query = "INSERT INTO annotation_stats_dataset_level (dataset_id, annotation_object, count) VALUES (%s, %s, %s)"
    data = []
    for dataset_id, stats in dataset_level.items():
        data.extend([(dataset_id, label, count) for label, count in stats.items()])
    print(f'Inserting {len(data)} rows into annotation_stats_dataset_level')
    print(f'query: {query}')
    print(f'data: {data}')

    # object level to to database
    query = "INSERT INTO annotation_stats_object_level (annotation_object, count) VALUES (%s, %s)"
    data = []
    for label, count in object_level.items():
        data.append((label, count))
    print(f'Inserting {len(data)} rows into annotation_stats_object_level')

    return model_level, dataset_level, object_level

model_level, dataset_level, object_level = scan_all()
# print(f'model_level: {model_level}')
# print(f'dataset_level: {dataset_level}')
# print(f'object_level: {object_level}')
