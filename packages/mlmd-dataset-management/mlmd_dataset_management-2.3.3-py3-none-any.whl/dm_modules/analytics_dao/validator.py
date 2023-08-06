
def validate(model_id, dataset_id, execution_id):
    from dm_modules.analytics_dao.prediction_dao import get_prediction_gen
    from dm_modules.analytics_dao.groundtruth_dao import get_groundtruth_gen
    from dm_modules.analytics_dao.utils.validator_utils import get_document_map
    from dm_modules.analytics_dao.utils.validator_utils import get_presion_recall

    prediction_gen = get_prediction_gen(execution_id)
    gt_gen = get_groundtruth_gen(dataset_id, model_id)
    
    document_map = get_document_map(model_id, gt_gen, prediction_gen)
    precision, recall = get_presion_recall(document_map)
    print("Precision/Recall: {}, {}".format(precision, recall))
    return precision, recall

# print(validate("moap-ir-hotspot-det", "test_moap_ir_hotspot_det_0"))