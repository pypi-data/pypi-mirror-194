
def is_detection(model_id):
    return "selectnet" not in model_id and "cls" not in model_id

def get_groundtruth_generator(dataset_id):
    import dataset_manager as dm
    dataset = dm.get_dataset(dataset_id)
    return dataset.get_filelist(get_annotation=True)

def get_prediction_generator(filepath):
    import os
    if not os.path.isfile(filepath):
        raise Exception("prediction_generator: file {} not found".format(filepath))
    f = open(filepath, "r")
    for line in f:
        yield line.rstrip()

def get_document_map(model_id, gt_gen, prediction_gen):
    """
    classification case generated format for each item: image_id, [[label_index, confident_score],...]
    detection case generated format for each item: image_id, [[batch_index, label_index, confident_score, xmin, ymin, xmax, ymax],...]
    """
    import json
    model_id = model_id.replace("-", "_")
    gt = next(gt_gen)
    prediction = next(prediction_gen)
    document_map = {}
    while gt and prediction:
        gt = gt.to_dict()
        prediction = prediction.to_dict()
        document_id_gt = gt['document_id']
        document_id_pred = prediction['document_id']
        document_map.setdefault(document_id_gt, {})["gt"] = json.loads(gt.get("gt"))
        prediction_output = prediction.get(model_id).strip('\"')
        document_map.setdefault(document_id_pred, {})["pred"] = json.loads(prediction_output)
        gt = next(gt_gen, None)
        prediction = next(prediction_gen, None)
    return document_map


def get_presion_recall(document_map, iou_threshold=0.5):
    from utils.coord_utils import calculate_iou
    true_positives = 0
    false_positives = 0
    false_negatives = 0
    for document_id, item in document_map.items():
        predicted_boxes = item['pred']
        gt_boxes = item['gt']
        for pred_box in predicted_boxes:
            iou_max = 0
            match = None

            for gt_box in gt_boxes:
                iou = calculate_iou(pred_box, gt_box)
                if iou > iou_max:
                    iou_max = iou
                    match = gt_box

            if iou_max >= iou_threshold and match is not None:
                true_positives += 1
                gt_boxes.remove(match)
            else:
                false_positives += 1

        false_negatives += len(gt_boxes)
    
    precision = true_positives / (true_positives + false_positives)
    recall = true_positives / (true_positives + false_negatives)

    return precision, recall